# Legenda: "fala original ==> texto na tela". *palavra* = ênfase (Caslon itálico terracota).
import json, re, unicodedata
L = r"""
#HOOK Você já ouviu falar em terapia capilar ou sabe para que realmente a terapia serve?
Hoje eu vou te explicar como que funciona a terapia capilar, ==> Hoje eu vou te explicar como funciona a *terapia capilar*,
a importância de uma avaliação no couro cabeludo e nos fios ==> a importância de uma avaliação no couro cabeludo e nos fios
e por que que é tão importante cuidar do couro cabeludo também ==> e por que é tão importante cuidar do *couro cabeludo* também,
e não só a estética de fios. ==> e não só da estética dos fios.
A terapia capilar envolve cuidados para tratar ==> A terapia capilar envolve cuidados pra tratar
tanto do couro cabeludo quanto da fibra capilar. ==> tanto do couro cabeludo quanto da *fibra capilar*.
No couro cabeludo pode envolver várias patologias, ==> No couro cabeludo, pode envolver várias *patologias*,
desde a queda de cabelo, que é muito comum. ==> desde a queda de cabelo, que é muito comum.
Hoje em dia muitas mulheres têm queda de cabelo ==> Hoje em dia muitas mulheres têm queda de cabelo,
e é muito importante investigar o que está causando essa queda. ==> e é muito importante *investigar* o que está causando essa queda.
Dermatite seborreica, tem muita gente que convive com caspa, ==> Dermatite seborreica: tem muita gente que convive com *caspa*,
com excesso de sebo, de escamação, uma vida inteira ==> com excesso de sebo, descamação, uma vida inteira,
e não busca um tratamento. ==> e não busca tratamento.
Alopecia androgenética, ==> *Alopecia androgenética*:
alopecia quando você tem uma predisposição genética à calvície, ==> quando você tem uma predisposição genética à calvície.
então começa a perder cabelos nas regiões das entradas, ==> Começa a perder cabelo na região das *entradas*,
deixa essa região frontal mais aberta. ==> deixa essa região frontal mais aberta.
Ou tem também alopecia cicatriciais, ==> Tem também as *alopecias cicatriciais*,
que é quando o folículo cicatriza ==> que é quando o folículo cicatriza,
e nesse caso já não tem mais tratamento. ==> e nesse caso já não tem mais tratamento.
Então tem várias patologias que a gente trata dentro da terapia capilar ==> Então são várias patologias que a gente trata na terapia capilar,
e por isso que é muito importante buscar o tratamento o quanto antes. ==> e por isso é muito importante buscar tratamento *o quanto antes*.
E na terapia capilar, tudo começa ==> E na terapia capilar, tudo começa
a partir de uma conversa, na avaliação. ==> a partir de uma *conversa*, na avaliação.
Eu quero entender melhor as necessidades ==> Eu quero entender melhor as necessidades
do couro cabeludo, dos fios. ==> do couro cabeludo e dos fios.
Direcionar esse cliente a um produto mais específico, ==> Direcionar pra um produto mais *específico*,
de acordo com as necessidades. ==> de acordo com as necessidades.
Aqui nós temos várias parcerias com médicos, nutricionistas, ==> Aqui nós temos parcerias com médicos e nutricionistas,
para direcionar esse cliente a tratar melhor da sua saúde. ==> pra direcionar cada cliente a cuidar melhor da saúde.
Ver como que está vitaminas, questões hormonais. ==> Ver como estão as vitaminas, as questões hormonais,
Ver como que está a saúde, de um modo geral. ==> como está a saúde de um modo geral.
Porque o cabelo é um marcador de saúde. ==> Porque o cabelo é um *marcador de saúde*.
Quando começa a ter queda de cabelo, ==> Quando começa a ter queda de cabelo,
descamação, excesso de oleosidade, ==> descamação, excesso de oleosidade,
coisas que a pessoa nunca teve, ==> coisas que a pessoa nunca teve,
pode procurar que tenha alguma coisa alterada. ==> pode procurar: tem alguma coisa *alterada*.
Então essa conversa é muito importante ==> Então essa conversa é muito importante
para a gente direcionar para um tratamento mais específico, ==> pra gente direcionar pra um tratamento mais específico.
não é um tratamento para todo mundo, ==> Não é um tratamento pra todo mundo,
é um tratamento mais direcionado de acordo com a necessidade, ==> é um tratamento *direcionado*, de acordo com a necessidade.
então às vezes um tratamento de fortalecimento ==> Às vezes, um tratamento de fortalecimento
não vai ser um tratamento para uma pessoa ==> não vai servir pra uma pessoa
que tem, por exemplo, dermatite seborreica, ==> que tem, por exemplo, dermatite seborreica.
fortalecimento a gente trata queda, ==> Com fortalecimento, a gente trata *queda*.
dermatite seborreica é controle de oleosidade, ==> Dermatite seborreica é *controle de oleosidade*,
é tratar processos inflamatórios ==> é tratar processos inflamatórios
também que acontecem no couro cabeludo, ==> que também acontecem no couro cabeludo.
essa avaliação é muito importante ==> Essa avaliação é muito importante
para a gente descobrir realmente as necessidades. ==> pra gente descobrir *de verdade* as necessidades.
Vamos falar de uma queda capilar, por exemplo. ==> Vamos falar de queda capilar, por exemplo.
Ela nunca acontece assim, do nada. ==> Ela nunca acontece assim, *do nada*.
Uma queda, geralmente, ela vem três meses após algum trauma, ==> Geralmente, a queda vem *três meses* após algum trauma:
seja porque a pessoa passou por um processo de cirurgia, ==> seja porque a pessoa passou por uma cirurgia,
teve algum processo inflamatório no couro cabeludo, ==> teve algum processo inflamatório no couro cabeludo
um exemplo, teve dengue ou covid. ==> ou, por exemplo, teve dengue ou covid.
Hoje em dia tem muitas pessoas que estão tendo muita queda de cabelo ==> Hoje em dia tem muita gente com queda de cabelo
após dengue ou chikungunya. ==> depois de dengue ou *chikungunya*.
Tudo isso pode interferir para a pessoa ter queda de cabelo. ==> Tudo isso pode interferir e causar queda de cabelo.
Então esse canal vai ser muito importante ==> Então esse canal vai ser muito importante
para tirar suas dúvidas, todas relacionadas a couro cabeludo e fios, ==> pra tirar suas dúvidas sobre couro cabeludo e fios,
te ensinar como cuidar dos seus cabelos em casa, ==> te ensinar a cuidar dos seus *cabelos em casa*,
processos básicos que às vezes a pessoa não sabe. ==> cuidados básicos que às vezes a pessoa não sabe.
Esse canal vai ser destinado para te auxiliar no seu tratamento ==> Esse canal vai ser pra te ajudar no seu tratamento
e deixar seu cabelo cada dia mais incrível. ==> e deixar seu cabelo cada dia mais *incrível*.
"""
norm = lambda s: re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', s.lower()).encode('ascii', 'ignore').decode())
E = json.load(open('/tmp/claude-0/edl.json')); W = E['words']; i = 0; caps = []
for line in L.strip().splitlines():
    hook = line.startswith('#HOOK ')
    src, _, txt = line.replace('#HOOK ', '').partition(' ==> ')
    toks = src.split(); first = i
    for t in toks:
        assert norm(t) == norm(W[i]['w']), (line, t, W[i]['w']); i += 1
    if hook: continue
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', txt)
    caps.append({'s': W[first]['s'], 'e': W[i-1]['e'], 'text': txt, 'html': html})
assert i == len(W), (i, len(W))
# cada legenda fica até a próxima começar (se o buraco for curto)
for a, b in zip(caps, caps[1:]):
    if b['s'] - a['e'] < 0.7: a['e'] = b['s']
    else: a['e'] += 0.3
caps[-1]['e'] += 0.4
json.dump(caps, open('/tmp/claude-0/legendas.json', 'w'), ensure_ascii=False, indent=1)
print(len(caps), 'legendas ok')
