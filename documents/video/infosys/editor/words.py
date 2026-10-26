"""Word timings of the rough cut -> src/words.json (for captions and effect timing)."""
import json, os
from faster_whisper import WhisperModel
HERE = os.path.dirname(os.path.abspath(__file__))
m = WhisperModel("medium", device="cpu", compute_type="int8")
segs, _ = m.transcribe(os.path.join(HERE, "..", "transcripts", "rough.wav"), language="en", word_timestamps=True,
    initial_prompt="Okay Infosys, at the Australian Open you brought a robot to the Fan Zone. MatchFeel. InStep. I haven't trained an ML model yet. Manit Khera. Deakin Open Day.")
W = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)} for s in segs for w in s.words]
json.dump(W, open(os.path.join(HERE, "src", "words.json"), "w"), indent=0)
print(" ".join(f"{x['w']}@{x['s']}" for x in W))
