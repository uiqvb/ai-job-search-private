"""Head position (x/y centroid of dark hair/face pixels) around each cut, vs. its settled
position while he is talking. A big offset at the start of a cut = still turning from the script."""
import json, os, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
BX, BY, BW, BH = 100, 120, 280, 330

def frames(path, a, b):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(0,a):.3f}", "-t", f"{b - a:.3f}", "-i", path,
                          "-vf", f"crop={BW}:{BH}:{BX}:{BY},scale=70:82,format=gray", "-f", "rawvideo", "-"],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, 82, 70).astype(np.float32)

def pos(fr):
    out = []
    ys, xs = np.mgrid[0:82, 0:70]
    for f in fr:
        m = f < 70          # hair, glasses, shirt edge
        if m.sum() < 20: out.append((np.nan, np.nan)); continue
        out.append((xs[m].mean(), ys[m].mean()))
    return np.array(out)

if __name__ == "__main__":
    cuts = json.load(open(os.path.join(HERE, "cut_list.json")))
    for i, c in enumerate(cuts):
        p = os.path.join(HERE, "Raw Takes", c["file"])
        ref = np.nanmedian(pos(frames(p, c["in"] + 0.8, c["out"] - 0.4)), axis=0)
        a = c["in"] - 1.0
        P = pos(frames(p, a, c["in"] + 1.5))
        dev = np.hypot(*(P - ref).T)
        s = "".join(" .:-=+*#%@"[min(9, int(v / 0.5))] if v == v else "?" for v in dev)
        print(f"#{i:2} {c['at']:6.1f}s |{s[:30]}[{s[30:]}|")
