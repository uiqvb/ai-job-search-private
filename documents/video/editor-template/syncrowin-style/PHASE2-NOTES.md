# Syncrowin phase 2: where we are (22 Oct 2026)

Done: editor/ set up (Remotion, node_modules copied from Capgemini); public/th/track.mp4 = approved rough
cut (59.2 s); public/img/robot_sticker.png (real robot, hand-traced cut-out, white sticker border);
public/sfx/*.wav (20 generated SFX, sfx.py); public/music/stroll.mp3; src/words.json (rough-cut word times).
Palette (syncrowin.com.au CSS): lime #9BF03C, black #0C0C0C/#111110, off-white #F4F4EF, greys #CDCDC5 #75756E.

Measurements (rough-cut time, 1080x1920):
- Palm (reel 3.3-15.2): centre ~(165,1700), palm surface y ~1600. Palm up at 3.3, settled 3.5.
- Props pop: 100/100 at 3.45 ("100"), robot sticker at 5.6 ("project"), 6x badge 10.46-12.4 ("5000"/"6").
  Stack slots x~210: y 1470 / 1230 / 1000.
- Toss: hand starts 15.2, at shoulder 15.5; freeze to 16.89. Insert 2.4 s chase cutaway at 15.75.
- Music off at "that" 14.92, back at "You're" 17.04.
- Words: curious 18.66, energy 19.82, experiments 20.84, exactly me 22.02; what-if 23.9; breaks 27.4; fun part 28.78.
- Head top ~(565,550) during hats (stable). backend 35.54, hardware 36.88, IT support 38.04, video 39.88.
- Reveal "Because" 40.54 to 44.9: shrink live video into a Claude Code editor window (real steps), scratch SFX.
- Fire palm base ~(160,1450); palm up 47.2-47.5, ignite 47.6, "Syncrowin" 51.74, fist closes 52.35 (puff).
- Close 53.0; "watching" 56.72; timer 1:00 -> 0:00 from "minute" 1.26 to "watching".
Next: write src/ (Root.tsx, index.ts, Video.tsx), render a preview of 13-20 s, then the full render.

## 22 Oct, later: src written and Draft 1 rendered
- src/Video.tsx holds every effect, timed from rough-cut word times; out() adds the 2.4 s chase cutaway
  inserted at 15.75 (total 61.7 s, 1852 frames). Composition id `Syncrowin`.
- Freeze frame for the cutaway zoom: public/img/freeze.png (track 15.767 s).
- Music: A Stroll from 23.8 s at "minute", cut on "that", resumes from 62.5 s on "You're"; 0.11, 0.16 during
  the fire hold, 0.25 on the end card. Captions built later (CAPTIONS flag off).
- Fire and explosion are drawn in code (Remotion particles), no AI video tool.
- Preview: npx remotion render src/index.ts Syncrowin out.mp4 --frames=A-B (frames = output s x 30).

## Draft 2 (22 Oct): PewDiePie-style rebuild after Manit's notes
- Draft 1 code kept as src/Video_draft1.tsx.bak. New src/Video.tsx follows documents/video/EDITING-STYLE.md.
- No cutaway insert; one hard cut skips the frozen beat 16.45 -> 16.95 (total 58.83 s, 1765 frames).
- src/face_track.json: OpenCV Haar face track (centre x, y, width) every 3 frames; drives snap zooms + hats.
- public/img: hats/bin = CC0/PD photo cutouts (CREDITS.txt); claude_code.png = Manit's screenshot, job table blurred.
- public/glitch: rembg cutouts of track frames 820-843 (glitch on "breaks" applies only to him).
- public/sfx/echo_that.wav (wet echo of "that", 14.92-15.28), boom_boost.wav (+18 dB clipped, turned down).
- rembg needs NUMBA_DISABLE_JIT=1 here (numba cache write fails). OpenCV must be 4.x (5.x lacks CascadeClassifier).
