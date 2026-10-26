# Intro video protocol

How Manit's application intro videos are made. Written from the Andromeda video (18 Oct 2026,
final 2:09, sent to Carina Parisella, YouTube `youtube.com/shorts/Un5nHnbxTTA`). Ready to turn
into a skill.

The process follows a YouTube creator's Claude Code editing workflow:
**script → film → lock the cut → graphics plan → short-draft review loop → captions → music → one final render → upload and test.**

---

## 0. Folder map (`documents/video/`)

| Path | What it is |
|---|---|
| `broll/originals/` | Master demo footage, full quality (4K in-class clips, Open Day, clothesline). Never edit these. |
| `broll/cuts/` | Editor-ready B-roll (1080p, same clips trimmed and re-encoded) plus `stills/robot.png` (4K frame of the robot). Copy into the editor's `public/broll/` and `public/stills/`. |
| `music/` | `A Stroll - The Grey Room _ Density & Time.mp3` (YouTube Audio Library, no attribution needed). The track used in the final. |
| `andromeda/` | Final video (`Final v4`), its `Script.md`, `Graphics Plan.md`, `How to edit.md`. The worked example. |
| `editor-template/syncrowin-style/` | Syncrowin's PewDiePie-style Remotion editor (src, sound effects, images, music). Start new videos from this. |
| `editor-template/tools/` | Helper scripts: transcribe, cut the talking track from one long take, head/face tracking, speech regions. |
| `editor-template/` | The Remotion project without media or `node_modules`: `src/` (IntroVideo.tsx, Root.tsx, index.ts, timeline.json), `build_timeline.py`, `build_talking_track.py`, `find_speech_edges.py`, `make_music*.py`, `package.json`. |

### Reusable B-roll moments (from the Andromeda timeline)

| Cut | At | Shows | Used for |
|---|---|---|---|
| `stills/robot.png` | still | The robot, clean 4K frame | "I built robots" (slow zoom 1.0 → 1.25) |
| `openday.mp4` (3:16) | 0:44 | Code on screen at Open Day | "the server does the thinking" |
| `openday.mp4` | 2:17 | Manit stopping the server | "what if it loses Wi-Fi" |
| `openday.mp4` | 2:39 | Robot rolling itself back (zoom 1.7) | "it retraces its steps" |
| `class.mp4` (0:19) | 0:02 | Presenting to the class | "my unit chair told me I can't" |
| `drive_vertical.mp4` (0:10) | 0:02 | Driving the robot from the dashboard, vertical | "drive it like an RC car" (full screen) |
| `drive.mp4` (0:31) | | Same dashboard driving, landscape | spare |
| `clothesline.mp4` (2:08) | 0:19 | Hand on the robot | "the voltage converter" |
| `clothesline.mp4` | 0:32 | Battery pack close-up | "only worked on fresh batteries" |
| `clothesline.mp4` | 0:52 | Robot following its line | "the robot I want to build" |

---

## 1. Script

**Read `SCRIPT-RULES.md` first.** It holds Manit's corrections on how scripts should sound.


1. **Study the company's own videos first.** Download two or three team videos, transcribe them
   (faster-whisper), sample frames (ffmpeg), and copy their *order and voice*. Andromeda's pattern:
   open on a question → "Hey, I'm X, I do Y" → what I'm working on → "one of the challenges with
   that is" → "what you're looking at here is" (the screen) → why this company.
2. **Write about 90 seconds (~230 words)**, eight short sections, one take each. Andromeda's:
   Hook, Who I am, What I built, The challenge ("what if"), Show the screen, When it broke,
   Why <company>, Close.
3. **Facts check every line** against `01-candidate-profile.md` / `master-notes.md`. Example: the
   Wi-Fi recovery is a "what if" he designed for, never something that happened.
4. **Say "Software Engineering student"**, never "software engineer". Third-year, never second-year.
5. **The "why" section carries the video.** Use a real personal reason only if Manit gives it, in his
   words, and agree what stays private (Andromeda: grandfather story in, family conflict out). Pitch
   any idea humbly ("I don't know if that's possible yet").
6. **Close with energy back up** and hold two seconds of silence after the last word for the end card.

## 2. Film and organise

- Vertical 1080x1920, face centred, one take per section, file names numbered by section
  (`1 Hook.mp4`, `7a Why ... .mp4`).
- Best take of each section in `Talking Head/`; bad takes in `Talking Head/Unused Takes/` with the
  reason in the filename ("says software engineer (old)"). Move, never delete, until the final is approved.
- Transcribe every take with faster-whisper (word timestamps) into `transcripts/*.json`;
  `find_speech_edges.py` finds where speech starts and ends (silencedetect).

