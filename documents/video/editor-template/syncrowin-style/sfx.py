"""Synthesise every sound effect for the Syncrowin video (no downloads, all generated here).
Writes 48 kHz mono WAVs into public/sfx/."""
import numpy as np, scipy.io.wavfile as wav, scipy.signal as sg, os
SR = 48000
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "sfx")
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(7)
t_ = lambda d: np.arange(int(SR * d)) / SR

def save(name, x, gain=0.9):
    x = np.asarray(x, dtype=np.float64)
    x = x / (np.max(np.abs(x)) + 1e-9) * gain
    fade = min(len(x), int(0.004 * SR)); x[-fade:] *= np.linspace(1, 0, fade)
    wav.write(os.path.join(OUT, name + ".wav"), SR, (x * 32767).astype(np.int16))

def env(d, a=0.005, decay=8.0):
    t = t_(d); e = np.exp(-t * decay); na = max(1, int(a * SR)); e[:na] *= np.linspace(0, 1, na); return e

def bp(x, lo, hi, order=2):
    b, a = sg.butter(order, [lo / (SR / 2), hi / (SR / 2)], "band"); return sg.lfilter(b, a, x)

def lp(x, f, order=2):
    b, a = sg.butter(order, f / (SR / 2)); return sg.lfilter(b, a, x)

def hp(x, f, order=2):
    b, a = sg.butter(order, f / (SR / 2), "high"); return sg.lfilter(b, a, x)

def sweep(f0, f1, d, curve=1.0):
    t = t_(d); f = f0 + (f1 - f0) * (t / d) ** curve; return np.sin(2 * np.pi * np.cumsum(f) / SR), f

def noise(d): return rng.standard_normal(int(SR * d))

# pop: quick pitch-drop bubble
s, _ = sweep(900, 220, 0.09, 0.6); save("pop", s * env(0.09, 0.002, 30))
# ding: bell partials
t = t_(1.2); ding = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, a, k in [(1568, 1, 3.5), (3136, .35, 6), (4704, .18, 9), (2349, .25, 5)])
save("ding", ding * env(1.2, 0.002, 0), 0.7)
# final ding (two notes)
t = t_(1.6); d2 = np.concatenate([ding[: int(0.12 * SR)] * 0.8, np.zeros(int(1.48 * SR))]) + \
    np.concatenate([np.zeros(int(0.12 * SR)), sum(a * np.sin(2 * np.pi * f * t_(1.48)) * np.exp(-t_(1.48) * k) for f, a, k in [(2093, 1, 3), (4186, .3, 6), (3136, .2, 5)])])
save("ding2", d2, 0.7)
# whoosh (toss up): noise through a rising band, swell then fade
d = 0.55; n = noise(d); x = np.zeros_like(n)
for i, (lo, hi) in enumerate(np.linspace([300, 900], [1800, 5200], 12)):
    seg = slice(int(i * len(n) / 12), int((i + 1) * len(n) / 12)); x[seg] = bp(n, lo, hi)[seg]
e = np.sin(np.pi * np.clip(t_(d) / d, 0, 1)) ** 1.6; save("whoosh", x * e, 0.8)
# whip: very short bright swish
d = 0.22; n = hp(noise(d), 1500); e = np.sin(np.pi * t_(d) / d) ** 3; save("whip", n * e, 0.7)
# rocket whistle "weeee": falling slide whistle with vibrato + hiss
d = 2.0; t = t_(d); f = 1900 - 1100 * (t / d) ** 1.3 + 25 * np.sin(2 * np.pi * 7 * t)
wh = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.25 * np.sin(4 * np.pi * np.cumsum(f) / SR)
hiss = hp(noise(d), 3000) * 0.18
e = np.minimum(1, t / 0.08) * (0.7 + 0.3 * t / d); save("rocket", (wh * 0.8 + hiss) * e, 0.75)
# boom: sub drop + crunchy noise burst
d = 2.2; t = t_(d); sub = np.sin(2 * np.pi * np.cumsum(70 * np.exp(-t * 2.5) + 32) / SR) * np.exp(-t * 2.2)
crack = lp(noise(d), 2500) * np.exp(-t * 6) * 0.9; rumble = lp(noise(d), 300) * np.exp(-t * 1.6) * 0.8
boom = np.tanh((sub * 1.2 + crack + rumble) * 2.2); save("boom", boom, 0.95)
# debris tinkle: scattered tiny metallic pings
d = 1.2; x = np.zeros(int(SR * d))
for k in range(14):
    st = int(rng.uniform(0, 0.9) * SR); f = rng.uniform(2500, 6000); L = int(0.08 * SR)
    x[st:st + L] += np.sin(2 * np.pi * f * t_(0.08)) * np.exp(-t_(0.08) * 60) * rng.uniform(.3, 1)
