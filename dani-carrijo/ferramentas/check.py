import sys, wave, numpy as np
from faster_whisper import WhisperModel
m=WhisperModel("large-v3",device="cpu",compute_type="int8",cpu_threads=4)
for spec in sys.argv[1:]:
    k,w0,o1,i2,w1=spec.split(','); w0,o1,i2,w1=map(float,(w0,o1,i2,w1))
    w=wave.open(f'/tmp/claude-0/audio/{k}.wav'); a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
    x=np.concatenate([a[int(w0*16000):int(o1*16000)],a[int(i2*16000):int(w1*16000)]])
    segs,_=m.transcribe(x,language='pt',beam_size=5)
    print(spec,'->',' '.join(s.text for s in segs),flush=True)
