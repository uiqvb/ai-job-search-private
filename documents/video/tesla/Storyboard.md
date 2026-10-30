# Tesla intro video: 1-minute storyboard (v2, DRAFT for Manit)

For Tesla, Industrial Product Engineering Intern, Megapack, Energy (Melbourne, job 287709). Applied
23 Oct 2026; the video goes as a follow-up.

**Theme (proposed, check with Manit before filming): ask the data instead of guessing.** Opens on
the Roadster doing a flip, hands off to his robot car failing the same flip, then tells one story in
two beats: (1) he finds a fault from the data, (2) he stops waiting for faults and tests to break it.
That's the role's two halves: diagnose field issues, and test before a site goes live. Lands on the
Megapack fleet. The Roadster is the hook only (SCRIPT-RULES rule 7). The robot car is the
clothesline robot (two-wheel drive, Arduino Nano + Raspberry Pi).
**Running gag: judges' scorecards.** Three plain white Olympic-style cards pop up along the bottom:
Roadster flip 10 · 10 · 10, robot flop 2 · 1 · 0.5, the stress test 10 · 10 · 10 (one card dripping
wet). No Tesla logo or brand colours (`../EDITING-STYLE.md`).
Edit style: old-PewDiePie, human-made: snap zooms, B&W + echo beats, meme text, real photo cutouts,
karaoke captions throughout.

| Time | Pointers (say your way) | Example line | You do | On screen | Sound |
|---|---|---|---|---|---|
| 0:00-0:05 | Okay Tesla · you make the Roadster (say exactly) | "Okay, Tesla. You make the Roadster." | Deadpan. Then **eyes follow it**: look to **your left** (viewer's right), then **up**, then over to **your right** (viewer's left), about 3 s | A Roadster photo cutout flies in from the **viewer's right**, arcs **up over your head doing a full flip**, and comes down on the **viewer's left**. The motion is timed to your eyes (left, up, right). Scorecards pop up: **10 · 10 · 10** | A goofy **human-made mouth "nyoooom" plane sound** under the whole flight (rising on the way up, falling on the way down), then a short crowd cheer |
| 0:05-0:09 | I made a car too · slightly smaller (say exactly) | "I made a car too. It's slightly smaller." | Small grin, then hold still and look slightly down, 2 s | `broll/cuts/stills/robot.png` cut out, tries the same flip, gets halfway, flops on its back with its wheels spinning. Scorecards: **2 · 1 · 0.5** | Record scratch, sad trombone |
| 0:09-0:11 | Doesn't do flips (say exactly) | "And it doesn't do flips." | **Straight face**, hold 1 s | **B&W + echo on "flips"**, freeze 0.7 s | Echo tail |
| 0:11-0:19 | Manit · third-year SE, Deakin · laundry under cover when it rains · firmware I wrote, on an Arduino | "I'm Manit, a third-year Software Engineering student at Deakin. I built it to carry the laundry under cover when it rains. It runs firmware I wrote, on an Arduino." | Just talk | Hard cut back to colour. Split screen: `broll/cuts/clothesline.mp4 @ 0:52` (robot following its line) top half, you bottom half. Small label "MY FIRMWARE" points at the robot | Light rain |
| 0:19-0:25 | Data to a Pi running Linux, every 5 s · but it kept restarting · at random | "It sends its data to a Raspberry Pi running Linux, every five seconds. But every so often, it would just restart. At random." | Straight face on "At random" | A small telemetry log (white monospace lines) scrolls in the corner. On "restart" the whole frame blinks off and back on, like a reboot | Power-down whine, click |
| 0:25-0:34 | Could've swapped parts · went back through the data · boot ID + reset cause · failing buck converter | "I could have swapped parts until it stopped. Instead, I went back through the data. The boot ID and reset cause pointed to the power dropping out, and that led me to a failing buck converter." | **Tap your temple** on "the data" | The log freezes; "bootId" and "resetCause" get circled in red, meme style. Cut to `broll/cuts/clothesline.mp4 @ 0:19` (hand on the robot), red circle + "FOUND IT" | Marker scribble, ding |
| 0:34-0:41 | After that, stopped waiting for faults · tried to break it on purpose · fake faulty data · tests in the wet | "After that, I stopped waiting for things to break. Before I trusted it, I tried to break it on purpose. Fake faulty data, and tests in the wet." | **Cheeky grin** on "on purpose" | "STRESS TEST" stamp slams on. The telemetry log fills with red junk lines, then a water splash hits the robot cutout. Scorecards: **10 · 10 · 10**, one card dripping | Stamp thud, splash |
| 0:41-0:52 | Megapacks = much bigger version · 444 at Plumpton · test a site before it goes live · catch faults before the customer sees downtime | "Your Megapacks are a much bigger version of that. There are four hundred and forty-four at Plumpton. This role tests a site before it goes live, and builds tools that catch a fault before the customer sees any downtime." | **Hands open wide** on "much bigger" | A grid of 444 small plain grey blocks fills the frame, "444" text. "GO LIVE" ticks green across it; then one block blinks red and the camera zooms onto it | Whoosh, alert blip |
| 0:52-0:57 | No CAN bus or battery systems yet · want to learn from your team | "I haven't worked with CAN bus or battery systems yet. That's what I'd want to learn from your team." | Honest shrug | Meme text "NOT YET" small, then gone | (no music, 1 beat) |
| 0:57-1:06 | So yeah, Manit Khera · no flips yet · always check the data · thanks for watching | "So yeah, I'm Manit Khera. No flips yet, but I'll always check the data. Thanks for watching." | Small wave | The robot flop replays tiny in the corner; end card (name, email, phone) | Ding, music button ending |

