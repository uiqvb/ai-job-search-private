"""Soft chord pad for the background. Quiet on purpose. Run: python make_music.py <seconds>"""
import sys, wave, numpy as np
sr = 44100
dur = float(sys.argv[1])
t = np.arange(int(sr * dur)) / sr
n = lambda m: 440 * 2 ** ((m - 69) / 12)
chords = [[48, 55, 60, 64, 71], [45, 52, 57, 60, 67], [41, 48, 57, 60, 64], [43, 50, 55, 62, 69]]  # Cmaj7 Am7 Fmaj7 G
bar = 8.0
out = np.zeros_like(t)
for k in range(int(dur // bar) + 1):
    ch = chords[k % 4]
    a, b = k * bar, (k + 1) * bar + 2.0
    m = (t >= a) & (t < b)
    tt = t[m] - a
    env = np.minimum(1, tt / 2.0) * np.clip((b - a - tt) / 2.0, 0, 1)
    sig = np.zeros_like(tt)
    for note in ch:
        fq = n(note)
        sig += np.sin(2 * np.pi * fq * tt) + 0.5 * np.sin(2 * np.pi * fq * 1.003 * tt) + 0.15 * np.sin(2 * np.pi * fq * 2 * tt)
    out[m] += sig * env
# gentle pluck on each beat for a bit of life
for k in range(int(dur / 1.0)):
    st = k * 1.0
    m = (t >= st) & (t < st + 0.6)
    tt = t[m] - st
    ch = chords[int(st // bar) % 4]
    fq = n(ch[(k % 3) + 2] + 12)
    out[m] += 0.6 * np.sin(2 * np.pi * fq * tt) * np.exp(-tt * 7)
out *= (0.6 + 0.4 * np.sin(2 * np.pi * 0.08 * t)) ** 1
out = out / np.max(np.abs(out)) * 0.7
fade = np.minimum(1, np.minimum(t / 2, (dur - t) / 3))
out *= fade
pcm = (np.stack([out, out], 1) * 32767).astype(np.int16)
with wave.open("public/music.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())
print("ok")
