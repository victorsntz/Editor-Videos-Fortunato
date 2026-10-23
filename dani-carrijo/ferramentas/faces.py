import cv2, json, subprocess, numpy as np
B='/home/user/Editor-Videos-Fortunato/dani-carrijo/brutos/2026-10-23-dani-youtube'
E=json.load(open('/tmp/claude-0/edl.json'))
cas=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
out={}
for clip in sorted(set(s['clip'] for s in E['segments'])):
    dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'{B}/{clip}.MOV']))
    pts=[]
    for t in np.arange(0.5,dur-0.3,1.0):
        raw=subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',f'{B}/{clip}.MOV','-frames:v','1','-vf','scale=960:540','-f','rawvideo','-pix_fmt','gray','-'],capture_output=True).stdout
        g=np.frombuffer(raw,np.uint8).reshape(540,960)
        f=cas.detectMultiScale(g,1.1,6,minSize=(40,40))
        if len(f):
            x,y,w,h=max(f,key=lambda r:r[2]*r[3]); pts.append((round(t,1),(x+w/2)/960,(y+h/2)/540,w/960))
    out[clip]=pts
    a=np.array([p[1:] for p in pts]); print(clip,len(pts),'med',np.round(np.median(a,0),3),'min',np.round(a.min(0),3),'max',np.round(a.max(0),3))
json.dump(out,open('/tmp/claude-0/faces.json','w'))
