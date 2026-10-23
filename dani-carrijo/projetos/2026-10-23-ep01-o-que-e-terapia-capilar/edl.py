import json, wave
import numpy as np
d = json.load(open('/tmp/claude-0/transcript.json'))
ORDER = ['IMG_8569', 'IMG_8576', 'IMG_8577', 'IMG_8579', 'IMG_8583', 'IMG_8584', 'IMG_8586', 'IMG_8587']
# trechos removidos (tempo no bruto), conferidos re-transcrevendo o áudio emendado
REMOVE = {'IMG_8579': [(6.30, 7.50)],    # "muitas mulheres" repetido
          'IMG_8583': [(14.60, 17.10)],  # "ver como está a saúde" dito duas vezes
          'IMG_8584': [(24.60, 25.35)]}  # "então assim"
GAP = 0.45; PRE = 0.10; POST = 0.22

def env(k):
    w = wave.open(f'/tmp/claude-0/audio/{k}.wav')
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
    h = 160; n = len(a) // h
    return np.convolve(np.sqrt((a[:n*h].reshape(n, h)**2).mean(1)), np.ones(5)/5, 'same')  # 10 ms

def snap(e, x, lo, hi):
    """leva o ponto de corte pro trecho mais silencioso perto dele"""
    lo = max(lo, x - 0.15, 0); hi = min(hi, x + 0.15, len(e)/100 - 0.01)
    if hi <= lo: return x
    i0, i1 = int(lo*100), int(hi*100) + 1
    return (i0 + int(np.argmin(e[i0:i1]))) / 100

def onset(e, a, b):
    floor = np.percentile(e, 10); peak = np.percentile(e, 95); thr = floor + 0.08 * (peak - floor)
    i0, i1 = int(a * 100), min(int(b * 100), len(e) - 3)
    return next((k / 100 for k in range(i0, i1) if (e[k:k+3] > thr).all()), None)

segs = []; words_out = []; T = 0.0
for k in ORDER:
    ws = [dict(w, w=w['w'].strip()) for s in d[k] for w in s['words']]
    rem = REMOVE.get(k, []); E = env(k)
    mid = lambda w: (w['s'] + w['e']) / 2
    keep = [w for w in ws if not any(a <= mid(w) < b for a, b in rem)]
    runs = [[keep[0]]]
    for w in keep[1:]:
        p = runs[-1][-1]
        crosses = any(mid(p) < a <= mid(w) for a, b in rem)
        if w['s'] - p['e'] > GAP or crosses: runs.append([w])
        else: runs[-1].append(w)
    for r in runs:
        I = ws.index(r[0]); J = ws.index(r[-1])
        prev_e = ws[I-1]['e'] if I > 0 else 0
        next_s = ws[J+1]['s'] if J+1 < len(ws) else 99
        after_rem = [b for a, b in rem if (mid(ws[I-1]) if I > 0 else -1) < b <= mid(r[0]) + 0.01 and a < mid(r[0])]
        before_rem = [a for a, b in rem if mid(r[-1]) < a and (J+1 >= len(ws) or mid(ws[J+1]) >= a)]
        a = after_rem[0] if after_rem else snap(E, max(0, r[0]['s'] - PRE), prev_e, r[0]['s'])
        if not after_rem:
            # o Whisper às vezes marca a 1ª palavra em 0,00 s mesmo com silêncio antes: corta rente à voz de verdade
            on = onset(E, a, a + 2.5)
            if on is not None and on - 0.06 - a > 0.12: a = round(on - 0.06, 2)
        b = before_rem[0] if before_rem else snap(E, r[-1]['e'] + POST, r[-1]['e'] - 0.04, next_s)
        segs.append({'clip': k, 'in': round(a, 3), 'out': round(b, 3), 't0': round(T, 3)})
        for w in r:
            words_out.append({'w': w['w'], 's': round(T + max(0, w['s'] - a), 3), 'e': round(T + max(w['e'] - a, max(0, w['s'] - a) + 0.12), 3), 'clip': k})
        T += b - a
json.dump({'segments': segs, 'words': words_out, 'duration': T}, open('/tmp/claude-0/edl.json', 'w'), ensure_ascii=False, indent=1)
print(len(segs), 'segmentos, duração', round(T, 2))
for s in segs: print(s)
