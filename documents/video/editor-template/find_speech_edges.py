"""Finds where speech actually starts and stops in each take, from the audio (not the transcript).
Writes transcripts/edges.json, which build_timeline.py uses to cut each take tightly."""
import json, os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "build_timeline.py")).read()
ns = {"__file__": os.path.join(HERE, "build_timeline.py")}
exec(src.split("pieces, words_out")[0], ns)
edges = {}
for raw in ns["SECTIONS"]:
    sid, ranges, _ = ns["norm"](raw)
    w = [x for x in ns["load_words"](sid) if any(a <= x["s"] < b for a, b in ranges)]
    first, last = w[0]["s"], w[-1]["e"]
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", os.path.join(HERE, "public", "th", f"{sid}.mp4"),
                          "-af", "silencedetect=noise=-38dB:d=0.12", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    sil = list(zip(starts, ends + [9999] * (len(starts) - len(ends))))
    # speech onset: end of the silence that covers (or ends just after) the first word's timestamp
    onset = first
    for a, b in sil:
        if a <= first + 0.3 and b >= first - 0.6 and b <= first + 0.6:
            onset = b
    # speech offset: start of the silence that begins around the last word's end
    offset = last
    cands = [a for a, b in sil if last - 0.6 <= a <= last + 0.8]
    if cands:
        offset = min(cands, key=lambda a: abs(a - last))
    edges[sid] = {"onset": round(onset, 3), "offset": round(offset, 3), "word_first": first, "word_last": last}
    print(f"{sid:>3}  speech {onset:6.2f} -> {offset:6.2f}   (transcript said {first:6.2f} -> {last:6.2f})")
json.dump(edges, open(os.path.join(HERE, "transcripts", "edges.json"), "w"), indent=1)
