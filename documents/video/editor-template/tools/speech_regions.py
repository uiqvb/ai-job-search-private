"""List speech regions (from silencedetect) per raw take, and flag ones with no transcribed words."""
import glob, json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
files = sorted(glob.glob(os.path.join(HERE, "Raw Takes", "*.mp4")))
for i, f in enumerate(files):
    if str(i) not in sys.argv[1:]: continue
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", f, "-af", "silencedetect=noise=-35dB:d=0.6", "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    en = [0.0] + [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    words = json.load(open(os.path.join(HERE, "transcripts", f"raw{i}.json")))["words"]
    print("== raw", i)
    for a, b in zip(en, st + [9999]):
        if b - a < 0.4: continue
        ws = [w["w"] for w in words if a - 0.3 <= w["s"] <= b]
        print(f"{a:7.2f}-{min(b,9999):7.2f}  {'' if ws else '*** NO WORDS'} {''.join(ws)[:90]}")
