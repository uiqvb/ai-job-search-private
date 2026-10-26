"""Head-movement profile around each cut (mean abs frame difference over the head area).
Used to start cuts after he has turned back from the script."""
import json, os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 60, 66   # head box 200x220 at (140,170) in the 478x850 source, downscaled

def motion(path, a, b):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", path,
                          "-vf", f"crop=200:220:140:170,scale={W}:{H},format=gray", "-f", "rawvideo", "-"],
                         capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)
    d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))
    return [(a + (k + 1) / 30, v) for k, v in enumerate(d)]

if __name__ == "__main__":
    cuts = json.load(open(os.path.join(HERE, "cut_list.json")))
    for i, c in enumerate(cuts):
        p = os.path.join(HERE, "Raw Takes", c["file"])
        m = motion(p, c["in"] - 1.0, c["in"] + 1.2)
        s = "".join(" .:-=+*#%@"[min(9, int(v / 0.6))] for t, v in m)
        e = motion(p, c["out"] - 0.8, c["out"] + 0.5)
        s2 = "".join(" .:-=+*#%@"[min(9, int(v / 0.6))] for t, v in e)
        print(f"#{i:2} {c['at']:6.1f}s in  |{s[:30]}[{s[30:]}|   out |{s2[:24]}]{s2[24:]}|")
