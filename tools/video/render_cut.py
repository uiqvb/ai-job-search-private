"""Phase 1, step 2: render the rough cut from the cutter's picks.

    python tools/video/render_cut.py documents/video/<company> [--fast]

Reads pipeline/cuts.json (written by the video-cutter agent):
  {"pieces": [{"line": "1 Hook", "file": "take.mp4", "in": 49.30, "out": 52.34,
               "snap": "both" | "in" | "out" | "none", "why": "last clean take"}]}

`in`/`out` are rough (word timings). Unless snap says otherwise, each edge is moved to where
speech really starts/ends, measured on the audio level (not silencedetect, which snapped too early
on digitally silent takes in the Capgemini cut), then padded by LEAD/TAIL.
Writes pipeline/cut_list.json (the exact times used) and pipeline/rough_cut.mp4.
"""

import sys

import numpy as np

import vlib

LEAD, TAIL = 0.06, 0.15      # padding before the first word / after the last (s)
SEARCH = 0.5                 # how far an edge may move while snapping (s)
FADE = 0.03                  # audio fade at each join (s)


def snap_edge(env, thr, t, start):
    """Move an edge to the true speech onset (start=True) or offset (start=False)."""
    i = int(round(t / vlib.HOP))
    i = min(max(i, 0), len(env) - 1)
    steps = int(SEARCH / vlib.HOP)
    quiet = int(0.08 / vlib.HOP) if start else int(0.12 / vlib.HOP)
    loud = lambda k: 0 <= k < len(env) and env[k] > thr
    if start:
        if loud(i):     # cut lands inside speech: walk back to the silence before it
            k = i
            while k > i - steps and any(loud(k - j) for j in range(1, quiet + 1)):
                k -= 1
            return k * vlib.HOP
        for k in range(i, min(len(env), i + steps)):   # cut lands in silence: walk forward to the first sound
            if all(loud(k + j) for j in range(3)):
                return k * vlib.HOP
        return t
    if loud(i):         # walk forward until it has been quiet for a while
        k = i
        while k < i + steps and any(loud(k + j) for j in range(1, quiet + 1)):
            k += 1
        return (k + 1) * vlib.HOP
    for k in range(i, max(0, i - steps), -1):          # walk back to the last sound
        if all(loud(k - j) for j in range(3)):
            return (k + 1) * vlib.HOP
    return t


def main(folder, fast=False):
    pj = vlib.Project(folder)
    pieces = pj.read_json("cuts.json")["pieces"]
    grade = pj.cfg.get("grade")
    end_hold = float(pj.cfg.get("end_hold", 2.0))
    envs, thrs = {}, {}
    cuts, at = [], 0.0
    for k, p in enumerate(pieces):
        f = p["file"]
        if f not in envs:
            envs[f] = vlib.rms_db(vlib.audio(pj.raw(f)))
            thrs[f] = vlib.speech_threshold(envs[f])
        snap = p.get("snap", "both")
        s, e = float(p["in"]), float(p["out"])
        if snap in ("both", "in"):
            s = snap_edge(envs[f], thrs[f], s, True) - LEAD
        if snap in ("both", "out"):
            e = snap_edge(envs[f], thrs[f], e, False) + TAIL
        if k == len(pieces) - 1:
            e += end_hold
        s = max(0.0, s)
        cuts.append({"line": p["line"], "file": f, "in": round(s, 3), "out": round(e, 3), "at": round(at, 3),
                     "moved_in": round(s - float(p["in"]), 2), "moved_out": round(e - float(p["out"]), 2)})
        print(f"{at:6.2f}  {p['line']:<14} {s:8.2f}-{e:8.2f}  ({e - s:4.1f}s)  snap moved {s - float(p['in']):+.2f} / {e - float(p['out']):+.2f}")
        at += e - s

    inputs, chains = [], []
    vf_grade = f"{grade}," if grade else ""
    for i, c in enumerate(cuts):
        d = c["out"] - c["in"]
        inputs += ["-ss", f"{c['in']:.3f}", "-t", f"{d:.3f}", "-i", str(pj.raw(c["file"]))]
        chains.append(f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1,"
                      f"{vf_grade}fps=30,setpts=PTS-STARTPTS[v{i}];"
                      f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,asetpts=PTS-STARTPTS,afade=t=in:d={FADE},"
                      f"afade=t=out:st={max(0, d - FADE):.3f}:d={FADE}[a{i}]")
    fc = ";".join(chains) + ";" + "".join(f"[v{i}][a{i}]" for i in range(len(cuts))) + \
        f"concat=n={len(cuts)}:v=1:a=1[v][ac];[ac]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[a]"
    out = pj.path("rough_cut.mp4")
    r = vlib.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                  "-c:v", "libx264", "-preset", "veryfast" if fast else "medium", "-crf", "20" if fast else "18",
                  "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)])
    if r.returncode:
        sys.exit("ffmpeg failed:\n" + r.stderr[-2000:])
    pj.write_json({"length": round(at, 3), "pieces": cuts}, "cut_list.json")
    print(f"ok {out}  ({at:.1f} s, {len(cuts)} pieces)")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        sys.exit(__doc__)
    main(args[0], fast="--fast" in sys.argv)
