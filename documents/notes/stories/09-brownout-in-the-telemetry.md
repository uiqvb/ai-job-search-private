# 09. The Brownout I Found in the Telemetry

**Hook:** I traced an intermittent brownout to a failing buck converter using boot identifiers
and reset causes in the telemetry, not a multimeter.

**Used in:** CSIRO (as the evidence behind "I have not used ROS, but I have the substrate
underneath it"). Held as interview material in the README rather than a resume bullet.

**Best for:** debugging depth, embedded and hardware-adjacent work, observability, any question
about a hard bug.

---

## The story

- The system ran MQTT publish and subscribe topics carrying JSON telemetry on a fixed interval,
  between a microcontroller and a Python supervisor.
- That telemetry was logged.
- An intermittent brownout was then debugged **from the record rather than from the hardware**,
  using `bootId` and `resetCause` fields in the telemetry. The cause was a failing buck
  converter.

## The idea worth stating

That is the same instinct a bag file rewards. If the telemetry carries the right fields, the
record can answer questions the hardware cannot easily be made to reproduce.

## What it evidences

- Instrumenting a system so that intermittent faults become diagnosable
- Preferring evidence over reproduction attempts
- Genuine hardware and software boundary experience without overclaiming a robotics stack

## Length variants

**One line.** I traced an intermittent brownout to a failing buck converter using boot ids and
reset causes in my telemetry rather than a multimeter.

**Short.** My robot published JSON telemetry over MQTT on a fixed interval to a Python
supervisor, and that telemetry was logged. When an intermittent brownout appeared, I traced it to
a failing buck converter using the boot identifiers and reset causes in the log rather than a
multimeter. Debugging from the record rather than from the hardware is the same instinct a bag
file rewards.

## Facts and verification

- Listed in `../CLAUDE.md` under "Held back as interview material, not bullets", described as
  "the buck-converter fix proved via `bootId`/`resetCause` telemetry rather than a multimeter",
  and marked verified.
- Pairs with the other held-back item, the timestamp-skew bug that silently disabled lease
  expiry, which is a good second answer if an interviewer asks for another one.

## Do not say

- Anything implying ROS bag file experience. The comparison in the CSIRO letter is explicitly an
  analogy, made in the same paragraph that admits no ROS experience. See `10-naming-the-ros-gap.md`.
