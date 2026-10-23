import json, glob, os, sys, wave
import numpy as np
from faster_whisper import WhisperModel
m = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=4)
out = {}
for f in sorted(glob.glob("/tmp/claude-0/audio/*.wav")):
    n = os.path.basename(f)[:-4]
    w_=wave.open(f); a_=np.frombuffer(w_.readframes(w_.getnframes()),dtype=np.int16).astype(np.float32)/32768
    segs, info = m.transcribe(a_, language="pt", word_timestamps=True, vad_filter=False, beam_size=5,
                              initial_prompt="Dani Carrijo, terapeuta capilar. Tricoscopia, couro cabeludo, queda capilar, raiz.")
    out[n] = [{"start": s.start, "end": s.end, "text": s.text,
               "words": [{"w": w.word, "s": w.start, "e": w.end, "p": w.probability} for w in s.words]} for s in segs]
    print(n, " ".join(s["text"] for s in out[n]), flush=True)
json.dump(out, open("/tmp/claude-0/transcript.json", "w"), ensure_ascii=False, indent=1)
