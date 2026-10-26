# 07. Making the Rain Sensor Prove Itself

**Hook:** The least reliable component in the system was allowed to be wrong, as long as it had
to agree with something else first.

**Used in:** CSIRO (Technology 14, alongside the grass traversability case study).

**Best for:** sensor fusion, reliability, embedded work, data quality, anything about trusting or
not trusting a signal.

---

## The story

- On the smart clothesline robot, the rain sensor was the least reliable component in the system.
- One bad reading had real consequences either way: shelter the washing on a clear day, or leave
  it out in a downpour.
- Rather than let a single reading decide, I made it agree with **Open-Meteo forecast data**
  before the robot committed to moving.

## The idea worth stating

Treating a signal as **conditionally reliable rather than absolutely** reliable. In the CSIRO
letter this is used to rhyme with treating grass as conditionally traversable rather than always
fatal. That is the transferable claim, and it is the reason this small story earns space next to
much bigger ones.

## What it evidences

- Recognising which component in a system is the weak link, before it fails in the field
- Designing around unreliability instead of assuming it away
- Cross-source validation as a cheap fix

## Length variants

**One line.** The rain sensor was the least reliable part of my clothesline robot, so I made it
agree with Open-Meteo forecast data before the robot would act on it.

**Short.** On the clothesline robot the rain sensor was the least reliable component, and one bad
reading could shelter the washing on a clear day or leave it out in a downpour. Rather than let a
single reading decide, I made it agree with Open-Meteo forecast data before the robot committed
to moving. Treating a signal as conditionally reliable rather than absolutely is a habit I have
kept.

## Facts and verification

From `../CLAUDE.md` (Smart Clothesline Robot entry) and the CSIRO letter:

- Sensors on the robot: infrared, light and rain. Arduino Nano, Raspberry Pi, Python/Flask, MQTT,
  I2C, systemd. Demo video and code linked in CLAUDE.md.
- Open-Meteo cross-check: stated in the CSIRO letter. **Verify against the actual sketch and Pi
  service before reusing**, per the standing rule that nothing gets written from memory.

## Do not say

- That it was a machine learning or predictive model. It is a cross-check against a forecast API.
