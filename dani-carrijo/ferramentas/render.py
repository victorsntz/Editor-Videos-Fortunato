# Compositor: corte + enquadramento (zoom no 4K) + grafismo + áudio -> mp4 final
import json, os, subprocess, sys, time
import numpy as np, cv2
B = '/home/user/Editor-Videos-Fortunato/dani-carrijo/brutos/2026-10-23-dani-youtube'
OUT = sys.argv[1]
OV = '/tmp/claude-0/ov'
FPS = 30; W, H = 1920, 1080; SW, SH = 2880, 1620          # decodifica o 4K em 2880 (sobra pra zoom de 1,6x)
E = json.load(open('/tmp/claude-0/edl.json')); SH_ = json.load(open('/tmp/claude-0/shots.json'))
shots, END = SH_['shots'], SH_['end']; DUR = E['duration']
faces = json.load(open('/tmp/claude-0/faces.json'))
GRADE = 'eq=contrast=1.04:saturation=1.03,colorbalance=rs=.015:bs=-.015'

def src_of(t):
    for g in E['segments']:
        if g['t0'] <= t < g['t0'] + g['out'] - g['in'] + 1e-6: return g['clip'], g['in'] + t - g['t0']
    g = E['segments'][-1]; return g['clip'], g['out']

def face_for(shot):
    """posição do rosto (mediana) durante o plano, pra câmera não ficar andando"""
    clip, a = src_of(shot['s']); _, b = src_of(max(shot['s'], shot['e'] - 0.05))
    pts = [p for p in faces[clip] if a - 0.6 <= p[0] <= b + 0.6] or faces[clip]
    return float(np.median([p[1] for p in pts])), float(np.median([p[2] for p in pts]))
for s in shots: s['fx'], s['fy'] = face_for(s)

def crop_for(t):
    sh = next((s for s in shots if s['s'] <= t < s['e']), shots[-1])
    u = min(1, max(0, (t - sh['s']) / max(0.01, sh['e'] - sh['s']))); u = u * u * (3 - 2 * u)
    z = sh['z0'] + (sh['z1'] - sh['z0']) * u
    cw, ch = 1 / z, 1 / z
    fx, fy = sh['fx'], sh['fy']
    cx = {'W': 0.5, 'M': fx, 'C': fx, 'L': fx + 0.15 * cw, 'R': fx - 0.17 * cw}[sh['kind']]
    x = min(max(cx - cw / 2, 0), 1 - cw)
    y = min(max(fy - (0.5 if sh['kind'] == 'W' else 0.33) * ch, 0), 1 - ch)
    return x * SW, y * SH, cw * SW                    # canto e largura do recorte, em pixels do quadro de 2880

def frame_out(img, t):
    x, y, cw = crop_for(t); s = W / cw
    if s < 1:                                          # reduz com média de área antes (sem serrilhado)
        img = cv2.resize(img, None, fx=s, fy=s, interpolation=cv2.INTER_AREA); x, y, s2 = x * s, y * s, 1
    else: s2 = s
    M = np.float32([[s2, 0, -x * s2], [0, s2, -y * s2]])
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

def comp(base, n):
    p = f'{OV}/f{n:06d}.png'
    if not os.path.exists(p): return base
    ov = cv2.imread(p, cv2.IMREAD_UNCHANGED)
    if ov.ndim == 2 or ov.shape[2] == 3: return ov if ov.ndim == 3 else cv2.cvtColor(ov, cv2.COLOR_GRAY2BGR)   # quadro opaco (cartela cheia)
    a = ov[:, :, 3:4].astype(np.float32) / 255
    return (base.astype(np.float32) * (1 - a) + ov[:, :, :3].astype(np.float32) * a).astype(np.uint8)

# ---------- áudio ----------
wav = '/tmp/claude-0/audio_final.wav'
args = ['ffmpeg', '-v', 'error', '-y']; f = []
for i, g in enumerate(E['segments']):
    d = round(g['out'] - g['in'], 3)
    args += ['-ss', str(g['in']), '-t', str(d), '-i', f"{B}/{g['clip']}.MOV"]
    f.append(f"[{i}:a]aresample=48000,afade=t=in:d=0.012,afade=t=out:st={d-0.015:.3f}:d=0.015[a{i}]")
n = len(E['segments'])
f.append(''.join(f'[a{i}]' for i in range(n)) + f'concat=n={n}:v=0:a=1,highpass=f=70,loudnorm=I=-14:TP=-1.2:LRA=9,apad=whole_dur={END:.3f}[a]')
subprocess.run(args + ['-filter_complex', ';'.join(f), '-map', '[a]', '-ar', '48000', wav], check=True)

# ---------- vídeo ----------
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
    '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p',
    '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-c:a', 'aac', '-b:a', '256k',
    '-movflags', '+faststart', '-shortest', OUT], stdin=subprocess.PIPE)
NTOT = round(END * FPS); nfr = 0
for gi, g in enumerate(E['segments']):
    N0 = round(g['t0'] * FPS); N1 = round((g['t0'] + g['out'] - g['in']) * FPS) if gi + 1 < len(E['segments']) else round(DUR * FPS)
    dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(g['in'] + (N0 / FPS - g['t0'])), '-i', f"{B}/{g['clip']}.MOV", '-frames:v', str(N1 - N0),
        '-vf', f'fps={FPS},scale={SW}:{SH}:flags=lanczos,{GRADE}', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE)
    last = None
    for k in range(N0, N1):
        buf = dec.stdout.read(SW * SH * 3)
        if len(buf) == SW * SH * 3: last = np.frombuffer(buf, np.uint8).reshape(SH, SW, 3)
        enc.stdin.write(comp(frame_out(last, k / FPS), k).tobytes()); nfr += 1
    dec.wait()
    print(f"{g['clip']} ok · {nfr}/{NTOT} · {time.strftime('%H:%M:%S')}", flush=True)
black = np.zeros((H, W, 3), np.uint8)
for k in range(nfr, NTOT): enc.stdin.write(comp(black, k).tobytes())
enc.stdin.close(); enc.wait()
print('pronto', OUT)
