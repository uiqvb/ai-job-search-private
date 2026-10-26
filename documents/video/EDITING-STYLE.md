# Editing style: old-PewDiePie, human-made (research notes, 22 Oct 2026)

Why this file exists: Manit rejected Syncrowin Draft 1 as "hella AI-ey" (grey chase tunnel, cracked-screen
glitch, lime brand colours, vector hats, fake typing terminal). He wants the old PewDiePie editing feel:
it should look like a person cut it in Premiere, not like generated motion graphics.
Read this before planning effects for any intro video.

## What the sources say

**"How To Edit like Pewdiepie (Brad 1 & Brad 2)"**, Learn How To Edit Stuff, 2018
(youtube.com/watch?v=N06nBy6OzHs). Transcribed and frame-checked. Six core moves:
1. **The zoom, following the subject.** Keyframe position, scale and rotation. Snap in fast on the face
   (keyframes close together = faster), re-position every few frames so the face stays centred as the head
   moves, tilt with the head, and scale up enough that no black corners show. "At the very least, the
   single zoom" on a punchline.
2. **Audio reverb on dramatic words.** Copy the clip's audio to its own track, studio reverb at 100% wet /
   0% dry (room ~88, decay ~8 s, early reflections 55, width 55), on a track-level effect so the tail rings
   on after the word ends. The dry voice stays as is; the wet tail is layered under it.
3. **Twist face.** Twirl distortion centred on the nose, small radius (just the face), angle 0 to ~94 over a
   few frames; often combined with a zoom.
4. **Face warp.** Puppet pins on eyebrows/mouth (mostly thumbnails, sometimes video).
5. **Blend modes.** Overlay a second copy of the footage (scaled, moved to the side) with Lighten etc.
6. **Boosted audio.** A sound or music hit gained +30 dB so it distorts, then turned DOWN so it only peaks a
   little. Never blow out ears.
Also: "a lot of jump cuts, a lot of black and white, a lot of colour effects."

**"How To Edit Like Pewdiepie"**, Javier Mercedes, 2019 (youtube.com/watch?v=AQQF3UpnDIM): the
**head-shake zoom** is done by hand: scale in (~250% to 350%), keyframe position every couple of frames
to keep the eyes centred as the head moves, plus motion blur (shutter angle 180) to accentuate the shake.
The "hmm" twirl is the same twirl effect, keyframed.

**Throw gags** (StudioBinder, whip-pan guides): whip-pan in the SAME direction the object travels,
trim to the motion blur, land on the next shot. In post: slide/scale the frame with motion blur.

**Comedy pacing** (AIR Media-Tech): fast zoom-in on the joke, freeze frames, quick reaction cuts, a held
awkward beat before the next cut, SFX sparingly (overuse backfires), cut music abruptly for timing.

**Glitch on the person only:** RGB split = duplicate the layer per colour channel, Add/screen blend,
jitter each copy's position; to keep it on the person, apply it through a roto matte of the subject.

## Rules for Manit's videos (from his feedback)
- Hard cuts and snap zooms that follow his head; tilt slightly; no springy bounce animations.
- "Grey" = the whole picture goes black-and-white for a beat (not a grey background).
- Echo/reverb on punchline words, wet tail only, ringing past the word.
- Throw: props fly off-screen, the camera follows them, they hit a trash can, it explodes (quick flash +
  shake), hard cut to the next line.
- Glitch: only HE glitches (cutout + RGB split/slice jitter), with a glitch sound. No cracked screen.
- Text: plain white, black outline (meme/Impact style), hard cut in. No company colours, no boxes.
- Captions throughout: white, black outline, 2-4 words; the word being spoken turns yellow (#FFE11A) and moves word by word (Manit, Draft 3).
- Hats/props: drawn in code (Draft 1 shapes, plain colours, no labels), pinned to the face track. Photo cutouts were rejected in Draft 2.
- Claude Code reveal: a terminal animation where he types the request and Claude starts making the video (Manit preferred this to a real screenshot in Draft 3). Steps shown must be ones that really happened.
- Punchline beats (B&W + echo, the bin explosion) should last about 0.7 s, not 0.5 s (hold a freeze frame).
- Syncrowin: music being chosen after Draft 3 (was none in Draft 2).
- Infosys Draft 2 (Manit: "love it"): effects move where his eyes and hands go (the robot rises to where he looks and
  the camera tilts and pushes in to follow it); punchline beats use his real stare in B&W + echo, not a frozen frame;
  literal gags for key lines (shot shrinks into a phone, robot drives out on "leave the screen"); real photo cut-outs
  with a white sticker outline for company things (Rally) are fine.

## Sources
- https://www.youtube.com/watch?v=N06nBy6OzHs
- https://www.youtube.com/watch?v=AQQF3UpnDIM
- https://studiobinder.com/blog/swish-pan-whip-pan-definition-film
- https://nofilmschool.com/how-to-do-a-whip-pan
- https://air.io/youtube-hacks/editing-tricks-for-fast-paced-funny-videos
- https://nofilmschool.com/2017/10/how-create-rgb-split-effect-after-effects
- https://www.instrumentalbackgroundmusic.com/blog/how-pewdiepie-uses-music-in-his-videos-to-engage-viewers/