save("tinkle", x, 0.5)
# slam: punchy thump + snap for words
d = 0.35; t = t_(d); thump = np.sin(2 * np.pi * np.cumsum(140 * np.exp(-t * 18) + 55) / SR) * np.exp(-t * 14)
snap = hp(noise(d), 2000) * np.exp(-t * 80) * 0.6; save("slam", np.tanh((thump + snap) * 1.8), 0.85)
# scribble: marker on paper
d = 0.75; t = t_(d); n = bp(noise(d), 1800, 6000); am = 0.55 + 0.45 * np.sin(2 * np.pi * 11 * t) ** 2
save("scribble", n * am * np.minimum(1, t / 0.03) * np.minimum(1, (d - t) / 0.08), 0.45)
# glitch: bit-crushed stutter chops
d = 0.6; x = np.zeros(int(SR * d)); pos = 0
while pos < len(x):
    L = int(rng.uniform(0.02, 0.07) * SR); kind = rng.integers(3); tt = t_(L / SR)
    seg = [np.sign(np.sin(2 * np.pi * rng.uniform(80, 900) * tt)), noise(L / SR), np.sin(2 * np.pi * rng.uniform(1000, 4000) * tt)][kind]
    x[pos:pos + L] = seg[: len(x[pos:pos + L])] * rng.uniform(.4, 1); pos += L
x = np.round(x * 6) / 6; save("glitch", x, 0.55)
# sparkle: rising chime arpeggio
x = np.zeros(int(SR * 0.7))
for i, f in enumerate([1760, 2217, 2637, 3520]):
    st = int(i * 0.06 * SR); L = int(0.4 * SR); x[st:st + L] += np.sin(2 * np.pi * f * t_(0.4)) * np.exp(-t_(0.4) * 9)
save("sparkle", x, 0.5)
# clapperboard clap
d = 0.25; t = t_(d); clap = hp(noise(d), 800) * np.exp(-t * 55) + np.sin(2 * np.pi * 180 * t) * np.exp(-t * 40) * 0.6
save("clap", clap, 0.9)
# record scratch: noise with fast pitch wobble, forward-back
d = 0.5; t = t_(d); base = noise(d); x = np.zeros_like(base)
for i in range(10):
    seg = slice(int(i * len(base) / 10), int((i + 1) * len(base) / 10)); fc = 600 + 2200 * abs(np.sin(i * 1.3)); x[seg] = bp(base, fc * .6, fc * 1.6)[seg]
save("scratch", x * np.minimum(1, t / 0.01) * np.exp(-t * 3), 0.7)
# typing: short clicks at irregular spacing
d = 1.6; x = np.zeros(int(SR * d)); pos = 0
while pos < len(x) - 3000:
    L = int(0.018 * SR); x[pos:pos + L] += hp(noise(0.018), 2500) * np.exp(-t_(0.018) * 300) * rng.uniform(.4, 1)
    pos += int(rng.uniform(0.06, 0.16) * SR)
save("typing", x, 0.4)
# fire ignite: low whoosh + bright flare
d = 0.9; t = t_(d); n = noise(d); fl = lp(n, 1200) * np.minimum(1, t / 0.15) * np.exp(-np.maximum(0, t - 0.15) * 3.5)
fl += hp(n, 2500) * np.exp(-t * 7) * 0.4; save("ignite", fl, 0.8)
# crackle loop: pops on a low roar
d = 6.0; t = t_(d); roar = lp(noise(d), 500) * 0.35; x = roar.copy()
for k in range(160):
    st = int(rng.uniform(0, d - 0.02) * SR); L = int(0.006 * SR); x[st:st + L] += noise(0.006) * np.exp(-t_(0.006) * 600) * rng.uniform(.5, 2.5)
save("crackle", x, 0.5)
# puff: soft low air burst
d = 0.5; t = t_(d); save("puff", lp(noise(d), 900) * np.minimum(1, t / 0.02) * np.exp(-t * 9), 0.7)
# hat pop: cartoon "bloop"
s, _ = sweep(300, 900, 0.12, 1.5); save("bloop", s * env(0.12, 0.003, 18), 0.7)
# tick: soft clock tick
save("tick", hp(noise(0.03), 3000) * np.exp(-t_(0.03) * 250), 0.35)
print("sfx ok:", sorted(os.listdir(OUT)))
