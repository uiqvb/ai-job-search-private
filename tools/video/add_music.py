"""Phase 1, step 5: lay the music under the approved rough cut (Manit's gate 1 watches this file).

    python tools/video/add_music.py documents/video/<company>

project.json "music":
  file        path from the repo root (YouTube Audio Library, or CC BY with the credit line kept)
  volume      base level under speech (about 0.11 = ~11 %)
  music_at    second in the music file where its entry/drop is (A Stroll: 16.25)
  anchor      word in the rough cut that entry should land on: {"word": "robots", "n": 1} or a number
  dips        [{"from": anchor, "to": anchor, "factor": 0.2}]  e.g. under an emotional line
  end_boost   multiplier on the end card (after the last word)
Writes pipeline/rough_cut_music.mp4 (video copied, not re-encoded) and prints the speech/music levels.
"""

import sys

import numpy as np

import vlib


def main(folder):
    pj = vlib.Project(folder)
    m = pj.cfg.get("music")
    if not m:
        sys.exit("no 'music' in project.json")
    src = vlib.REPO / m["file"]
    if not src.exists():
        sys.exit(f"music file not found: {src}")
    words = pj.read_json("rough_words.json")["words"]
    cl = pj.read_json("cut_list.json")
    length = cl["length"]
    end_card = length - float(pj.cfg.get("end_hold", 2.0))
    anchor = vlib.resolve(m.get("anchor", 0), words)
    start = anchor - float(m.get("music_at", 0))          # where music time 0 sits in the track
    vol = float(m.get("volume", 0.11))
    parts = []
    for d in m.get("dips", []):
        a, b = vlib.resolve(d["from"], words), vlib.resolve(d["to"], words)
        parts.append(f"if(between(t,{a:.3f},{b:.3f}),{float(d.get('factor', 0.3))},1)")
    parts.append(f"if(gte(t,{end_card:.3f}),{float(m.get('end_boost', 1.0))},1)")
    expr = f"{vol}*" + "*".join(parts)
    pre = (f"atrim=start={-start:.3f},asetpts=PTS-STARTPTS" if start < 0
           else f"adelay={int(start * 1000)}|{int(start * 1000)}")
    fc = (f"[1:a]aresample=48000,aformat=channel_layouts=stereo,{pre},atrim=end={length:.3f},"
          f"volume='{expr}':eval=frame,afade=t=out:st={max(0, length - 1.2):.3f}:d=1.2[m];"
          f"[0:a][m]amix=inputs=2:duration=first:normalize=0[a]")
    out = pj.path("rough_cut_music.mp4")
    r = vlib.run(["ffmpeg", "-v", "error", "-y", "-i", str(pj.path("rough_cut.mp4")), "-i", str(src),
                  "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                  "-movflags", "+faststart", str(out)])
    if r.returncode:
        sys.exit("ffmpeg failed:\n" + r.stderr[-2000:])
    # levels: speech in the rough cut vs music alone at the same gain
    sp = vlib.rms_db(vlib.audio(pj.path("rough_cut.mp4")))
    speech = float(np.percentile(sp[sp > vlib.speech_threshold(sp)], 70))
    mus = vlib.audio(src, start=max(0, -start), dur=min(30, length))
    music_db = float(np.percentile(vlib.rms_db(mus), 70)) + 20 * np.log10(vol)
    print(f"music entry (music {m.get('music_at', 0)}s) lands at {anchor:.2f}s in the cut; music starts at {max(0, start):.2f}s")
    print(f"speech ~{speech:.1f} dB, music ~{music_db:.1f} dB -> music sits {speech - music_db:.1f} dB under speech "
          f"(Andromeda and Capgemini were approved at volume 0.11 with A Stroll, which measures ~12 dB here; aim ~10-16 dB)")
    print(f"ok {out}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
