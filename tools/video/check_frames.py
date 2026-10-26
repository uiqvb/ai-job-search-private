"""Phase 2, step 4: frame sheets + automatic checks of a rendered draft, for the visual-reviewer agent.

    python tools/video/check_frames.py documents/video/<company> "<draft or final .mp4>" [--start 12.0]

--start = the cut time the draft begins at (render.py names drafts "Draft N - <a> to <b>", read from the name
if omitted). Samples a frame just after every planned event starts and in its middle, plus every 2 s, and
saves labelled sheets (8 frames each) to pipeline/review/visual_<draft>/. Automatic checks:
black corners (a zoom or tilt showing the edge of the frame), frames gone black, true peak and loudness.
"""

import json
import re
import sys
from pathlib import Path

import cv2
import numpy as np

import render
import vlib

FW, FH = 270, 480


def main(folder, video, start):
    pj = vlib.Project(folder)
    video = Path(video)
    plan = json.loads((pj.editor / "src" / "plan.json").read_text(encoding="utf-8"))
    dur = vlib.probe(video)["duration"]
    a, b = start, start + dur
    events = []
    for key in ("zooms", "follow", "bw", "broll", "texts", "stickers"):
        for x in plan.get(key, []):
            label = f"{key[:-1] if key.endswith('s') else key} {x.get('txt', Path(x.get('src', '')).stem)}".strip()
            events += [(x["from"] + 0.1, label + " start"), ((x["from"] + x["to"]) / 2, label + " mid")]
    for key in ("nametag", "endcard"):
        if plan.get(key):
            events.append((plan[key]["from"] + 0.15, key))
    events += [(t, "") for t in np.arange(a + 1.0, b, 2.0)]
    events = sorted({round(t, 2): l for t, l in events if a <= t < b - 0.05}.items())
    endcard = plan.get("endcard", {}).get("from", 1e9)

    outdir = pj.path("review", "visual_" + re.sub(r"\W+", "_", video.stem)[:40])
    outdir.mkdir(parents=True, exist_ok=True)
    issues, tiles = [], []
    for t, label in events:
        big = vlib.frame_at(video, t - a, 540, 960)
        g = cv2.cvtColor(big, cv2.COLOR_BGR2GRAY)
        if g.mean() < 6 and t < endcard:
            issues.append(f"{t:.2f}s: frame is black")
        corners = [g[:12, :12], g[:12, -12:], g[-12:, :12], g[-12:, -12:]]
        dark = sum(1 for c in corners if c.mean() < 4)
        if dark and t < endcard and g.mean() > 25:
            issues.append(f"{t:.2f}s: {dark} black corner(s), a zoom or tilt shows the frame edge ({label or 'between events'})")
        img = cv2.resize(big, (FW, FH))
        cv2.rectangle(img, (0, 0), (FW, 22), (0, 0, 0), -1)
        cv2.putText(img, f"{t:.2f}s {label}"[:34], (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 1)
        tiles.append(img)
    sheets = []
    for i in range(0, len(tiles), 8):
        group = tiles[i:i + 8] + [np.zeros((FH, FW, 3), np.uint8)] * (8 - len(tiles[i:i + 8]))
        sheet = np.vstack([np.hstack(group[:4]), np.hstack(group[4:])])
        name = outdir / f"sheet_{i // 8 + 1:02d}.png"
        cv2.imwrite(str(name), sheet)
        sheets.append(name)
    lufs, peak = render.loudness(video)
    if peak is not None and peak > -0.5:
        issues.append(f"true peak {peak} dBFS: a sound effect is clipping; turn the loudest one down")
    md = [f"# Visual check: {video.name}", "", f"Cut time {a:.2f}-{b:.2f}s. Loudness {lufs} LUFS, true peak {peak} dBFS.", ""]
    md += [f"- **{x}**" for x in issues] or ["- no automatic issues"]
    md += ["", "Frame sheets (8 frames each, time and planned event on every frame):"] + [f"- {s}" for s in sheets]
    md += ["", "Plan check: pipeline/plan_check.md"]
    (outdir / "report.md").write_text("\n".join(md), encoding="utf-8")
    print(f"ok {len(events)} frames, {len(issues)} issue(s) -> {outdir / 'report.md'}")


if __name__ == "__main__":
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    st = None
    if "--start" in sys.argv:
        st = float(sys.argv[sys.argv.index("--start") + 1])
        args = [x for x in args if x != sys.argv[sys.argv.index("--start") + 1]]
    if len(args) != 2:
        sys.exit(__doc__)
    if st is None:
        m = re.search(r" - ([\d.]+) to ([\d.]+)", Path(args[1]).name)
        st = float(m.group(1)) if m else 0.0
    main(args[0], args[1], st)
