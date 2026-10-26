"""Phase 2, step 2: turn the planner's pipeline/plan.json into the editor's src/plan.json, and check it.

    python tools/video/build_plan.py documents/video/<company>

The planner writes times as word anchors so a re-cut never breaks the plan:
  number (seconds) | {"word": "right", "n": 1, "edge": "s"|"e", "offset": 0.1} | "@name" or "@name+0.2"
  ("@name" refers to the plan's "anchors": {"name": <anchor>} block).
Media paths are relative to documents/video/ (e.g. "broll/cuts/openday.mp4"), or "project:img/x.png" for
this project's own files; they are copied into editor/public/lib/.
"echo": [{"id": "right", "word": {...}, "vol": 0.75}] makes a wet-only echo tail of that word (EDITING-STYLE rule).
Also refreshes editor/public/th/track.mp4 (the rough cut, no music), src/words.json and src/face_track.json.
Writes pipeline/plan_check.md with rule warnings (text on his face, captions over his face, overlaps, missing files).
"""

import json
import re
import shutil
import sys

import cv2
import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as sg

import vlib

LIB = vlib.REPO / "documents" / "video"
SPAN_KEYS = ("zooms", "follow", "bw", "broll", "texts", "stickers")


class Resolver:
    def __init__(self, words, anchors):
        self.words, self.named = words, {}
        for k, v in (anchors or {}).items():
            self.named[k] = self(v)

    def __call__(self, v):
        if isinstance(v, str):
            m = re.fullmatch(r"@([\w-]+)\s*([+-]\s*[\d.]+)?", v.strip())
            if not m or m.group(1) not in self.named:
                raise ValueError(f"unknown anchor {v!r}")
            return round(self.named[m.group(1)] + float((m.group(2) or "0").replace(" ", "")), 3)
        return vlib.resolve(v, self.words)


def face_track(track, out):
    stamp = f"{track.stat().st_size}-{int(track.stat().st_mtime)}"
    meta = out.with_suffix(".stamp")
    if out.exists() and meta.exists() and meta.read_text() == stamp:
        return json.loads(out.read_text())
    casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(str(track))
    rows, i, last = [], 0, None
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        if i % 3 == 0:
            g = cv2.cvtColor(cv2.resize(fr, (540, 960)), cv2.COLOR_BGR2GRAY)
            f = casc.detectMultiScale(g, 1.1, 5, minSize=(90, 90))
            if len(f):
                x, y, w, h = max(f, key=lambda r: r[2])
                last = [(x + w / 2) * 2, (y + h / 2) * 2, w * 2]
            if last:
                rows.append([round(i / 30, 3)] + [round(v, 1) for v in last])
        i += 1
    a = np.array(rows) if rows else np.zeros((0, 4))
    for c in (1, 2, 3):
        if len(a) > 5:
            a[:, c] = np.convolve(np.pad(a[:, c], 2, mode="edge"), np.ones(5) / 5, "valid")
    data = [[round(v, 2) for v in r] for r in a.tolist()]
    out.write_text(json.dumps(data))
    meta.write_text(stamp)
    return data


def face_at(track, t):
    if not track:
        return (540, 860, 380)
    for a, b in zip(track, track[1:]):
        if a[0] <= t <= b[0]:
            return tuple(a[1:])
    return tuple(track[-1][1:])


def echo_tail(track, s, e, out):
    """Wet-only reverb + three slap echoes of one word (the dry word stays in the voice track)."""
    SR = 48000
    w = vlib.audio(track, start=s, dur=e - s, sr=SR).astype(float)
    rng = np.random.default_rng(11)
    t = np.arange(int(3.0 * SR)) / SR
    b, a = sg.butter(2, 5000 / (SR / 2))
    ir = sg.lfilter(b, a, rng.standard_normal(len(t)) * np.exp(-t * 1.9))
    wet = sg.fftconvolve(w, ir)[: int(3.2 * SR)]
    slap = np.zeros(int(3.2 * SR))
    for dt, g in ((0.22, 0.55), (0.44, 0.32), (0.66, 0.18)):
        i = int(dt * SR)
        slap[i:i + len(w)] += w[: len(slap) - i] * g
    y = wet / (np.max(np.abs(wet)) + 1e-9) * 0.6 + slap
    y = y / (np.max(np.abs(y)) + 1e-9) * 0.75
    f = int(0.004 * SR)
    y[-f:] *= np.linspace(1, 0, f)
    wav.write(str(out), SR, (y * 32767).astype(np.int16))


