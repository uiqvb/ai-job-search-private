"""Phase 1, step 3: measure the rough cut so the cut-reviewer agent can judge every join.

    python tools/video/check_cut.py documents/video/<company> --round N

Agents can't listen, so this turns sound into numbers and pictures:
  - re-transcribes the rough cut and compares each piece with what the raw take says there
  - per join: dead air, words running together, loudness jump, a phrase repeated across the cut
  - per piece edge: cut lands mid-sound (clipped word), head turning (face missing / off-centre)
  - pictures: pipeline/review/roundN/join_XX.png = 4 frames around the cut + the loudness curve with words
Writes pipeline/review/roundN/report.md + report.json, and pipeline/rough_words.json (reused by Phase 2).
"""

import json
import sys
from difflib import SequenceMatcher

import cv2
import numpy as np

import vlib

DEAD_FAIL, DEAD_WARN, TIGHT = 0.65, 0.45, 0.08
LOUD_WARN, LOUD_FAIL = 4.0, 7.0
LONG_PAUSE = 0.9
FW, FH = 270, 480     # thumbnail size


def faces(img):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    f = CASC.detectMultiScale(g, 1.1, 5, minSize=(40, 40))
    if not len(f):
        return None
    x, y, w, h = max(f, key=lambda r: r[2])
    return (x + w / 2, y + h / 2, w)


CASC = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


