# Infosys intro video: script (v3)

For the Infosys InStep International Internship in GenAI, Robotics & Machine Learning (Melbourne,
from 18 Jan 2027). Email the link to Saloni Agarwal (the cover letter says a video is included).
About 1:40.

**One story, told properly:** the Smart Clothesline Robot (IoT, Python, hardware) and the random
resets he traced with telemetry.
**Why it fits Infosys:** InStep's robotics and IoT projects, and MatchFeel at the Australian Open 2026
(a magnetic ring traces the ball across engraved court lines so blind and visually impaired fans can
follow a match by touch; verified from the 28 Jan 2026 release).

Facts check: all in `01-candidate-profile.md` and `company_research/infosys.json`. Do not say the
resets stopped after a fix or that batteries were bought; only that the telemetry traced the fault to
a failing voltage (buck) converter.

**Before editing this script, read `../SCRIPT-RULES.md`.**

---

## FILMING VERSION (v3, ~230 words). Speak it like you're telling a friend.

**1. Hook** (to camera)
"My first robot kept switching itself off. At random. And I had no idea why."

**2. Who I am** (to camera)
"Hi, I'm Manit. I'm in my third year of Software Engineering at Deakin, and I'd love to join InStep
this summer."

**3. The setup** (with the clothesline robot)
"That robot was my smart clothesline. The idea is simple: if rain pours, it autonomously moves to
shelter, and when it's sunny, it turns toward the light. It's powered by an Arduino that reads the
sensors and drives the motors, and a Raspberry Pi running Python sends it commands over MQTT."

**4. The problem** (with the robot, slower)
"But halfway through a run, it would just reset. Instead of guessing why, I made the robot tell me.
Every time it booted, it reported the reason it had restarted. After enough restarts, those reports
all pointed to one part: a failing voltage converter."

**5. How it turned out** (to camera)
"That robot ended up scoring 93. Later, I connected it to my own backend, so a server could drive it."

**6. Why Infosys** (to camera)
"Connecting software to something physical is what I enjoy most, and it's why MatchFeel at the
Australian Open stuck with me. With MatchFeel, a magnetic ring traces the ball across the court, so
blind and visually impaired fans can follow the match by touch. It takes live data and turns it into
something a person can feel. That's the kind of work I want to do at InStep. I haven't trained a
machine learning model yet, and that's exactly what I'd love to learn from your mentors."

**7. Close** (to camera, warm)
"Thanks for watching. I hope we get to talk soon."
Hold two seconds for the end card.

---

## Shot list (approx. timings; re-timed to the real takes after filming)

Source timings are the same in `broll/cuts/` and `broll/originals/`. Split = footage in the top half,
you in the bottom half. Text never sits on your face. One idea on screen at a time.

| Video time | You say                                                             | Footage (source @ time in source)                                                                             | Animation                                                                                                         |
| ---------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| 0:00-0:06  | Hook                                                                | Face only                                                                                                     | Power icon flickers off and on, top of frame                                                                      |
| 0:06-0:15  | Who I am                                                            | Face only                                                                                                     | Name tag at 0:07: *Manit Khera / Software Engineering student, Deakin University*                               |
| 0:15-0:19  | "That robot was my smart clothesline."                              | Split: [clothesline.mp4 @ 1:04-1:08](../broll/cuts/clothesline.mp4) (robot following its line, wide)           | none                                                                                                              |
| 0:19-0:27  | "...if rain pours, it autonomously moves to shelter... turns toward the light"  | Split: [clothesline.mp4 @ 1:28-1:35](../broll/cuts/clothesline.mp4) (hand holding the cardboard shade over it) | Small icons: rain cloud → shelter arrow, sun → light arrow                                                      |
| 0:27-0:32  | "It's powered by an Arduino that reads the sensors and drives the motors"                | Split: [clothesline.mp4 @ 0:32-0:37](../broll/cuts/clothesline.mp4) (robot close-up)                           | Chip: **ARDUINO**                                                                                           |
| 0:32-0:38  | "...a Raspberry Pi running Python sends it commands over MQTT"      | Split: [clothesline.mp4 @ 0:00-0:06](../broll/cuts/clothesline.mp4) (live dashboard on the laptop)             | **PYTHON ON A PI → MQTT → ROBOT**, arrow animates                                                         |
| 0:38-0:43  | "But halfway through a run, it would just reset." | Face only                                                                                                     | Section tag: **WHEN IT BROKE**                                                                              |
| 0:43-0:52  | "Instead of guessing why, I made the robot tell me. Every time it booted..."       | Split: [clothesline.mp4 @ 0:08-0:17](../broll/cuts/clothesline.mp4) (dashboard close-up)                       | Boot markers stack up one by one: **RESTART → REASON**, **RESTART → REASON**                        |
| 0:52-0:59  | "...those reports all pointed to one part: a failing voltage converter"      | Split: [clothesline.mp4 @ 0:23-0:27](../broll/cuts/clothesline.mp4) (hand on the robot and battery pack)       | Label: **THE CULPRIT: VOLTAGE CONVERTER**                                                                   |
| 0:59-1:03  | "That robot ended up scoring 93."                                        | Split: [clothesline.mp4 @ 0:36-0:40](../broll/cuts/clothesline.mp4) (robot on its line)                        | Pop: **93**                                                                                                 |
| 1:03-1:07  | "...connected it to my own backend, so a server could drive it"     | Split: [drive.mp4 @ 0:03-0:07](../broll/cuts/drive.mp4) (driving it from the dashboard)                        | none                                                                                                              |
| 1:07-1:10  | "Connecting software to something physical is what I enjoy most... MatchFeel stuck with me."        | Face only                                                                                                     | none                                                                                                              |
| 1:10-1:20  | "A magnetic ring traces the ball... follow the match by touch"      | Face, with an animation in the top half (no Infosys or AO footage)                                            | Simple court line drawing: ball dot moves, a ring follows it, vibration ripples spread. Label **MATCHFEEL** |
| 1:20-1:26  | "It takes live data and turns it into something a person can feel."          | Face only                                                                                                     | none (let it land)                                                                                                |
| 1:26-1:32  | "I haven't trained a machine learning model yet..."                 | Face only                                                                                                     | Tag: **NEXT: MACHINE LEARNING**                                                                             |
| 1:32-1:37  | Close                                                               | Face only                                                                                                     | none                                                                                                              |
| 1:37-1:41  | (hold)                                                              | End card                                                                                                      | Name, email, LinkedIn, "Thanks for watching"                                                                      |

Colours: Infosys blues (check brand colours before the graphics pass). Music: a YouTube Audio Library
track different from the Capgemini one (pick before the music pass).
