"""Original lo-fi track, written for this video so there is no copyright owner but Manit.

Same style as the Pixabay track it replaces (B-flat minor / D-flat major, ~72 BPM, warm and
low-passed), but the chords, bassline, drums and melody are all written here from scratch.
The structure is timed to the video:
  0:00   soft keys only
  7.75s  drums + bass drop in ("I built robots")
  75.0s  breakdown to a quiet pad (grandfather)
  90.2s  full groove returns ("I saw a video of Abi")
  125s   end card: drums stop, last chord rings
Run: python make_music_v2.py  ->  public/music/original.wav
"""
import json, os, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

HERE = os.path.dirname(os.path.abspath(__file__))
tl = json.load(open(os.path.join(HERE, "src", "timeline.json"), encoding="utf-8"))
SR = 44100
TOTAL = tl["total"] + 0.2
DROP = 7.75
RETURN = 90.2
BREAK = 75.0
END = tl["endCardStart"]
BAR = (RETURN - DROP) / 25          # 25 whole bars between drop and return -> ~72.8 BPM
BEAT = BAR / 4
rng = np.random.default_rng(7)
N = int(TOTAL * SR)
t_all = np.arange(N) / SR

def midi(m): return 440.0 * 2 ** ((m - 69) / 12)

def lp(x, hz, order=2): return sosfilt(butter(order, hz, "low", fs=SR, output="sos"), x)
def hp(x, hz, order=2): return sosfilt(butter(order, hz, "high", fs=SR, output="sos"), x)
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], "band", fs=SR, output="sos"), x)

def add(buf, start, sig, gain=1.0):
    i = int(start * SR)
    if i >= len(buf) or i + len(sig) <= 0: return
    j = min(len(buf), i + len(sig))
    s = max(0, -i)
    buf[max(i, 0):j] += sig[s:s + j - max(i, 0)] * gain

# ---------- chords (my own progression: Bbm9 - Gbmaj7 - Ebm9 - Ab13sus) ----------
CHORDS = [
    (46, [61, 65, 68, 72]),   # Bbm9:  Db F Ab C
    (42, [58, 61, 65, 70]),   # Gbmaj7: Bb Db F Bb
    (39, [58, 61, 65, 66]),   # Ebm9:  Bb Db F Gb
    (44, [60, 63, 66, 70]),   # Ab13sus: C Eb Gb Bb
]

def bar_start(k): return DROP + k * BAR          # k can be negative (intro bars)
def chord_at(k): return CHORDS[k % 4]

# ---------- instruments ----------
def ep_note(f, dur, vel=0.5):
    """Electric piano: two-operator FM with a bell-ish tine that decays."""
    n = int((dur + 1.8) * SR); t = np.arange(n) / SR
    idx = 1.6 * np.exp(-t * 3.5) + 0.25
    mod = np.sin(2 * np.pi * f * t) * idx
    tine = 0.18 * np.sin(2 * np.pi * f * 14 * t) * np.exp(-t * 18)
    car = np.sin(2 * np.pi * f * t + mod) + tine
    env = np.minimum(1, t / 0.006) * np.exp(-t * 1.3)
    rel = np.clip((dur + 1.8 - t) / 0.4, 0, 1)
    return car * env * rel * vel

def bass_note(f, dur, vel=0.8):
    n = int((dur + 0.15) * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)
    env = np.minimum(1, t / 0.01) * np.clip((dur + 0.15 - t) / 0.12, 0, 1) * (0.75 + 0.25 * np.exp(-t * 4))
    return s * env * vel

def kick(vel=1.0):
    n = int(0.45 * SR); t = np.arange(n) / SR
    f = 48 + 70 * np.exp(-t * 30)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) * np.exp(-t * 7.5) + 0.3 * rng.standard_normal(n) * np.exp(-t * 300)) * vel

def snare(vel=0.6):
    n = int(0.3 * SR); t = np.arange(n) / SR
    noise = bp(rng.standard_normal(n), 1200, 6000) * np.exp(-t * 16)
    tone = np.sin(2 * np.pi * 185 * t) * np.exp(-t * 25)
    return (noise * 0.9 + tone * 0.6) * vel

def hat(vel=0.25, open_=False):
    n = int((0.16 if open_ else 0.05) * SR); t = np.arange(n) / SR
    return hp(rng.standard_normal(n), 7000) * np.exp(-t * (25 if open_ else 90)) * vel

def pad(freqs, dur, vel=0.12):
    n = int(dur * SR); t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 1.004 * t) for f in freqs)
    env = np.minimum(1, t / 1.2) * np.clip((dur - t) / 1.2, 0, 1)
    return lp(s, 1400) * env * vel

def lead_note(f, dur, vel=0.18):
    n = int((dur + 0.4) * SR); t = np.arange(n) / SR
    vib = 1 + 0.004 * np.sin(2 * np.pi * 5 * t) * np.minimum(1, t / 0.3)
    ph = 2 * np.pi * f * np.cumsum(vib) / SR
    s = np.sin(ph) + 0.15 * np.sin(2 * ph) + 0.05 * np.sin(3 * ph)
    env = np.minimum(1, t / 0.04) * np.clip((dur + 0.4 - t) / 0.35, 0, 1) * np.exp(-t * 0.6)
    return s * env * vel

# ---------- arrange ----------
keys = np.zeros(N); bass = np.zeros(N); drums = np.zeros(N); padb = np.zeros(N); lead = np.zeros(N)
SWING = 0.58

def groove(k):
    t0 = bar_start(k)
    return (DROP <= t0 < BREAK - 0.01) or (RETURN <= t0 < END - 0.01)

