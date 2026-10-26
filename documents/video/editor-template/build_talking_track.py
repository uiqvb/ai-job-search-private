"""Joins the chosen talking-head pieces into ONE continuous file (public/th/track.mp4),
cut exactly where timeline.json says, with 2-frame audio fades at each join.
The editor plays this single file, so there are no gaps or load delays between takes."""
import json, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, "src", "timeline.json")))
fps = d["fps"]
f = lambda s: round(s * fps)
inputs, chains, labels = [], [], []
for i, p in enumerate(d["pieces"]):
    n = f(p["start"] + p["dur"]) - f(p["start"])          # exact frame count the timeline expects
    dur = n / fps
    fade = 2 / fps
    inputs += ["-ss", f"{p['from']:.3f}", "-t", f"{dur + 0.5:.3f}", "-i", os.path.join(HERE, "public", p["src"])]
    chains.append(f"[{i}:v]trim=end_frame={n},setpts=PTS-STARTPTS[v{i}];"
                  f"[{i}:a]atrim=duration={dur:.4f},asetpts=PTS-STARTPTS,"
                  f"afade=t=in:d={fade:.4f},afade=t=out:st={dur - fade:.4f}:d={fade:.4f}[a{i}]")
    labels.append(f"[v{i}][a{i}]")
fc = ";".join(chains) + ";" + "".join(labels) + f"concat=n={len(labels)}:v=1:a=1[v][a]"
out = os.path.join(HERE, "public", "th", "track.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                "-r", str(fps), "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-g", "15", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
print("ok", out)
