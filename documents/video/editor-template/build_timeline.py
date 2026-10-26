"""Builds timeline.json for the Remotion edit from the word-level transcripts.

Edit the SECTIONS list below (which part of each take to use) and the BROLL / GRAPHICS lists
(what goes on screen, anchored to spoken words), then run:  python build_timeline.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
GAP = 999         # never cut pauses inside a take; each section plays as one continuous take
PAD_IN, PAD_OUT = 0.25, 0.35

# id, source range in the take (seconds), on-screen section tag (or None)
SECTIONS = [
    ("1",  12.4, 17.0, None),
    ("2",  20.8, 28.2, None),
    ("3",   7.2, 23.1, None),
    ("4",   5.1, 33.8, "THE WHAT IF"),
    ("5",   1.9, 8.6,  None),
    ("6",  11.4, 24.8, "WHEN IT BROKE"),
    ("7a",  8.8, 23.7, None),   # grandfather: nothing on screen
    ("7b", 31.8, 50.5, None),
    ("7c", 27.1, 35.7, None),
    ("8",  11.9, 20.3, None),
]

# caption fixes: section -> {spoken token: caption text}; "" drops the token
FIXES = {
    "1": {"go": "gone", "on": ""},
    "2": {},
    "3": {"decide": "decided"},
    "4": {"it's": "its"},
    "7b": {"Abby": "Abi", "Abby,": "Abi,"},
}


def load_words(sid):
    data = json.load(open(os.path.join(HERE, "transcripts", f"{sid}.json")))
    words = []
    for seg in data:
        for w in seg["words"]:
            t = w["w"].strip()
            if words and (t.startswith("-") or t == "%"):
                words[-1]["w"] += t.lstrip("-") if t.startswith("-") else t
                words[-1]["e"] = w["e"]
                if t.startswith("-"):
                    words[-1]["w"] = words[-1]["w"].replace("WiFi", "Wi-Fi")
                continue
            words.append({"w": t, "s": w["s"], "e": w["e"]})
    return words


def norm(sec):
    sid, a, b = sec[0], sec[1], sec[2]
    if isinstance(a, list):
        return sid, a, sec[3]
    return sid, [(a, b)], sec[3]


EDGES = json.load(open(os.path.join(HERE, "transcripts", "edges.json"))) if os.path.exists(os.path.join(HERE, "transcripts", "edges.json")) else {}
LEAD_IN, TAIL = 0.12, 0.22   # breathing room around the real speech edges (from find_speech_edges.py)

pieces, words_out, sections_out = [], [], []
t = 0.0
for raw in SECTIONS:
    sid, ranges, tag = norm(raw)
    allw = load_words(sid)
    fixes = FIXES.get(sid, {})
    sec_start = t
    chosen = [w for w in allw if any(a <= w["s"] < b for a, b in ranges)]
    # group into runs, split on long pauses or range boundaries
    runs, cur = [], []
    for w in chosen:
        if cur and (w["s"] - cur[-1]["e"] > GAP or
                    not any(a <= cur[-1]["s"] < b and a <= w["s"] < b for a, b in ranges)):
            runs.append(cur); cur = []
        cur.append(w)
    if cur:
        runs.append(cur)
    for i, run in enumerate(runs):
        src_from = max(0, run[0]["s"] - PAD_IN)
        src_to = run[-1]["e"] + PAD_OUT
        if i + 1 < len(runs):
            src_to = min(src_to, runs[i + 1][0]["s"] - PAD_IN)
        if sid in EDGES and len(runs) == 1:
            src_from = max(0, EDGES[sid]["onset"] - LEAD_IN)
            src_to = EDGES[sid]["offset"] + TAIL
        dur = src_to - src_from
        pieces.append({"src": f"th/{sid}.mp4", "from": round(src_from, 3), "dur": round(dur, 3),
                       "start": round(t, 3), "zoom": 1.0,
                       "section": sid})
        for w in run:
            txt = fixes.get(w["w"], w["w"])
            if txt == "":
                continue
            words_out.append({"text": txt, "start": round(t + w["s"] - src_from, 3),
                              "end": round(t + w["e"] - src_from, 3), "section": sid})
        t += dur
    sections_out.append({"id": sid, "start": round(sec_start, 3), "end": round(t, 3), "tag": tag})

TOTAL_SPEECH = t


def at(sid, word, nth=1, edge="start"):
    """Output time of the nth caption word in a section that starts with `word`."""
    n = 0
    for w in words_out:
        if w["section"] == sid and w["text"].lower().strip(".,?!").startswith(word.lower()):
            n += 1
            if n == nth:
                return w[edge]
    raise KeyError(f"{word!r} #{nth} not in section {sid}")


def sec(sid):
    return next(s for s in sections_out if s["id"] == sid)


# B-roll (shown split screen: footage on top, face below). Matches "Graphics Plan.md".
# (start, end, file or "panel:<name>", source second, objectPosition, zoom, zoom origin)
BROLL = [
    # 3  still of the robot (from the 4K in-class clip), slow zoom in
    (at("2", "built") - 0.2, sec("2")["end"], "image:stills/robot.png", 0, "50% 50%", 1.25, "51% 62%"),
    # 5  Open Day: talking visitors through it
    (at("3", "server") - 0.2, at("3", "because") - 0.3, "broll/openday.mp4", 44.0, "50% 50%", 1.0, "50% 50%"),
    # 6  in-class presentation, "unit chair told me I cannot"
    (at("3", "because") - 0.3, at("3", "decided") - 0.5, "broll/class.mp4", 2.0, "50% 50%", 1.0, "50% 50%"),
    # 9  Open Day: stopping the server (Wi-Fi what if)
    (at("4", "robot", 1) - 0.3, at("4", "send") - 0.2, "broll/openday.mp4", 137.0, "25% 50%", 1.0, "50% 50%"),
    # 10-11  robot rolling itself back, zoomed in
    (at("4", "send") - 0.2, sec("4")["end"], "broll/openday.mp4", 159.0, "55% 50%", 1.7, "55% 28%"),
    # 12  in-class: driving from the dashboard
    (sec("5")["start"], sec("5")["end"], "full:broll/drive_vertical.mp4", 2.0, "50% 50%", 1.0, "50% 50%"),  # take 5 is voice only
    # 14  battery pack close-up
    (at("6", "For") - 0.2, at("6", "found") - 0.2, "broll/clothesline.mp4", 32.0, "50% 50%", 1.0, "50% 50%"),
    # 15  hand on the robot (voltage converter)
    (at("6", "found") - 0.2, at("6", "So") - 0.1, "broll/clothesline.mp4", 19.0, "50% 50%", 1.0, "50% 50%"),
    # 20  family -> Abi line drawing, as a panel in the top half
    (at("7b", "What", 3) - 0.2, sec("7b")["end"], "panel:globe", 0, "", 1.0, ""),
    # 21  clothesline robot following its line
    (sec("7c")["start"], at("7c", "and", 1) - 0.1, "broll/clothesline.mp4", 52.0, "50% 50%", 1.0, "50% 50%"),
]

# Graphics: (type, start, duration, text). Placed on the split seam when B-roll is up, else on the chest.
GRAPHICS = [
    ("hook", 0.0, 2.6, "TOLD YOU CAN'T?"),
    ("nametag", sec("2")["start"] + 0.3, at("2", "built") - sec("2")["start"] - 0.5,
     "Manit Khera|Software Engineering student · Deakin University"),
    ("chips", at("3", "thinking") - 0.4, at("3", "because") - at("3", "thinking") + 0.1, "SERVER: THINKS|ROBOT: DOES"),
    ("quote", at("3", "told") - 0.2, at("3", "decided") - at("3", "told") - 0.3, "Nah, you can't do that."),
    ("wifi", at("4", "Wi-Fi", 1) - 0.3, 2.8, ""),
    ("chips", at("4", "undo") - 0.4, 2.8, "COMMAND|+ ITS UNDO"),
    ("label", at("4", "retrace") - 0.2, sec("4")["end"] - at("4", "retrace") + 0.1, "IT RETRACES ITS STEPS"),
    ("label", at("5", "RC") - 0.3, 1.6, "LIKE AN RC CAR"),
    ("label", at("6", "problem") - 0.2, at("6", "So") - at("6", "problem") + 0.1, "THE CULPRIT: VOLTAGE CONVERTER"),
    ("batteries", at("6", "90") - 0.3, sec("6")["end"] - at("6", "90") + 0.4, "90%"),
    ("label", at("7b", "what", 1) - 0.05, 1.6, "WHAT IF?"),
]

END_CARD = 4.0
total = TOTAL_SPEECH + END_CARD

out = {
    "fps": 30, "total": round(total, 3), "endCardStart": round(TOTAL_SPEECH, 3),
    "pieces": pieces, "words": words_out, "sections": sections_out,
    "broll": [{"start": round(a, 3), "dur": round(b - a, 3), "src": s, "from": f, "pos": p, "zoom": z, "origin": o} for a, b, s, f, p, z, o in BROLL],
    "captions": True,
    # Music: "Lo-fi Chill" (zephiramusic, Pixabay). Track starts 23s in so its kick lands on
    # "I built robots" (0:07.75) and its dip/re-entry lands on "I saw a video of Abi" (1:30.2).
    # Music: "A Stroll" (The Grey Room / Density & Time, YouTube Audio Library, no attribution).
    # Pixabay track was blocked by YouTube on 18 Oct. Track starts 16.25s in so its full entry
    # (24.0s in the track) lands on "I built robots" (0:07.75). Ducked under the grandfather.
    "music": {"src": "music/stroll.mp3", "offset": 16.25, "base": 0.11, "duck": 0.02,
              "duckStart": round(sec("7a")["start"] - 0.2, 3), "duckEnd": round(at("7b", "Then") - 0.1, 3),
              "endLift": 0.25},
    "graphics": [{"type": ty, "start": round(a, 3), "dur": round(d, 3), "text": x} for ty, a, d, x in GRAPHICS],
}
json.dump(out, open(os.path.join(HERE, "src", "timeline.json"), "w"), indent=1)
print(f"speech {TOTAL_SPEECH:.1f}s, total {total:.1f}s, {len(pieces)} pieces, {len(words_out)} words")
for s in sections_out:
    print(f"  {s['id']:>3} {s['start']:6.2f} -> {s['end']:6.2f}  ({s['end']-s['start']:.1f}s)")
