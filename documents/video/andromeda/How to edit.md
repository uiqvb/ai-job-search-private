# Intro video: how it is built

- `Raw Recordings/Talking Head/`: best take of each script section, numbered. Bad takes in `Unused Takes/`.
- `Raw Recordings/B-roll/`: demo footage. Master copies of reusable footage live in `Resume/Evidences/`.
- `editor/`: the Remotion project that makes the video.
  - `build_timeline.py`: which part of each take is used, captions fixes, where B-roll and graphics go.
  - `src/IntroVideo.tsx`: the look (captions, colours, graphics, end card).
  - `make_music.py`: the quiet background pad.
- `Final/`: rendered videos.

To rebuild after a change (from `editor/`):

    python build_timeline.py
    python build_talking_track.py   # joins the takes into one file the editor plays
    npx remotion render src/index.ts IntroVideo "../Final/Manit Khera - Andromeda Intro (vN).mp4" --crf=18

To preview in a browser: `npx remotion studio src/index.ts`
