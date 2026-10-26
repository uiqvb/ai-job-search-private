# 01. The Frankenstein Integration

**Hook:** Two unrelated final projects, one month, and a backend that ended up driving a physical
robot.

**Used in:** Asta, Deloitte, Suncorp, CSIRO (both versions). This is the workhorse story.

**Best for:** initiative, risk tolerance, self-directed work, persistence through debugging,
systems thinking, anything asking for "goes beyond the brief".

---

## The story

- In one trimester I had two unrelated final projects. Backend Development: a server-side REST
  platform for controlling robots. Embedded Systems: a physical two-wheel-drive robot built on an
  Arduino Nano and Raspberry Pi with several sensors.
- The two units were unrelated. Nothing in either brief suggested they should meet.
- I decided to connect them: develop the backend API further and make it communicate with the
  physical car.
- I took it to my backend unit chair. He was supportive but honest. It was ambitious. Both
  projects were significant assessment, and combining them created a real chance I would spread
  myself thin and finish neither properly. (In the Asta and Deloitte versions this is phrased as
  him saying seeing it work would be a dream come true, while being understandably sceptical.)
- The sensible option was to finish them separately and take the marks.
- I could already see the combined system in my head. I took the risk.
- For about a month I built, tested, broke and rebuilt it. Sometimes the backend worked and the
  robot ignored it. Sometimes the robot moved while the software believed something completely
  different had happened. Solving one problem created another somewhere I thought I had already
  finished.
- Eventually the backend spoke to the robot, and the robot listened.
- The backend project received 100 out of 100 and was selected from my cohort for showcase at
  Deakin Open Day.

## What it evidences

- Creating the challenge yourself rather than executing a defined brief
- Accepting and managing a real downside risk, deliberately, with the stakeholder informed
- Sustained debugging across a hardware and software boundary
- The gap between what a system reports and what physically happens (this is the part CSIRO
  cared about)
- Earning trust: the professor and unit chair backed it, and it went to Open Day

## Length variants

**One line.** I connected two unrelated final projects, a backend robot control API and a
self-built two-wheel robot, so the backend drove the physical car. It scored 100 out of 100 and
was shown at Deakin Open Day.

**Short.** In one trimester I had two unrelated final projects, a REST control platform for
robots and a physical two-wheel robot. They were never meant to interact. I spent about a month
making the backend drive the robot, at the risk of finishing neither properly. It worked, scored
100 out of 100, and was selected from my cohort for showcase at Deakin Open Day.

**Full.** See `../Archive/Cover_Letters/Manit_Khera_Cover_Letter_Suncorp.docx` for the tightest
narrative version, and `..._Asta.docx` for the version that ends on what it changed about me.

## The angles this story can be pointed at

| Angle | Framing used |
| --- | --- |
| Bold ideas and ownership (Deloitte, "Lead the way") | Leading the way is not having bold ideas, it is taking responsibility for them and staying committed when they get difficult. |
| Client work with no fixed playbook (Asta) | There was no guide for connecting a backend API to a physical robot, the same way client problems arrive without one. |
| Trust and challenge in a team (Suncorp) | The unit chair challenged the idea, made sure I understood the risk, then let me choose. See `12-trust-and-challenge.md`. |
| Plan versus reality (CSIRO Tech 11) | Watching a plan that looked reasonable on a dashboard become the wrong movement on a floor. The representation an operator approves and the behaviour they get are two different objects. |

## Facts and verification

Verified in `../CLAUDE.md` (Robot Controller API and Smart Clothesline Robot entries):

- 100/100 and Open Day showcase: on my word, not code-verifiable. Consistent everywhere.
- Backend: .NET 8, ASP.NET Core, C#, PostgreSQL, EF Core, ADO.NET/Npgsql. 18 controllers,
  16 bounded contexts, all planning server-side.
- Robot: Arduino Nano, C/C++, Raspberry Pi, Python/Flask, MQTT, I2C, systemd.
- Both trimester 1, 2026. Demo videos and repos are linked in CLAUDE.md.

**Careful:** the phrase "the boldest idea I had attempted at university" and "Frankenstein
project" are Asta/Deloitte flourishes. Fine in a letter, do not put them anywhere near a resume.

## Do not say

- "Orchestrating autonomous robots." The design is the opposite. The robot deliberately holds no
  plan of its own.
- "Saga pattern." Removed from all material as inaccurate.
- Anything implying the integration was part of either unit's requirements.
