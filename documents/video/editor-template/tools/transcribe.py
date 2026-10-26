"""Transcribe the raw take with word timestamps -> transcripts/raw0.json and raw0.txt."""
import json, os
from faster_whisper import WhisperModel
HERE = os.path.dirname(os.path.abspath(__file__))
m = WhisperModel("medium", device="cpu", compute_type="int8")
src = os.path.join(HERE, "transcripts", "raw0.wav")
segs, _ = m.transcribe(src, language="en", word_timestamps=True, vad_filter=False,
                       initial_prompt="Syncrowin, Deakin, Open Day, Manit Khera, Claude Code, API, backend.")
words, lines = [], []
for s in segs:
    lines.append(f"[{s.start:7.2f}-{s.end:7.2f}] {s.text.strip()}")
    for w in s.words:
        words.append({"w": w.word, "s": round(w.start, 3), "e": round(w.end, 3)})
    print(lines[-1], flush=True)
json.dump({"file": "20261022_102801.mp4", "words": words}, open(os.path.join(HERE, "transcripts", "raw0.json"), "w"), indent=0)
open(os.path.join(HERE, "transcripts", "raw0.txt"), "w", encoding="utf-8").write("\n".join(lines))
print("DONE")
