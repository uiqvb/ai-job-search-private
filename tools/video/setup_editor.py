"""Phase 2, step 0: make (or refresh) the project's Remotion editor from tools/video/kit.

    python tools/video/setup_editor.py documents/video/<company>

Copies the kit's src files (Video.tsx, Root.tsx, index.ts are always refreshed from the kit; Custom.tsx
only if missing, since it holds this video's one-off gags), generates the sound-effect library, and
installs node_modules (copied from another project editor when one has the same Remotion version).
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

import vlib

KIT = Path(__file__).resolve().parent / "kit"
MARK = "Plan-driven intro-video editor (tools/video/kit)"


def main(folder):
    pj = vlib.Project(folder)
    ed = pj.editor
    old = ed / "src" / "Video.tsx"
    if old.exists() and MARK not in old.read_text(encoding="utf-8"):
        sys.exit(f"{ed} holds a hand-made editor (not from the kit); refusing to overwrite it. "
                 'Set "editor" in project.json to another folder, e.g. "pipeline/editor".')
    (ed / "src").mkdir(parents=True, exist_ok=True)
    for sub in ("th", "sfx", "lib"):
        (ed / "public" / sub).mkdir(parents=True, exist_ok=True)
    shutil.copy2(KIT / "package.json", ed / "package.json")
    for f in ("Video.tsx", "Root.tsx", "index.ts"):
        shutil.copy2(KIT / "src" / f, ed / "src" / f)
    if not (ed / "src" / "Custom.tsx").exists():
        shutil.copy2(KIT / "src" / "Custom.tsx", ed / "src" / "Custom.tsx")
    for f, empty in (("plan.json", {"length": 1}), ("words.json", []), ("face_track.json", [])):
        if not (ed / "src" / f).exists():
            (ed / "src" / f).write_text(json.dumps(empty), encoding="utf-8")
    if not any((ed / "public" / "sfx").glob("*.wav")):
        subprocess.run([sys.executable, str(Path(__file__).parent / "make_sfx.py"), str(ed / "public" / "sfx")], check=True)

    want = json.loads((KIT / "package.json").read_text())["dependencies"]["remotion"]
    nm = ed / "node_modules"
    if not (nm / "remotion").exists():
        donor = None
        for other in (vlib.REPO / "documents" / "video").glob("*/editor/node_modules/remotion/package.json"):
            if json.loads(other.read_text(encoding="utf-8")).get("version") == want and other.parents[2] != ed:
                donor = other.parents[1]
                break
        if donor:
            print(f"copying node_modules from {donor.parent.parent.name} (remotion {want}) ...", flush=True)
            r = subprocess.run(["robocopy", str(donor), str(nm), "/E", "/MT:16", "/NFL", "/NDL", "/NJH", "/NJS", "/NP"])
            if r.returncode >= 8:
                sys.exit("robocopy failed")
        else:
            print("npm install ...", flush=True)
            subprocess.run("npm install --no-audit --no-fund", cwd=ed, shell=True, check=True)
    print(f"ok editor ready: {ed}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