No Claude Code / AI-editing mention in this video.
Words: ~185, so 70-75 s. If long, trim "There are four hundred and forty-four at Plumpton" to "444 of
them at Plumpton" first; keep the CAN bus gap line (it matches the cover letter).

## How each row ties to the job ad
| Row | Job ad line it answers |
|---|---|
| 0:11 firmware I wrote | "engineering fundamentals... for firmware/software-enabled systems" |
| 0:19 Raspberry Pi running Linux | Desired: "equipment running Linux based-applications" |
| 0:25 boot ID → buck converter | "troubleshoot... hardware, software, and firmware issues"; "root cause analysis"; electronics |
| 0:34 tried to break it on purpose | "testing, diagnosing, and resolving issues" before commissioning; "proactive, solution-focused attitude" |
| 0:41 test before go-live, catch faults before downtime | "seamless, on-time commissioning"; "proactively flag field issues"; "issues that cause downtime for... customers" |
| 0:52 CAN bus / batteries not yet | Desired CAN bus and battery systems, named honestly as gaps |

Values are shown, never quoted (no-AI-sounding-copy rule): proactive (tests to break it before
trusting it), solution-focused on hard problems (data over guessing), customer downtime as the goal.

## Facts (profile, story 09, cover letter, company_research/tesla.json)
- Roadster: say only that Tesla makes the Roadster. No specs, thrusters, flight, 0-60 or dates (the
  Oct 2026 new-Roadster claims are unverified secondary reports). The flip is a cartoon gag; his
  robot never flips, it flops, which is the joke.
- Clothesline robot: Arduino Nano firmware he wrote in C++; Python service under systemd on a
  Raspberry Pi (Linux); JSON telemetry over MQTT every 5 s; restarts traced from `bootId`/
  `resetCause` to a failing buck converter (voltage sag). Wet tests and injected telemetry faults
  are in the profile. Don't say the restarts stopped after the fix, or anything about batteries.
  Don't date the stress tests (not recorded whether before or after Open Day). Not "autonomous".
  Don't use the `clothesline.mp4 @ 0:32` battery close-up.
- Plumpton: Melbourne Renewable Energy Hub, 444 Megapacks, running since Dec 2025 (Enerdata, SEC
  factsheet). Don't mention the 2021 Victorian Big Battery fire.
- Role wording (commissioning, downtime, flag field issues): from the saved posting,
  `documents/applications/tesla_industrial_product_engineering_intern/job_posting.md`.
- Gap: no CAN bus, power systems or battery systems experience (same as the cover letter). No visa
  or hours line.

## Filming
Same setup as Infosys: phone vertical at eye level, ~1.2 m, waist up, face a window, plain wall.
One long take from `Filming Sheet.txt`: read a point, look at the lens, wait 1 s, say it. Mess up?
Pause and say the whole point again. Don't move your feet.
Moves: follow the Roadster with your eyes, your left → up → your right (0:00), hold still and look
down (0:05), straight face (0:09, 0:19), tap temple (0:25), cheeky grin (0:34), hands open wide
(0:41), shrug (0:52), wave.
