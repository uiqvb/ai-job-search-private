"""Draft 4: a bigger, boomier explosion (Manit: 'bigger and boomier'). Writes public/sfx/boom_big.wav."""
import numpy as np, scipy.signal as sg
from sfx import SR, save, env, lp, hp, bp, sweep, noise, t_, rng

D = 2.6
n = int(SR * D)
def pad(x, at=0.0):
    y = np.zeros(n); i = int(at * SR); y[i:i + len(x)] = x[: n - i]; return y

crack = pad(hp(noise(0.05), 900) * env(0.05, 0.001, 60) * 0.9)                 # the hit
thump1, _ = sweep(110, 38, 0.5, 0.5); thump1 = pad(thump1 * env(0.5, 0.002, 7) * 1.4)
thump2, _ = sweep(80, 30, 0.6, 0.6); thump2 = pad(thump2 * env(0.6, 0.004, 5) * 1.2, 0.07)  # second layer
sub, _ = sweep(62, 24, D, 0.7); sub = sub * env(D, 0.01, 1.6) * 1.3              # long sub drop
body = pad(lp(noise(1.4), 420, 4) * env(1.4, 0.003, 3.2) * 2.4)                  # fireball roar
roll = 0.6 + 0.4 * np.sin(2 * np.pi * 3.3 * t_(D)) * np.sin(2 * np.pi * 1.7 * t_(D) + 1)
rumble = lp(noise(D), 160, 4) * env(D, 0.05, 1.2) * roll * 3.0                    # rolling rumble
debris = pad(bp(noise(1.2), 2000, 6000) * env(1.2, 0.02, 4) * 0.15, 0.12)

dry = crack + thump1 + thump2 + sub + body + rumble + debris
ir = rng.standard_normal(int(0.7 * SR)) * np.exp(-np.arange(int(0.7 * SR)) / SR * 6)
wet = sg.fftconvolve(lp(dry, 2500), ir)[:n]
mix = dry + wet / np.max(np.abs(wet)) * np.max(np.abs(dry)) * 0.35
mix = np.tanh(mix / np.max(np.abs(mix)) * 2.6)                                    # warm saturation
save("boom_big", mix, 0.95)
print("ok")
