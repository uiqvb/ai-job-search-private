"""Infosys-only sounds (generated, no downloads): tennis thock, ta-daah, echo tail on "right".
Writes public/sfx/thock.wav, tada.wav, echo_right.wav."""
import numpy as np, scipy.io.wavfile as wav, scipy.signal as sg, os, subprocess
SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "public", "sfx")
rng = np.random.default_rng(11)
t_ = lambda d: np.arange(int(SR * d)) / SR
def save(n, x, g=0.9):
    x = x / (np.max(np.abs(x)) + 1e-9) * g; f = int(0.004 * SR); x[-f:] *= np.linspace(1, 0, f)
    wav.write(os.path.join(OUT, n + ".wav"), SR, (x * 32767).astype(np.int16))
def lp(x, f): b, a = sg.butter(2, f / (SR / 2)); return sg.lfilter(b, a, x)
def bp(x, lo, hi): b, a = sg.butter(2, [lo / (SR / 2), hi / (SR / 2)], "band"); return sg.lfilter(b, a, x)

# tennis ball hit: hollow body tone + strings ping + felt noise click
d = 0.35; t = t_(d)
body = np.sin(2 * np.pi * (420 * np.exp(-t * 9) + 180) * t) * np.exp(-t * 28)
ping = np.sin(2 * np.pi * 1250 * t) * np.exp(-t * 45) * 0.35
click = bp(rng.standard_normal(len(t)), 900, 4500) * np.exp(-t * 160) * 1.2
save("thock", body + ping + click, 0.85)

# ta-daaah: two brass hits (short G4, then long C major chord with vibrato), sawtooth + lowpass swell
def brass(freqs, d, swell=0.06, vib=0.0):
    t = t_(d); out = np.zeros_like(t)
    for f in freqs:
        ph = 2 * np.pi * np.cumsum(f * (1 + vib * np.sin(2 * np.pi * 5.5 * t) * np.minimum(1, t / 0.4))) / SR
        saw = sum(np.sin(k * ph) / k for k in range(1, 14))
        out += saw
    a = np.minimum(1, t / swell); r = np.minimum(1, (d - t) / 0.25)
    bright = lp(out, 2600) * 0.7 + lp(out, 900) * 0.6
    return bright * a * r
ta = brass([392.0, 493.9], 0.2, 0.02)
daah = brass([523.3, 659.3, 784.0, 1046.5], 1.7, 0.05, 0.006)
gap = np.zeros(int(0.05 * SR))
x = np.concatenate([ta, gap, daah]); x = x + 0.25 * np.concatenate([np.zeros(int(0.03 * SR)), x[:-int(0.03 * SR)]])
save("tada", np.tanh(x * 0.6), 0.85)

# echo tail of "right": cut the word from the track, wet-only reverb + three slap echoes (dry stays in the track)
S0, S1 = 17.48, 17.86
raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(S0), "-t", str(S1 - S0), "-i", os.path.join(HERE, "public", "th", "track.mp4"),
                      "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True).stdout
w = np.frombuffer(raw, np.int16).astype(float) / 32768
ir_t = t_(3.0); ir = rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 1.9); ir = lp(ir, 5000)
wet = sg.fftconvolve(w, ir)[: int(3.2 * SR)]
slap = np.zeros(int(3.2 * SR))
for k, (dt, g) in enumerate([(0.22, 0.55), (0.44, 0.32), (0.66, 0.18)]):
    i = int(dt * SR); slap[i:i + len(w)] += w[: len(slap) - i] * g
y = wet / (np.max(np.abs(wet)) + 1e-9) * 0.6 + slap
save("echo_right", y, 0.75)
print("ok")