## 3. Lock the cut (step 1 of the YouTube workflow)

- `build_timeline.py` → `SECTIONS`: which part of each take is used (trim on word timestamps).
- `build_talking_track.py` joins the takes into one continuous talking track (`public/th/track.mp4`).
- Manit approves the rough cut (takes continuous, tight joins) **before** any graphics.

## 4. Graphics plan, then build

- Write `Graphics Plan.md` first: one row per moment (timestamp, what is said, what is on screen).
  Manit crosses out or changes rows before anything is built; cheaper than fixing afterwards.
- **Layout rules:**
  - No B-roll: face fills the screen.
  - With B-roll: **split screen**, demo in the top half (`SEAM = 960`), face in the bottom half
    shifted up (`FACE_SHIFT = 150`, 0.3 s ramp). He never disappears, so cuts don't feel jumpy.
  - Voice-only takes: full-screen B-roll (`full:` prefix).
  - **Text never sits on his face**: on the seam between halves, or at the very top.
  - Colours: the company's own palette (Andromeda: Abi's pink, lime, orange, purple). Font: Montserrat.
  - Never use the company's footage; the video is about his work.
  - Emotional section: face only, nothing on screen, music dips. Let it sit.
- B-roll entries: `(start, end, src, from_seconds, position, zoom, zoom_origin)`; graphics:
  `(type, start, duration, text)`: hook text, name tag, section tags, chips, pop-ups, end card.

## 5. Review loop: short drafts, not the studio

- Remotion Studio stutters on the laptop. Instead, after each change render **only the changed
  section** (5 to 30 s, under a minute): `npx remotion render src/index.ts IntroVideo out.mp4 --frames=A-B`.
- Drafts go in `Drafts/` named by time range ("Draft 2 - 0.27 to 1.02 (Wi-Fi what if, dashboard)").
- Manit gives notes in plain words with a timestamp ("0:46, robot too small, zoom in"). One change,
  one draft, repeat. Same as the YouTuber talking to Claude like an editor beside him.

## 6. Captions

- Word by word, current word highlighted in lime, bold white text on the brand-colour boxes.
- Placed on the chest below the face, never over the face or B-roll.
- Fix transcription spelling in `build_timeline.py` (Abi not Abby, "decided" not "decide").
- Built early but switched off until graphics are signed off.

## 7. Music

- **YouTube Audio Library only.** A Pixabay track ("Lo-fi Chill") got the upload blocked by
  Content ID. Generated music (`make_music_v2.py`) was tried and rejected by Manit.
- Final settings (A Stroll): `offset 16.25 s` so the music's entry lands on a key line
  ("I built robots"); `base 0.11` (about 11% volume); `duck 0.02` under the emotional section;
  `0.25` on the end card. Earlier guide: roughly -23 dB under speech.
- Remix audio without a video render: `--codec=wav`, then mux with `ffmpeg -c:v copy`.

## 8. Final render and export

    python build_timeline.py
    python build_talking_track.py
    npx remotion render src/index.ts IntroVideo "Final/Manit Khera - <Company> Intro (Final).mp4" --crf=18

- Keep one final; move older finals to `Final/Old Versions/` until sent, then delete them.
- An email-sized copy (~80 MB) if attaching; normally send a link instead.

## 9. Upload and send

- YouTube, **Unlisted**. A vertical video under 3 minutes becomes a Short automatically (fine).
- **Open the link in a private window before sending**: it must play with music and show no
  copyright notice.
- **Paste the link into the email before writing anything else.** The Andromeda email first went out
  without it and needed a follow-up.
- Log the send in `documents/notes/log.md` and the tracker; follow up once after about a week.

## Setup on a new machine / new video

1. Copy `editor-template/` to a working folder, run `npm install` (Remotion 4.0.242, React 18).
2. Create `public/broll/`, `public/stills/`, `public/music/`, `public/th/` and copy in the cuts,
   the still and `music/A Stroll ... .mp3` (rename to `stroll.mp3` or update `build_timeline.py`).
3. Tools: ffmpeg/ffprobe on PATH, Python with `faster-whisper`, `numpy`, `scipy`.
4. Rewrite `SECTIONS`, `BROLL`, `GRAPHICS` in `build_timeline.py` for the new script; recolour in
   `src/IntroVideo.tsx`.

## Plan for the startup EOI videos (from 20 Oct 2026)

One core cut (who I am, what I built, the challenge, when it broke, close) reused for every
company, plus a 10 to 15 s opening and a short "why you" recorded per company. Tier 1 targets
are in the startup EOI list (`documents/applications/cold_outreach_2026_10_16/Startup EOI Targets - 20 Oct 2026.md`).