def main(folder):
    pj = vlib.Project(folder)
    ed = pj.editor
    if not (ed / "src" / "Video.tsx").exists():
        sys.exit("no editor yet: run tools/video/setup_editor.py first")
    plan = pj.read_json("plan.json")
    words = pj.read_json("rough_words.json")["words"]
    length = pj.read_json("cut_list.json")["length"]
    warns, errs = [], []

    # track, words, face
    track = ed / "public" / "th" / "track.mp4"
    src = pj.path("rough_cut.mp4")
    if not track.exists() or track.stat().st_size != src.stat().st_size or track.stat().st_mtime < src.stat().st_mtime:
        shutil.copy2(src, track)
    (ed / "src" / "words.json").write_text(json.dumps([{"w": w["w"], "s": w["s"], "e": w["e"]} for w in words], indent=0))
    ft = face_track(track, ed / "src" / "face_track.json")

    R = Resolver(words, plan.get("anchors"))
    out = {"length": round(length, 3), "anchors": R.named}

    def T(v, where):
        try:
            x = R(v)
        except ValueError as e:
            errs.append(f"{where}: {e}")
            return 0.0
        if not 0 <= x <= length + 0.01:
            errs.append(f"{where}: time {x:.2f}s is outside the cut (0-{length:.2f})")
        return x

    def media(p, where):
        path = pj.dir / p[len("project:"):] if p.startswith("project:") else LIB / p
        if not path.exists():
            errs.append(f"{where}: file not found: {path}")
            return p
        rel = ("project/" + p[len("project:"):]) if p.startswith("project:") else p
        dst = ed / "public" / "lib" / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists() or dst.stat().st_size != path.stat().st_size:
            shutil.copy2(path, dst)
        return "lib/" + rel.replace("\\", "/")

    for key in SPAN_KEYS:
        items = []
        for k, it in enumerate(plan.get(key, [])):
            it = dict(it)
            it["from"], it["to"] = T(it["from"], f"{key}[{k}].from"), T(it["to"], f"{key}[{k}].to")
            if it["to"] <= it["from"]:
                errs.append(f"{key}[{k}]: ends before it starts ({it['from']:.2f}-{it['to']:.2f})")
            if "src" in it:
                it["src"] = media(it["src"], f"{key}[{k}]")
            items.append(it)
        out[key] = items
    out["shakes"] = [{**s, "at": T(s["at"], f"shakes[{k}]")} for k, s in enumerate(plan.get("shakes", []))]
    out["bursts"] = [{**b, "at": T(b["at"], f"bursts[{k}]")} for k, b in enumerate(plan.get("bursts", []))]
    sfx = [{**s, "at": T(s["at"], f"sfx[{k}]")} for k, s in enumerate(plan.get("sfx", []))]
    for k, s in enumerate(sfx):
        if not (ed / "public" / "sfx" / f"{s['name']}.wav").exists():
            errs.append(f"sfx[{k}]: no sound named {s['name']!r} in editor/public/sfx")
    for k, e in enumerate(plan.get("echo", [])):
        spec = dict(e["word"]) if isinstance(e["word"], dict) else {"word": e["word"]}
        try:
            s0 = vlib.resolve({**spec, "edge": "s"}, words)
            s1 = vlib.resolve({**spec, "edge": "e"}, words)
        except ValueError as x:
            errs.append(f"echo[{k}]: {x}")
            continue
        name = f"echo_{e.get('id', k)}"
        echo_tail(track, s0 - 0.03, s1 + 0.05, ed / "public" / "sfx" / f"{name}.wav")
        sfx.append({"name": name, "at": round(s0, 3), "vol": e.get("vol", 0.75)})
    out["sfx"] = sorted(sfx, key=lambda s: s["at"])

    cap = dict(plan.get("captions", {"on": True}))
    cap["lift"] = [{**l, "from": T(l["from"], f"captions.lift[{k}]"), "to": T(l["to"], f"captions.lift[{k}]")}
                   for k, l in enumerate(cap.get("lift", []))]
    out["captions"] = cap
    ec = pj.cfg.get("end_card", {})
    if "nametag" in plan:
        n = plan["nametag"]
        out["nametag"] = {"from": T(n["from"], "nametag.from"), "to": T(n["to"], "nametag.to"),
                          "name": n.get("name", ec.get("name", "")), "subtitle": n.get("subtitle", "Software Engineering student, Deakin")}
    if "endcard" in plan:
        e = plan["endcard"]
        out["endcard"] = {"from": T(e["from"], "endcard.from"), "title": e.get("title"), "name": e.get("name", ec.get("name", "")),
                          "subtitle": e.get("subtitle", ec.get("subtitle")), "lines": e.get("lines", ec.get("lines", []))}
    m = {**pj.cfg.get("music", {}), **plan.get("music", {})} if (plan.get("music") is not False) else {}
    if m.get("file"):
        anchor = T(m.get("anchor", 0), "music.anchor")
        out["music"] = {"src": media(m["file"].replace("documents/video/", ""), "music"), "startAt": round(anchor - float(m.get("music_at", 0)), 3),
                        "musicFrom": 0, "volume": float(m.get("volume", 0.1)), "endBoost": float(m.get("end_boost", 1)),
                        "stops": [{"from": T(s["from"], "music.stops"), "to": T(s["to"], "music.stops")} for s in m.get("stops", [])],
                        "dips": [{"from": T(d["from"], "music.dips"), "to": T(d["to"], "music.dips"), "factor": d.get("factor", 0.4)}
                                 for d in m.get("dips", [])]}
        if not m.get("credit"):
            warns.append("music has no 'credit' note: use YouTube Audio Library or CC BY with the credit in the YouTube description (Pixabay got Content ID blocked)")
    out["custom"] = bool(plan.get("custom"))

    # ---- rule checks
    splits = [b for b in out["broll"] if b.get("layout", "split") == "split"]

    def shifted(t):
        return any(b["from"] <= t < b["to"] for b in splits)

    for k, x in enumerate(out["texts"]):
        t = x["from"] + 0.05
        fx, fy, fw = face_at(ft, t)
        if shifted(t):
            fy += 520
        size = x.get("size", 120)
        top, bot = x.get("top", 250), x.get("top", 250) + size * 1.1
        half = len(x["txt"]) * size * 0.27
        cx = x.get("x", 540)
        if top < fy + 0.9 * fw and bot > fy - 0.75 * fw and cx - half < fx + 0.6 * fw and cx + half > fx - 0.6 * fw:
            warns.append(f"texts[{k}] '{x['txt']}' at {t:.2f}s may sit on his face (face y {fy - 0.75 * fw:.0f}-{fy + 0.9 * fw:.0f}, text y {top}-{bot:.0f})")
        if half * 2 > 1040:
            warns.append(f"texts[{k}] '{x['txt']}' is probably wider than the frame at size {size}")
    if cap.get("on"):
        bad = []
        for w in words:
            t = w["s"]
            if out.get("endcard") and t >= out["endcard"]["from"]:
                continue
            top = next((l["top"] for l in cap["lift"] if l["from"] <= t < l["to"]), cap.get("top", 1600))
            fx, fy, fw = face_at(ft, t)
            if shifted(t):
                fy += 520
            if top < fy + 0.85 * fw:
                bad.append(t)
        if bad:
            warns.append(f"captions overlap his chin/face at {len(bad)} word(s), first at {bad[0]:.2f}s: add a captions.lift with a lower top, or move them")
    for key in ("zooms", "broll"):
        xs = sorted(out[key], key=lambda z: z["from"])
        for a, b in zip(xs, xs[1:]):
            if b["from"] < a["to"]:
                warns.append(f"{key} overlap at {b['from']:.2f}s")

    (ed / "src" / "plan.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    md = [f"# Plan check: {pj.name}", "", f"Length {length:.2f}s. {len(errs)} error, {len(warns)} warning.", ""]
    md += [f"- **ERROR** {e}" for e in errs] + [f"- warning: {w}" for w in warns]
    md += ["", "## Resolved times", ""]
    for key in SPAN_KEYS:
        for x in out[key]:
            md.append(f"- {key}: {x['from']:.2f}-{x['to']:.2f} {x.get('txt', x.get('src', ''))}")
    for s in out["sfx"]:
        md.append(f"- sfx {s['name']} @ {s['at']:.2f}")
    pj.path("plan_check.md").write_text("\n".join(md), encoding="utf-8")
    print(f"{'FAILED' if errs else 'ok'}: {len(errs)} error, {len(warns)} warning -> {pj.path('plan_check.md')}")
    for e in errs + warns:
        print(" -", e)
    if errs:
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
