# Roteiro do ep. 01: planos de câmera (shots.json) e peças gráficas (eventos.json)
import json
C = json.load(open('/tmp/claude-0/legendas.json'))
E = json.load(open('/tmp/claude-0/edl.json'))
DUR = E['duration']          # fim da fala
END = DUR + 4.6              # cartela final
c = lambda i: C[i]['s']      # início da legenda i

# ---------- planos ----------
# W aberto · M médio · C fechado · L ela à esquerda (painel na direita) · R ela à direita (título na esquerda)
# (início, tipo, zoom inicial, zoom final). Troca sempre no começo de uma frase; zoom final > inicial = aproximação lenta.
S = [
 (0.00, 'R', 1.18, 1.26),                         # gancho
 (E['segments'][1]['t0'], 'W', 1.00, 1.03), (c(1), 'M', 1.30, 1.33), (c(2), 'C', 1.55, 1.66), (c(3), 'W', 1.00, 1.02),
 (c(4), 'M', 1.30, 1.34), (c(5), 'C', 1.58, 1.64),
 (c(6), 'W', 1.00, 1.04), (c(7), 'L', 1.22, 1.24), (c(8), 'L', 1.40, 1.42), (c(9), 'L', 1.42, 1.58),   # "investigar"
 (c(10), 'L', 1.22, 1.24), (c(11), 'L', 1.40, 1.42), (c(13), 'L', 1.24, 1.26), (c(15), 'L', 1.42, 1.44),
 (c(17), 'L', 1.30, 1.56),                         # cicatriciais: aproximação lenta, assunto sério
 (c(20), 'W', 1.00, 1.03), (c(21), 'C', 1.50, 1.68),   # "o quanto antes"
 (c(22), 'L', 1.20, 1.22), (c(24), 'L', 1.38, 1.40), (c(26), 'L', 1.22, 1.24), (c(28), 'L', 1.38, 1.40),
 (c(29), 'L', 1.22, 1.24), (c(30), 'L', 1.40, 1.42), (c(31), 'C', 1.50, 1.60),
 (c(33), 'L', 1.24, 1.26), (c(35), 'L', 1.42, 1.56),
 (c(37), 'W', 1.00, 1.03), (c(38), 'M', 1.30, 1.32), (c(39), 'C', 1.50, 1.70),  # "não é pra todo mundo"
 (c(41), 'L', 1.22, 1.24), (c(43), 'L', 1.40, 1.42), (c(45), 'L', 1.24, 1.26), (c(46), 'L', 1.40, 1.42),
 (c(48), 'M', 1.30, 1.32), (c(49), 'C', 1.55, 1.62),
 (c(50), 'W', 1.00, 1.03), (c(51), 'C', 1.50, 1.70),   # "nunca acontece do nada"
 (c(52), 'L', 1.24, 1.26), (c(53), 'L', 1.40, 1.42), (c(55), 'L', 1.24, 1.26), (c(56), 'L', 1.40, 1.42), (c(58), 'L', 1.30, 1.44),
 (c(59), 'W', 1.00, 1.03), (c(60), 'M', 1.30, 1.32), (c(61), 'C', 1.55, 1.60), (c(62), 'M', 1.32, 1.34),
 (c(63), 'W', 1.00, 1.02), (c(64), 'C', 1.50, 1.60),
]
# cada emenda dentro de um take (pausa ou tropeço removido) precisa cair numa troca de plano, senão vira pulo
for cut in [g['t0'] for g in E['segments']][1:]:
    near = [i for i, x in enumerate(S) if abs(x[0] - cut) < 0.4]
    if near: S[near[0]] = (cut,) + S[near[0]][1:]
    else:
        i = max(j for j, x in enumerate(S) if x[0] < cut); k, z0, z1 = S[i][1:]
        S.insert(i + 1, (cut, k, 1.24 if z0 > 1.32 else 1.42, (1.24 if z0 > 1.32 else 1.42) + 0.02))
shots = [{'s': round(a, 3), 'e': round(S[i+1][0] if i+1 < len(S) else DUR, 3), 'kind': k, 'z0': z0, 'z1': z1}
         for i, (a, k, z0, z1) in enumerate(S)]
json.dump({'shots': shots, 'end': END}, open('/tmp/claude-0/shots.json', 'w'), indent=1)

# ---------- peças ----------
ev = []
cuts = [s['t0'] for s in E['segments']]
take = [E['segments'][i]['t0'] for i in range(len(E['segments'])) if i == 0 or E['segments'][i]['clip'] != E['segments'][i-1]['clip']]
# take = inícios de cada take: 0, 6.95, 17.06, 22.43, 68.12, 104.49, 133.62, 157.47

