"""Phase 1: cut the Infosys long take (7:20) into the talking track, no effects. Last clean take of each line."""
import json, os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "Raw Takes", "20261022_210409.mp4")
LEAD, TAIL = 0.06, 0.15
GRADE = "huesaturation=hue=0:saturation=-0.45:colors=b+c,colortemperature=temperature=4700:mix=0.75,eq=gamma=1.08:contrast=0.95:saturation=0.95,colorbalance=rh=0.04:gh=0.02:bh=-0.04"  # warm 'sunny' look, option B (Manit, 22 Oct)
END_HOLD = 2.0
PIECES = [
    ("1 Hook",       49.30,  52.34, True,  "Okay, Infosys, at the Australian Open, you brought a robot to the Fan Zone."),
    ("2 Open Day",   80.80,  83.00, True,  "I too brought mine to the Deakin Open Day."),
    ("3 Meet",      192.60, 201.30, "in",  "Two separate uni projects, an API and a robot. Nobody said they should meet, but I still made them meet. [hands up, look up]"),
    ("4 Chair",     230.80, 236.00, "in",  "My unit chair warned me that I might not finish neither, and for a month he was right. [straight face]"),
    ("5 Worked",    244.50, 248.88, True,  "Then it worked. 100 out of 100, and it got picked for Deakin's Open Day."),
    ("6 MatchFeel", 275.95, 281.39, True,  "That's why MatchFeel got to me. No one expects to follow tennis by touch. You built it anyways."),
    ("7 Robot",     327.30, 331.68, True,  "Same with my robot. Nobody asked me to build it, but I still built it anyway."),
    ("8 InStep",    381.72, 385.49, True,  "That's the work I want at InStep. AI and robots that leave the screen. (restart only; first attempt at 378.3 dropped)"),
    ("9 ML gap",    413.43, 418.17, True,  "I haven't trained a machine learning model yet, but that's what I want to learn from InStep and its mentors."),
    ("10 Close",    426.08, 431.81, True,  "So yeah, I'm Manit Khera and I usually end up doing more than what is asked of me. Thank you so much for watching."),
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
    chains.append(f"[{i}:v]scale=1080:1920:flags=lanczos,setsar=1,"
                  f"{GRADE},fps=30,setpts=PTS-STARTPTS[v{i}];"
                  f"[{i}:a]aresample=48000,asetpts=PTS-STARTPTS,afade=t=in:d={fade},"
                  f"afade=t=out:st={d - fade:.3f}:d={fade}[a{i}]")
fc = ";".join(chains) + ";" + "".join(f"[v{i}][a{i}]" for i in range(len(cuts))) + \
     f"concat=n={len(cuts)}:v=1:a=1[v][ac];[ac]loudnorm=I=-16:TP=-1.5:LRA=11[a]"
os.makedirs(os.path.join(HERE, "Rough Cut"), exist_ok=True)
out = os.path.join(HERE, "Rough Cut", "Infosys - Rough Cut.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out], check=True)
print(f"ok {out}  ({t:.1f} s)")
