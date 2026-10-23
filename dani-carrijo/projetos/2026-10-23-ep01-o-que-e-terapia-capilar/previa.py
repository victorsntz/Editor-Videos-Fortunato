import json, subprocess
E=json.load(open('/tmp/claude-0/edl.json')); C=json.load(open('/tmp/claude-0/legendas.json'))
B='/home/user/Editor-Videos-Fortunato/dani-carrijo/brutos/2026-10-23-dani-youtube'
def ts(t): h=int(t//3600); m=int(t%3600//60); s=t%60; return f"{h}:{m:02d}:{s:05.2f}"
# ASS: Satoshi Medium bege, ênfase Caslon itálico terracota (BGR no ASS)
ass="""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Satoshi Medium,54,&H00EDF6FC,&H00EDF6FC,&H64000000,&H8C000000,0,0,0,0,100,100,0,0,1,0,2.2,2,260,260,92,1
Style: Hook,Libre Caslon Condensed,112,&H00EDF6FC,&H00EDF6FC,&H64000000,&H8C000000,1,0,0,0,100,100,0,0,1,0,3,4,120,700,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ass+=f"Dialogue: 0,{ts(0.1)},{ts(E['segments'][0]['out'])},Hook,,0,0,0,,{{\\fad(250,200)}}VOCÊ SABE PRA\\NQUE SERVE A\\N{{\\fnLibre Caslon Condensed\\i1\\b0\\c&H546CC1&}}terapia capilar{{\\r}}?\n"
for c in C:
    t=c['text']
    import re
    t=re.sub(r'\*(.+?)\*',lambda m:'{\\fnLibre Caslon Condensed\\i1\\fs64\\c&H546CC1&}'+m.group(1)+'{\\r}',t)
    ass+=f"Dialogue: 0,{ts(c['s'])},{ts(c['e'])},Cap,,0,0,0,,{{\\fad(150,0)}}{t}\n"
open('/tmp/claude-0/previa.ass','w').write(ass)
args=['ffmpeg','-v','error','-y']; f=[]
for i,s in enumerate(E['segments']):
    args+=['-ss',str(s['in']),'-t',str(round(s['out']-s['in'],3)),'-i',f"{B}/{s['clip']}.MOV"]
    f.append(f"[{i}:v]fps=30,scale=1920:1080,setsar=1[v{i}];[{i}:a]aresample=48000,afade=t=in:d=0.012,afade=t=out:st={round(s['out']-s['in']-0.015,3)}:d=0.015[a{i}]")
n=len(E['segments'])
f.append(''.join(f"[v{i}][a{i}]" for i in range(n))+f"concat=n={n}:v=1:a=1[v][a];[v]eq=contrast=1.04:saturation=1.03,colorbalance=rs=.015:bs=-.015,subtitles=/tmp/claude-0/previa.ass:fontsdir=/root/.fonts,scale=1280:720[vo];[a]loudnorm=I=-16:TP=-1.5[ao]")
args+=['-filter_complex',';'.join(f),'-map','[vo]','-map','[ao]','-c:v','libx264','-preset','veryfast','-crf','24','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',
 '/home/user/Editor-Videos-Fortunato/dani-carrijo/renders/previa-etapa1-corte-e-legenda.mp4']
subprocess.run(args,check=True)
