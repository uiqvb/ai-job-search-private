"""Look at frames: a labelled contact sheet of any video at chosen times (for agents, which see images).

    python tools/video/peek.py documents/video/<company> <raw file | rough | music | draft path> 12.0 12.4 13.1 ...

Saves pipeline/peek/<source>_<first time>.png (up to 8 frames, 4 per row) and prints its path.
"""

import sys
from pathlib import Path

import cv2
import numpy as np

import vlib


def main(folder, src, times):
    pj = vlib.Project(folder)
    if src == "rough":
        path = pj.path("rough_cut.mp4")
    elif src == "music":
        path = pj.path("rough_cut_music.mp4")
    elif Path(src).exists():
        path = Path(src)
    else:
        path = pj.raw(src)
    if not path.exists():
        sys.exit(f"not found: {path}")
    tiles = []
    for t in times[:8]:
        img = vlib.frame_at(path, t)
        cv2.rectangle(img, (0, 0), (270, 24), (0, 0, 0), -1)
        cv2.putText(img, f"{t:.2f}s", (6, 17), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
        tiles.append(img)
    while len(tiles) % 4:
        tiles.append(np.zeros_like(tiles[0]))
    sheet = np.vstack([np.hstack(tiles[i:i + 4]) for i in range(0, len(tiles), 4)])
    out = pj.path("peek", f"{path.stem[:30]}_{times[0]:.2f}.png")
    out.parent.mkdir(exist_ok=True)
    cv2.imwrite(str(out), sheet)
    print(out)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], [float(x) for x in sys.argv[3:]])