ev.append({'type': 'bug', 'start': take[2] + 0.6, 'end': DUR - 0.5})
chap = [(take[2], '01', 'O que é terapia capilar'), (take[3], '02', 'O que ela trata'),
        (take[4], '03', 'Tudo começa na avaliação'), (take[5], '04', 'Tratamento direcionado'),
        (take[6], '05', 'Por que o cabelo cai'), (take[7], '06', 'O que vem no canal')]
for t, n, lab in chap:
    ev.append({'type': 'chapter', 'start': t + 0.35, 'end': t + 4.6, 'n': n, 'label': lab})

ev.append({'type': 'list', 'start': c(7) - 0.2, 'end': c(20) - 0.1, 'eyebrow': 'Terapia capilar trata', 'title': 'Patologias',
           'items': [{'t': c(7) + 0.3, 'title': 'Queda de cabelo', 'desc': 'Muito comum. O importante é investigar a causa.'},
                     {'t': c(10), 'title': 'Dermatite seborreica', 'desc': 'Caspa, excesso de sebo e descamação.'},
                     {'t': c(13), 'title': 'Alopecia androgenética', 'desc': 'Predisposição genética. As entradas abrem.'},
                     {'t': c(17), 'title': 'Alopecias cicatriciais', 'desc': 'O folículo cicatriza e o fio não volta.'}]})
ev.append({'type': 'list', 'start': c(22) + 0.3, 'end': c(32) - 0.25, 'eyebrow': 'Na avaliação', 'title': 'Tudo começa aqui',
           'items': [{'t': c(23), 'title': 'Uma conversa', 'desc': 'Entender o couro cabeludo e os fios.'},
                     {'t': c(26), 'title': 'Produto específico', 'desc': 'De acordo com cada necessidade.'},
                     {'t': c(28), 'title': 'Médicos e nutricionistas', 'desc': 'Parcerias pra cuidar da saúde toda.'},
                     {'t': c(30), 'title': 'Vitaminas e hormônios', 'desc': 'E a saúde de um modo geral.'}]})
ev.append({'type': 'list', 'start': c(33) - 0.1, 'end': c(37) - 0.2, 'eyebrow': 'Sinais de alerta', 'title': 'Fique de olho',
           'items': [{'t': c(33) + 0.4, 'title': 'Queda de cabelo'},
                     {'t': c(34), 'title': 'Descamação'},
                     {'t': c(34) + 0.9, 'title': 'Excesso de oleosidade'},
                     {'t': c(36), 'title': 'Algo que você nunca teve', 'desc': 'Pode ter alguma coisa alterada.'}]})
ev.append({'type': 'list', 'start': c(41) - 0.1, 'end': c(48) - 0.2, 'eyebrow': 'Cada caso, um caminho', 'title': 'Não é igual',
           'items': [{'t': c(44), 'title': 'Fortalecimento', 'desc': 'Pra quem tem queda.'},
                     {'t': c(45), 'title': 'Dermatite seborreica', 'desc': 'Controle de oleosidade e dos processos inflamatórios.'}]})
ev.append({'type': 'number', 'start': c(52) - 0.1, 'end': c(59) - 0.2, 'eyebrow': 'A queda vem depois', 'value': 3, 'unit': 'meses',
           'sub': 'é o tempo comum entre um trauma e a queda.',
           'pills': [{'t': c(53) + 0.6, 'text': 'Cirurgia'}, {'t': c(54) + 0.6, 'text': 'Inflamação no couro'},
                     {'t': c(55) + 0.9, 'text': 'Dengue'}, {'t': c(55) + 1.5, 'text': 'Covid'}, {'t': c(57) + 0.6, 'text': 'Chikungunya'}]})

ev.append({'type': 'hook', 'start': 0.0, 'end': take[1] - 0.25, 'eyebrow': 'Terapia capilar · Episódio 01',
           'title': 'Você sabe<br>pra que serve a<br><em>terapia capilar?</em>'})
ev.append({'type': 'logo', 'start': take[1] - 0.05, 'end': take[1] + 2.5})
ev.append({'type': 'quote', 'start': c(32) - 0.15, 'end': c(33) + 0.7, 'text': 'O cabelo é um<br><b>marcador</b> de saúde.'})

for i, cap in enumerate(C):
    if i == 32: continue                     # a cartela já diz a frase
    ev.append({'type': 'caption', 'start': cap['s'], 'end': min(cap['e'], DUR), 'html': cap['html']})

ev.append({'type': 'end', 'start': DUR - 0.05, 'end': END, 'out': 0.01, 'cta': 'Sua raiz merece atenção.'})

# transição de ondas em cada troca de bloco (o corte acontece no meio dela)
for t in take[2:] + [DUR]:
    ev.append({'type': 'wipe', 'start': t - 0.45, 'end': t + 0.45})
json.dump(ev, open('/tmp/claude-0/eventos.json', 'w'), ensure_ascii=False, indent=1)
print(len(shots), 'planos ·', len(ev), 'peças · fim', round(END, 2))
