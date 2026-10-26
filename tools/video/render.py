"""Phase 2: render a short draft of the changed section, or the final.

    python tools/video/render.py documents/video/<company> draft 12.0 20.5 "robot rises"
    python tools/video/render.py documents/video/<company> draft all
    python tools/video/render.py documents/video/<company> final

Runs build_plan.py first, so the editor always matches pipeline/plan.json.
Drafts: <project>/Drafts/<Company> - Draft N - <a> to <b> (<note>).mp4 (short drafts render in under a minute;
Remotion Studio stutters on the laptop). Final: <project>/Final/Manit Khera - <Company> Intro (Final).mp4,
with any older final moved to Final/Old Versions/. Prints loudness (integrated LUFS, true peak) after.
"""

import re
import shutil
import subprocess
import sys

import vlib


def loudness(path):
    err = vlib.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", err)
    p = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", err)
    return (float(i[-1]) if i else None), (float(p[-1]) if p else None)


def main(folder, mode, args):
    pj = vlib.Project(folder)
    r = subprocess.run([sys.executable, str(vlib.Path(__file__).parent / "build_plan.py"), str(pj.dir)])
    if r.returncode:
        sys.exit("plan has errors; fix pipeline/plan.json first")
    length = pj.read_json("cut_list.json")["length"]
    total = round(length * 30)
    if mode == "final":
        out_dir = pj.dir / "Final"
        out_dir.mkdir(exist_ok=True)
        out = out_dir / f"Manit Khera - {pj.name} Intro (Final).mp4"
        if out.exists():
            (out_dir / "Old Versions").mkdir(exist_ok=True)
            shutil.move(str(out), str(out_dir / "Old Versions" / out.name.replace("(Final)", "(Final, old)")))
        frames = None
    else:
        out_dir = pj.dir / "Drafts"
        out_dir.mkdir(exist_ok=True)
        n = 1 + max([int(m.group(1)) for f in out_dir.glob("*.mp4") if (m := re.search(r"Draft (\d+)", f.name))] or [0])
        if args and args[0] == "all":
            a, b, note = 0.0, length, " ".join(args[1:])
            frames = None
        else:
            a, b = float(args[0]), float(args[1])
            note = " ".join(args[2:])
            frames = f"{max(0, round(a * 30))}-{min(total - 1, round(b * 30))}"
        name = f"{pj.name} - Draft {n} - {a:.2f} to {b:.2f}" + (f" ({note})" if note else "") + ".mp4"
        out = out_dir / re.sub(r'[<>:"/\\|?*]', "", name)
    cmd = f'npx remotion render src/index.ts Intro "{out}" --crf=18 --log=error'
    if frames:
        cmd += f" --frames={frames}"
    print(cmd, flush=True)
    r = subprocess.run(cmd, cwd=pj.editor, shell=True)
    if r.returncode:
        sys.exit("render failed")
    lufs, peak = loudness(out)
    flag = "" if peak is None or peak <= -0.5 else "  (peak too hot: turn down the loudest sound effect)"
    print(f"ok {out}\nloudness {lufs} LUFS, true peak {peak} dBFS{flag}")


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[2] not in ("draft", "final"):
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
