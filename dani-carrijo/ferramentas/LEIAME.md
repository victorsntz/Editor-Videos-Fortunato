# Ferramentas de edição da Dani

- `transcribe.py`: transcreve os takes com Whisper large-v3 (palavra por palavra, com tempo).
- `check.py`: emenda dois trechos de áudio e transcreve de novo, pra conferir se um corte ficou limpo.
- `overlay.html` + `frames.js`: o motor de grafismo. A página desenha legenda, gancho, cartão de termo, rótulo de capítulo, logo com ondas e cartelas a partir de uma lista de eventos com tempo. O `frames.js` abre no Chromium (Playwright) e salva cada quadro em PNG transparente pra compor por cima do vídeo no FFmpeg.

Pra rodar o motor, colocar na mesma pasta do `overlay.html`: as fontes (Libre Caslon Condensed e Satoshi) e os logos de `../marca/` (`logo-horizontal.png`, `logo-empilhado.png`).

Os scripts de cada vídeo (corte, legenda, prévia) ficam na pasta do projeto, em `../projetos/`.
