# Intro-video pipeline (`tools/video/`)

Turns raw takes into a finished application intro video in two phases, with agents doing the work and
Manit approving at three gates. Run it with `/video` (`.claude/commands/video.md`). The style and process
rules live in `documents/video/PROTOCOL.md`, `SCRIPT-RULES.md` and `EDITING-STYLE.md`.

```
PHASE 1  cut          prep.py -> video-cutter agent -> render_cut.py -> check_cut.py -> cut-reviewer agent
                      (loop up to 3 rounds) -> add_music.py          GATE 1: Manit approves the music cut
PHASE 2  visuals      setup_editor.py -> visual-planner agent writes plan.json + Visual Plan.md
                                                                     GATE 2: Manit approves the plan
                      build_plan.py -> render.py draft -> check_frames.py -> visual-reviewer agent
                      (loop up to 3 rounds per section)              GATE 3: Manit watches, notes, final
```

Agents can't hear. Sound reaches them as numbers (gaps, loudness, clipped edges), re-transcription and
loudness curves drawn under the join pictures. Manit's ear is the last check, at gate 1 and gate 3.

## Project folder (`documents/video/<company>/`, gitignored)

| Path | Written by |
|---|---|
| `project.json` | `/video new` (script lines, raw folder, grade, music, end card) |
| `Raw Takes/` | Manit: one long take, one file per line, or a mix |
| `pipeline/transcripts/*.json` | prep.py (word timings, cached) |
| `pipeline/takes.md`, `takes.json` | prep.py: every attempt of every line |
| `pipeline/cuts.json` | video-cutter agent |
| `pipeline/cut_list.json`, `rough_cut.mp4` | render_cut.py (exact times used) |
| `pipeline/rough_words.json` | check_cut.py (word timings of the cut; Phase 2 anchors and captions) |
| `pipeline/review/roundN/` | check_cut.py report + join pictures, and the reviewer's verdict |
| `pipeline/rough_cut_music.mp4` | add_music.py (gate 1) |
| `pipeline/plan.json`, `Visual Plan.md` | visual-planner agent (gate 2) |
| `pipeline/plan_check.md` | build_plan.py |
| `editor/` (or project.json `"editor"`) | setup_editor.py (Remotion kit copy) |
| `Drafts/`, `Final/` | render.py |

### project.json

```json
{
 "company": "Acme",
 "raw": "Raw Takes",
 "editor": "editor",
 "transcribe_prompt": "names Whisper should spell right: Acme, Deakin, Manit Khera, MatchFeel",
 "grade": "optional ffmpeg colour filter (Infosys used a warm 'sunny' grade)",
 "end_hold": 2.0,
 "lines": [
  {"id": "1 Hook", "text": "what he should say (pointers are fine)", "exact": false, "action": "what he does: hold 1 s, point at lens"}
 ],
 "music": {"file": "documents/video/music/<track>.mp3", "volume": 0.11, "music_at": 16.25,
           "anchor": {"word": "robots", "n": 1}, "dips": [], "end_boost": 2.3,
           "credit": "YouTube Audio Library, no attribution needed"},
 "end_card": {"name": "MANIT KHERA", "subtitle": "Software Engineering student · Deakin University", "lines": ["email", "linkedin"]}
}
```

## plan.json (Phase 2, written by the visual-planner)

Times are **anchors**, so a re-cut never breaks the plan: a number (seconds), `{"word": "right", "n": 1,
"edge": "s"|"e", "offset": 0.1}` (n-th time that word or phrase is said in the cut), or `"@name+0.2"`
referring to the `anchors` block. Media paths are relative to `documents/video/` (`broll/cuts/openday.mp4`,
`broll/cuts/stills/robot.png`) or `project:img/x.png` for this video's own files. Frame is 1080x1920.

| Key | Fields | Use |
|---|---|---|
| `anchors` | `{"name": anchor}` | name the beats once, reuse as `"@name"` |
| `zooms` | from, to, scale (1.2-1.9), tilt (deg) | snap zoom that follows his face (punchlines) |
| `follow` | from, to, scale, amount | frame drifts with his head turn (gestures) |
| `bw` | from, to | black-and-white beat (pair with `echo` and a zoom, ~0.7 s) |
| `echo` | id, word, vol | wet-only echo tail on a punchline word |
| `shakes` | at, strength | short camera shake on an impact |
| `broll` | from, to, src, start (s in clip), layout `split`/`full`, zoom, focus [x,y] = point to centre, in pixels of the 1080x960 split box (or 1080x1920 for full), push | demo footage; `split` = demo top half, his face pushed down (he never disappears) |
| `texts` | from, to, txt, size, top, x, rot | meme text: white Anton, black outline, hard cut in |
| `stickers` | from, to, src, x, y, width, anim `pop`/`slide`/`rise`, rise_to, label | real photo cut-outs (white sticker outline) |
| `bursts` | at, x, y | white impact lines |
| `nametag` | from, to (name/subtitle default from project) | name tag top-left |
| `endcard` | from, title (optional) | black end card with name, subtitle, contact lines |
| `captions` | on, top (default 1600), lift [{from, to, top}], fix {"Abby": "Abi"} | word-by-word, current word yellow |
| `sfx` | name, at, vol, max | pop ding ding2 whoosh whip rocket boom tinkle slam scribble glitch sparkle clap scratch typing ignite crackle puff bloop tick thock tada |
| `music` | stops [{from,to}] (music pauses, then resumes), dips [{from,to,factor}], volume, file, music_at, anchor | overrides project music; `false` = no music |
| `custom` | true | render this video's one-off gags from `editor/src/Custom.tsx` |

## Commands

```
python tools/video/prep.py <project>
python tools/video/render_cut.py <project> [--fast]
python tools/video/check_cut.py <project> --round N
python tools/video/add_music.py <project>
python tools/video/peek.py <project> <raw file|rough|music|path.mp4> t1 t2 ...
python tools/video/setup_editor.py <project>
python tools/video/build_plan.py <project>
python tools/video/render.py <project> draft <from> <to> "note" | draft all | final
python tools/video/check_frames.py <project> "<draft.mp4>"
```

Needs ffmpeg/ffprobe on PATH, Python with faster-whisper, numpy, scipy, opencv-python, and Node (Remotion 4.0.242).
