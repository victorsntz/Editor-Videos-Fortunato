# Editor de vídeos · Victor Fortunato

Aqui o Claude Code edita os vídeos do Victor Fortunato (Fortunato Estúdio): Reels, vlogs do estúdio e cortes pro YouTube. Tudo em português do Brasil.

## Antes de qualquer edição

1. Ler o `ESTILO.md` inteiro. Ele é a fonte única do estilo e vence qualquer regra genérica da skill de edição.
2. Conferir se o vídeo bruto é HDR (comum em iPhone). Se for, converter pra SDR com a conversão de cor da própria Apple (AVFoundation) antes de montar.

## Pastas

- `brutos/`: vídeos gravados, um subdiretório por projeto (`brutos/2026-10-10-nome-do-video/`).
- `renders/`: vídeos prontos, em `renders/<projeto>.mp4`.
- `ESTILO.md`: o estilo.
- `.claude/skills/`: a skill de edição, quando estiver instalada.

Vídeo e áudio nunca vão pro GitHub (o `.gitignore` já barra). Se um arquivo de mídia aparecer pra commit, parar e avisar.

## Como editar: sempre por etapas

1. **Corte e legenda:** mostrar o corte proposto e o texto da legenda já corrigido. Esperar aprovação.
2. **Roteiro de elementos:** o que entra na tela, segundo a segundo, com imagens dos momentos principais. Esperar aprovação.
3. **Render:** só depois das duas aprovações.

Nunca renderizar direto sem passar pelas etapas 1 e 2.

## Quando o Victor disser "salva isso"

1. Escrever a regra na seção do `ESTILO.md` onde ela se encaixa (legenda, movimento, som e assim por diante).
2. Acrescentar uma linha na seção **9. Notas**: `data · vídeo · o que mudou e por quê`.
3. Fazer o commit e o push.

## Como falar com o Victor

Ele é designer de marcas e lidera uma agência. Falar simples, como gente, com exemplo concreto. Sem travessão, sem jargão de IA, sem a frase "não é sobre X, é sobre Y". Pode ter humor rápido.

## Primeira vez num computador novo

O método vem do guia "Edite Reels com IA", que usa o kit WeAreNoCode-YouTube-Editor (baixado da comunidade gratuita skool.com/wearenocode) e o HyperFrames.

1. Instalar a skill do kit em `.claude/skills/`, instalar o HyperFrames e as skills dele, conferir FFmpeg, Node e Python e rodar os testes.
2. Rodar `npx hyperframes doctor` e resolver o que faltar.
3. Adaptar a skill pra Reels com o nome `reels-edit`, apontando pro `ESTILO.md` da raiz deste projeto. As regras técnicas (formato, zona segura, entrega) estão na seção 7 do `ESTILO.md`.

Antes de instalar o kit, ler os arquivos dele e explicar pro Victor o que cada script faz.