first_bar = int(np.floor(-DROP / BAR))
last_bar = int(np.ceil((TOTAL - DROP) / BAR))
for k in range(first_bar, last_bar):
    t0 = bar_start(k)
    root, notes = chord_at(k)
    in_break = BREAK - 0.01 <= t0 < RETURN - 0.01
    in_end = t0 >= END - 0.01
    if in_break:
        padb_sig = pad([midi(n) for n in notes] + [midi(root + 12)], BAR + 1.2)
        add(padb, t0, padb_sig)
        continue
    if in_end:
        if t0 < END + BAR:   # one last ringing chord on the end card
            for i, n in enumerate(notes):
                add(keys, t0 + i * 0.03, ep_note(midi(n), 3.0, 0.42))
        continue
    # keys: hit on 1, and on the "and" of 2 (lo-fi push), slightly strummed
    for hit, vel, dur in ((0.0, 0.5, 1.4), (1.5 + (SWING - 0.5), 0.34, 1.8)):
        for i, n in enumerate(notes):
            add(keys, t0 + hit * BEAT + i * 0.012, ep_note(midi(n), dur * BEAT, vel * rng.uniform(0.9, 1.05)))
    if groove(k):
        # bass: root on 1, fifth pickup, root again
        add(bass, t0, bass_note(midi(root), 1.4 * BEAT))
        add(bass, t0 + 2.5 * BEAT, bass_note(midi(root + 7), 0.45 * BEAT, 0.6))
        add(bass, t0 + 3.0 * BEAT, bass_note(midi(root), 0.9 * BEAT, 0.7))
        # drums: boom-bap
        for b, v in ((0, 1.0), (1.75, 0.55), (2.5, 0.8)):
            add(drums, t0 + b * BEAT, kick(v))
        for b in (1, 3):
            add(drums, t0 + b * BEAT, snare(0.55 * rng.uniform(0.9, 1.05)))
        for e in range(8):
            off = (e % 2) * (SWING - 0.5) * BEAT
            add(drums, t0 + e * 0.5 * BEAT + off, hat(0.22 * (1.0 if e % 2 == 0 else 0.65) * rng.uniform(0.8, 1.1), open_=(e == 7 and k % 2 == 1)))

# a short original melody, used sparingly (Db major pentatonic)
PHRASE = [(0.0, 77, 0.75), (1.0, 80, 0.5), (1.5, 82, 1.0), (3.0, 80, 0.5), (3.5, 77, 1.5),
          (6.0, 75, 0.5), (6.5, 77, 0.5), (7.0, 73, 2.0)]   # beats, midi, length in beats
def phrase(at):
    for b, m, l in PHRASE:
        add(lead, at + b * BEAT, lead_note(midi(m), l * BEAT))
for k in (8, 16, 27, 33):            # bar numbers after the drop, inside the grooves
    if groove(k):
        phrase(bar_start(k))

# soft swell into the drop and into the return
for at in (DROP, RETURN):
    n = int(1.6 * SR); t = np.arange(n) / SR
    sw = hp(rng.standard_normal(n), 2500) * (t / 1.6) ** 3 * 0.06
    add(drums, at - 1.6, sw)

# ---------- mix ----------
# sidechain feel: keys and bass dip slightly on each kick
duck = np.ones(N)
for k in range(first_bar, last_bar):
    if groove(k):
        for b in (0, 1.75, 2.5):
            i = int((bar_start(k) + b * BEAT) * SR); n = int(0.28 * SR)
            if 0 <= i < N:
                seg = 1 - 0.3 * np.exp(-np.arange(min(n, N - i)) / SR * 9)
                duck[i:i + len(seg)] = np.minimum(duck[i:i + len(seg)], seg)

# tape wow on the keys (slow pitch wobble via resampling)
wow = 0.0018 * np.sin(2 * np.pi * 0.45 * t_all)
idx = np.clip(np.arange(N) + np.cumsum(wow) * SR / 50, 0, N - 1)
keys = np.interp(idx, np.arange(N), keys)

ir_t = np.arange(int(1.4 * SR)) / SR
ir = rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 3.2); ir /= np.sqrt((ir ** 2).sum())
def verb(x, wet): return x + wet * fftconvolve(x, ir)[:len(x)]

keys = verb(lp(keys, 3800), 0.35) * duck
padb = verb(padb, 0.5)
lead = verb(lp(lead, 3500), 0.45)
bass = lp(bass, 220) * duck
drums = lp(drums, 9000)

mix = 0.55 * keys + 0.8 * bass + 0.7 * drums + 0.9 * padb + 0.6 * lead
# vinyl crackle + hiss
crackle = np.zeros(N); pops = rng.integers(0, N, size=int(TOTAL * 9))
crackle[pops] = rng.uniform(-1, 1, len(pops)) * 0.25
mix += hp(crackle, 1500) + 0.004 * lp(rng.standard_normal(N), 5000)
mix = lp(mix, 6500)                         # warm, rolled-off top like the original
fade = np.minimum(1, t_all / 1.0) * np.clip((TOTAL - t_all) / 2.0, 0, 1)
mix *= fade
mix /= np.max(np.abs(mix)) / 0.89

# light stereo width: keys/pad slightly delayed on one side
d = int(0.012 * SR)
side = np.concatenate([np.zeros(d), (0.55 * keys + 0.9 * padb)[:-d]]) / np.max(np.abs(mix) + 1e-9) * 0.0
L, R = mix, mix.copy()
R[d:] = 0.85 * mix[d:] + 0.15 * mix[:-d]
pcm = (np.stack([L, R], 1) * 32767).astype(np.int16)
os.makedirs(os.path.join(HERE, "public", "music"), exist_ok=True)
with wave.open(os.path.join(HERE, "public", "music", "original.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print(f"ok  {TOTAL:.1f}s  bar {BAR:.3f}s  ~{240 / BAR:.1f} BPM")