def grab(path, times):
    """Thumbnails at the given times (one decode pass)."""
    cap = cv2.VideoCapture(str(path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    want = sorted({max(0, int(round(t * fps))) for t in times})
    out, i, j = {}, 0, 0
    while j < len(want):
        ok = cap.grab()
        if not ok:
            break
        if i == want[j]:
            _, fr = cap.retrieve()
            out[i] = cv2.resize(fr, (FW, FH))
            j += 1
        i += 1
    cap.release()
    return Thumbs({t: out.get(max(0, int(round(t * fps))), np.zeros((FH, FW, 3), np.uint8)) for t in times})


class Thumbs(dict):
    """Frames by time; a lookup returns the nearest grabbed frame, so float rounding never misses."""
    def __missing__(self, t):
        return self[min(self.keys(), key=lambda k: abs(k - t))]


def strip(env, thr, t0, t1, cut, words, width=4 * FW, height=170):
    """Loudness curve between t0 and t1 with the cut line and word labels."""
    img = np.full((height, width, 3), 255, np.uint8)
    a, b = int(t0 / vlib.HOP), int(t1 / vlib.HOP)
    seg = env[max(0, a):b]
    if len(seg) < 2:
        return img
    y = lambda db: int(height - 30 - (np.clip(db, -70, 0) + 70) / 70 * (height - 50))
    x = lambda t: int((t - t0) / (t1 - t0) * (width - 1))
    pts = np.array([[x(t0 + k * vlib.HOP), y(v)] for k, v in enumerate(seg)], np.int32)
    cv2.line(img, (0, y(thr)), (width, y(thr)), (200, 200, 200), 1)
    cv2.polylines(img, [pts], False, (40, 40, 40), 2)
    cv2.line(img, (x(cut), 0), (x(cut), height), (0, 0, 230), 2)
    for w in words:
        if t0 <= w["s"] <= t1:
            cv2.rectangle(img, (x(w["s"]), height - 26), (max(x(w["s"]) + 1, x(w["e"])), height - 22), (200, 120, 0), -1)
            cv2.putText(img, w["w"][:12], (x(w["s"]), height - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (120, 60, 0), 1)
    cv2.putText(img, f"loudness {t0:.2f}-{t1:.2f}s  red = cut  grey = speech threshold", (6, 16),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1)
    return img


def label(img, text):
    img = img.copy()
    cv2.rectangle(img, (0, 0), (FW, 24), (0, 0, 0), -1)
    cv2.putText(img, text, (6, 17), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    return img


def loud_runs(env, thr, a, b):
    """First and last loud frame time inside [a, b]."""
    idx = [k for k in range(max(0, int(a / vlib.HOP)), min(len(env), int(b / vlib.HOP))) if env[k] > thr]
    return (idx[0] * vlib.HOP, idx[-1] * vlib.HOP) if idx else (None, None)


def main(folder, rnd):
    pj = vlib.Project(folder)
    cl = pj.read_json("cut_list.json")
    pieces = cl["pieces"]
    rough = pj.path("rough_cut.mp4")
    outdir = pj.path("review", f"round{rnd}")
    outdir.mkdir(parents=True, exist_ok=True)
    # names only: giving Whisper the whole script makes it skip words it thinks were already said
    rw = vlib.transcribe(rough, pj.path("rough_words.json"), pj.cfg.get("transcribe_prompt", ""))
    expected = sum(len([w for w in vlib.transcribe(pj.raw(p["file"]), pj.path("transcripts", pj.raw(p["file"]).stem + ".json"))
                        if p["in"] <= w["s"] <= p["out"]]) for p in pieces)
    if len(rw) < 0.6 * expected:
        print(f"re-transcription found {len(rw)} of ~{expected} words; retrying without a prompt", flush=True)
        rw = vlib.transcribe(rough, pj.path("rough_words.json"), "", force=True)
    env = vlib.rms_db(vlib.audio(rough))
    thr = vlib.speech_threshold(env)
    end_hold = float(pj.cfg.get("end_hold", 2.0))
    src_words = {}
    issues, joins, edges = [], [], []

    # ---- coverage
    ids = [p["line"] for p in pieces]
    for L in pj.lines:
        if ids.count(L["id"]) == 0:
            issues.append(("fail", f"line '{L['id']}' is missing from the cut"))
        elif ids.count(L["id"]) > 1:
            issues.append(("warn", f"line '{L['id']}' is used {ids.count(L['id'])} times"))
    order = [L["id"] for L in pj.lines]
    if [i for i in ids if i in order] != sorted([i for i in ids if i in order], key=order.index):
        issues.append(("warn", "pieces are not in script order"))

    # ---- per piece
    times = []
    for k, p in enumerate(pieces):
        f = p["file"]
        if f not in src_words:
            src_words[f] = vlib.transcribe(pj.raw(f), pj.path("transcripts", pj.raw(f).stem + ".json"))
        dur = p["out"] - p["in"]
        speech_end = dur - (end_hold if k == len(pieces) - 1 else 0)
        p["_a"], p["_b"], p["_speech_end"] = p["at"], p["at"] + dur, p["at"] + speech_end
        times += [p["at"] + 0.03, p["at"] + 0.15, p["at"] + 0.3, p["at"] + dur * 0.5,
                  p["at"] + speech_end - 0.3, p["at"] + speech_end - 0.1]
        if k:
            times += [p["at"] - 0.25, p["at"] - 0.04, p["at"] + 0.04, p["at"] + 0.25]
    times += [pieces[-1]["_b"] - 0.1]
    thumbs = grab(rough, times)

    src_env, src_thr = {}, {}
    for k, p in enumerate(pieces):
        f, a, b = p["file"], p["_a"], p["_b"]
        if f not in src_env:
            src_env[f] = vlib.rms_db(vlib.audio(pj.raw(f)))
            src_thr[f] = vlib.speech_threshold(src_env[f])
        se, st = src_env[f], src_thr[f]
        notes = []
        # clipped edges: the raw audio is still loud right at the cut point
        i_in, i_out = int(p["in"] / vlib.HOP), int((p["out"] - (end_hold if k == len(pieces) - 1 else 0)) / vlib.HOP)
        if 0 <= i_in < len(se) and se[i_in] > st:
            notes.append(("fail", "starts mid-sound (first word may be clipped)"))
        if 0 <= i_out < len(se) and se[min(i_out, len(se) - 1)] > st and k != len(pieces) - 1:
            notes.append(("fail", "ends mid-sound (last word may be clipped)"))
        # words: what the raw take says inside the piece vs what the rough cut says
        exp = [w for w in src_words[f] if w["s"] >= p["in"] - 0.02 and w["e"] <= p["out"] + 0.02]
        got = [w for w in rw if a - 0.05 <= w["s"] < b - 0.02]
        et, gt = [vlib.norm(w["w"]) for w in exp], [vlib.norm(w["w"]) for w in got]
        sm = SequenceMatcher(None, et, gt, autojunk=False)
        ratio = round(sm.ratio(), 2)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                continue
            edge = i1 == 0 or i2 == len(et) or j1 == 0 or j2 == len(gt)
            if edge:
                notes.append(("warn", f"words differ at the {'start' if (i1 == 0 or j1 == 0) else 'end'}: "
                                      f"raw '{' '.join(et[i1:i2])}' vs cut '{' '.join(gt[j1:j2])}'"))
        if ratio < 0.8:
            notes.append(("warn", f"re-transcription only matches {ratio:.0%} of the raw words (check for garbled audio)"))
        # long pauses inside the piece
        gaps = [(x["e"], y["s"]) for x, y in zip(got, got[1:]) if y["s"] - x["e"] > LONG_PAUSE]
        for g0, g1 in gaps:
            notes.append(("warn", f"pause of {g1 - g0:.1f}s inside the piece at {g0:.2f}s (fine if it is a planned hold)"))
        # head turning at the start/end: face missing or far from where it settles
        mid = faces(thumbs[p["at"] + (b - a) * 0.5])
        for tag, t in (("start", p["at"] + 0.03), ("start", p["at"] + 0.15), ("end", p["_speech_end"] - 0.1)):
            fc = faces(thumbs[t])
            if mid and not fc:
                notes.append(("warn", f"no face found at {t:.2f}s ({tag}); he may be looking down or turning"))
            elif mid and fc and abs(fc[0] - mid[0]) > 0.45 * mid[2]:
                notes.append(("warn", f"head off to the side at {t:.2f}s ({tag}) vs the middle of the piece"))
        edges.append({"piece": k, "line": p["line"], "at": round(a, 2), "length": round(b - a, 2),
                      "said": " ".join(w["w"] for w in got), "match": ratio,
                      "issues": [{"level": l, "text": t} for l, t in dict.fromkeys(notes)]})

    # ---- per join
    for k in range(1, len(pieces)):
        prev, cur = pieces[k - 1], pieces[k]
        t = cur["at"]
        _, last = loud_runs(env, thr, max(0, t - 2.0), t)
        first, _ = loud_runs(env, thr, t, t + 2.0)
        gap = round((first if first is not None else t) - (last if last is not None else t), 2)
        # overall speech level of the piece before vs the piece after (median of clearly loud frames)
        def level(x0, x1):
            seg = env[int(max(0, x0) / vlib.HOP):int(x1 / vlib.HOP)]
            loud = seg[seg > thr + 6]
            return float(np.median(loud)) if len(loud) > 20 else None
        lb = level(prev["_a"], prev["_speech_end"])
        la = level(cur["_a"], cur["_speech_end"])
        jump = round(abs(lb - la), 1) if lb is not None and la is not None else None
        notes = []
        if gap > DEAD_FAIL:
            notes.append(("fail", f"dead air {gap:.2f}s"))
        elif gap > DEAD_WARN:
            notes.append(("warn", f"gap {gap:.2f}s, a little long"))
        elif gap < TIGHT:
            notes.append(("warn", f"gap only {gap:.2f}s, words may run together"))
        if jump is not None and jump > LOUD_FAIL:
            notes.append(("fail", f"loudness jumps {jump} dB"))
        elif jump is not None and jump > LOUD_WARN:
            notes.append(("warn", f"loudness changes {jump} dB"))
        # the same 3 words on both sides (a line said twice, or a restart left in)
        tb = [vlib.norm(w["w"]) for w in rw if t - 4 <= w["s"] < t][-10:]
        ta = [vlib.norm(w["w"]) for w in rw if t <= w["s"] < t + 4][:12]
        grams = lambda xs: {tuple(xs[i:i + 3]) for i in range(len(xs) - 2)}
        rep = grams(tb) & grams(ta)
        if rep:
            notes.append(("fail", f"words repeated across the cut: '{' '.join(sorted(rep)[0])}'"))
        img = np.vstack([np.hstack([label(thumbs[t - 0.25], f"-0.25s {prev['line'][:14]}"), label(thumbs[t - 0.04], "-0.04s"),
                                    label(thumbs[t + 0.04], "+0.04s"), label(thumbs[t + 0.25], f"+0.25s {cur['line'][:14]}")]),
                         strip(env, thr, t - 1.5, t + 1.5, t, rw)])
        name = f"join_{k:02d}.png"
        cv2.imwrite(str(outdir / name), img)
        joins.append({"join": k, "at": round(t, 2), "between": [prev["line"], cur["line"]], "gap": gap, "loudness_jump_db": jump,
                      "image": f"pipeline/review/round{rnd}/{name}",
                      "issues": [{"level": l, "text": x} for l, x in notes]})

    # first and last frame sheets
    p0, pl = pieces[0], pieces[-1]
    cv2.imwrite(str(outdir / "start_end.png"), np.vstack([
        np.hstack([label(thumbs[p0["at"] + 0.03], "start +0.03s"), label(thumbs[p0["at"] + 0.3], "start +0.3s"),
                   label(thumbs[pl["_speech_end"] - 0.1], "last word"), label(thumbs[pl["_b"] - 0.1], "end of hold")]),
        strip(env, thr, 0, 3.0, 0, rw)]))

    nfail = sum(1 for x in joins + edges for i in x["issues"] if i["level"] == "fail") + sum(1 for l, _ in issues if l == "fail")
    nwarn = sum(1 for x in joins + edges for i in x["issues"] if i["level"] == "warn") + sum(1 for l, _ in issues if l == "warn")
    report = {"round": rnd, "length": cl["length"], "fails": nfail, "warnings": nwarn,
              "general": [{"level": l, "text": t} for l, t in issues], "pieces": edges, "joins": joins,
              "start_end_image": f"pipeline/review/round{rnd}/start_end.png"}
    (outdir / "report.json").write_text(json.dumps(report, indent=1), encoding="utf-8")

    md = [f"# Cut check, round {rnd}: {pj.name}", "",
          f"Length {cl['length']:.1f}s, {len(pieces)} pieces, {len(joins)} joins. **{nfail} fail, {nwarn} warning.**", "",
          "Automatic measurements; the reviewer decides. Pictures: 4 frames around each cut + loudness curve with words.", ""]
    for l, t in issues:
        md.append(f"- **{l.upper()}** {t}")
    md += ["", "## Pieces", "", "| # | line | at | len | match | said (re-transcribed) | issues |", "|---|---|---|---|---|---|---|"]
    for e in edges:
        md.append(f"| {e['piece']} | {e['line']} | {e['at']} | {e['length']} | {e['match']} | {e['said'][:90]} | "
                  + "; ".join(f"{i['level'].upper()}: {i['text']}" for i in e["issues"]) + " |")
    md += ["", "## Joins", "", "| # | at | between | gap | loud jump | issues | picture |", "|---|---|---|---|---|---|---|"]
    for j in joins:
        md.append(f"| {j['join']} | {j['at']} | {j['between'][0]} -> {j['between'][1]} | {j['gap']} | {j['loudness_jump_db']} | "
                  + ("; ".join(f"{i['level'].upper()}: {i['text']}" for i in j["issues"]) or "ok") + f" | {j['image']} |")
    md += ["", f"Start and end: {report['start_end_image']}", ""]
    (outdir / "report.md").write_text("\n".join(md), encoding="utf-8")
    print(f"ok round {rnd}: {nfail} fail, {nwarn} warning -> {outdir / 'report.md'}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    rnd = int(sys.argv[sys.argv.index("--round") + 1]) if "--round" in sys.argv else 1
    args = [a for a in args if a != str(rnd)]
    if len(args) != 1:
        sys.exit(__doc__)
    main(args[0], rnd)
