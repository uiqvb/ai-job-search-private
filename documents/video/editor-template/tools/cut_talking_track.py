"""Phase 1: cut the one long take into the talking track (no effects).

PIECES = (section, rough in, rough out, snap?, what is said). Times are in the raw take
(Raw Takes/20261022_102801.mp4, 8 min, one continuous take). With snap=True the in/out are moved
to the real speech edges (silencedetect) and padded; snap=False keeps hand-set times (checked frame
by frame: toss freeze, palm/fist hold).
Output: Rough Cut/Syncrowin - Rough Cut.mp4 (1080x1920, 30 fps) + cut_list.json.
"""
import json, os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "Raw Takes", "20261022_102801.mp4")
LEAD, TAIL = 0.06, 0.15
END_HOLD = 2.0
PIECES = [
    ("1 Hook",    30.40,  33.50, True,  "Syncrowin, give me one minute and I'll tell you why you should hire me."),
    ("2 Reel+toss", 69.60, 83.75, "in", "I got 100/100 in my backend unit. ...Open Day... 5,000 simulated robots... six times faster, but you don't want to hear that. [toss, freeze]"),
    ("3 Startup", 123.10, 129.00, True,  "You're a startup... curious... energy... experiments, and that's exactly me."),
    ("4 What if", 206.10, 212.95, True,  "I can't leave a what-if alone... It usually breaks, but that's the fun part."),
    ("5 Hats",    324.90, 336.20, True,  "In a small team... backend guy, hardware guy, IT support guy, and today I'm the video guy."),
    ("6 Reveal",  374.40, 379.10, True,  "Because this whole video has been made just using Claude Code and with AI."),
    ("7 Fire",    432.20, 440.40, "in",  "And it can do things a camera cannot, like this. [palm] Imagine that for Syncrowin. [fist]"),
    ("8 Close",   465.50, 469.90, True,  "I'm Manit Khera. Give me a what if and I'll go and find out. Thanks for watching."),
]


def silences(a, b):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", SRC, "-vn",
                          "-af", "silencedetect=noise=-38dB:d=0.12", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    st = [a + float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", err)]
    en = [a + float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    if len(en) < len(st):
        en.append(b)
    return list(zip(st, en))


def snap(s, e):
    sil = silences(max(0, s - 1.0), e + 1.0)
    before = [b for a, b in sil if b <= s + 0.6]
    after = [a for a, b in sil if a >= e - 0.4]
    return (max(before) if before else s), (min(after) if after else e)


cuts, t = [], 0.0
for i, (sec, s, e, mode, text) in enumerate(PIECES):
    if mode is True:
        on, off = snap(s, e)
        src_in, src_out = max(0, on - LEAD), off + TAIL
    elif mode == "in":                       # snap only the start, keep the hand-set end
        on, _ = snap(s, s + 1.0)
        src_in, src_out = max(0, on - LEAD), e
    else:
        src_in, src_out = s, e
    if i == len(PIECES) - 1:
        src_out += END_HOLD
    cuts.append({"section": sec, "in": round(src_in, 3), "out": round(src_out, 3), "at": round(t, 3), "text": text})
    print(f"{t:6.2f}  {sec:<12} {src_in:7.2f}-{src_out:7.2f}  ({src_out - src_in:4.1f}s)  {text[:55]}")
    t += src_out - src_in

json.dump(cuts, open(os.path.join(HERE, "cut_list.json"), "w"), indent=1)
inputs, chains, fade = [], [], 0.03
for i, c in enumerate(cuts):
    d = c["out"] - c["in"]
    inputs += ["-ss", f"{c['in']:.3f}", "-t", f"{d:.3f}", "-i", SRC]
    chains.append(f"[{i}:v]scale=1080:1920:flags=lanczos,setsar=1,fps=30,setpts=PTS-STARTPTS[v{i}];"
                  f"[{i}:a]aresample=48000,asetpts=PTS-STARTPTS,afade=t=in:d={fade},"
                  f"afade=t=out:st={d - fade:.3f}:d={fade}[a{i}]")
fc = ";".join(chains) + ";" + "".join(f"[v{i}][a{i}]" for i in range(len(cuts))) + \
     f"concat=n={len(cuts)}:v=1:a=1[v][ac];[ac]loudnorm=I=-16:TP=-1.5:LRA=11[a]"
os.makedirs(os.path.join(HERE, "Rough Cut"), exist_ok=True)
out = os.path.join(HERE, "Rough Cut", "Syncrowin - Rough Cut.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out], check=True)
print(f"ok {out}  ({t:.1f} s)")
