# NxtGen Intern Challenge 2026 intake

## SHORT form message (16 Oct 2026, for the Message box)

> Hi NXTGEN team! I'm Manit, a third-year Software Engineering (Honours) student at Deakin University.
>
> **What I've built:** a sensor-driven robot on an Arduino and a Raspberry Pi, plus a .NET backend that controls it over Wi-Fi, which I later load-tested against a simulated fleet of 5,000 robots. Demo videos are in the portfolio linked above.
>
> **Areas I want to get into:** software and the code that ties hardware together is my strongest side, but I'd love to get hands-on with closed-loop control and your LIDAR hardware, and I'm genuinely up for that fortnight of wiring and assembly.
>
> **When:** this summer, as a continuous three-month block over the break. I know the Challenge is designed around degree placements and mine isn't a required one, but I have the whole summer free and would be so grateful for the chance to learn from your team.
>
> Thank you for reading! My resume, cover letter, portfolio and grades are linked above.
>
> Manit

## Longer email version (16 Oct 2026, use this one)

Paste into the form's Message box. If the form fails, send the same text to careers@nxtgenindustries.com.
Form takes links only (Google Drive, anyone with the link can view): resume, cover letter, portfolio, grades.

**Subject:** Intern Challenge 2026, a software student hoping for a summer with your team (Manit Khera)

> Hi NXTGEN team,
>
> I hope your week has been a good one! My name is Manit, and I'm a third-year Software Engineering (Honours) student at Deakin University.
>
> I have to admit, I read the Intern Challenge page twice. The line about arriving as a software person and spending a fortnight on wiring and mechanical assembly made me grin, because that is exactly how I fell into robotics in the first place: I set out to write software and ended up wiring sensors into a little robot, finding out first-hand that hardware has opinions of its own.
>
> I also want to be honest with you. I know the Challenge is designed for students who need to complete a placement for their degree, and I'm applying a little outside that. The truth is simply that I have this whole summer free, and I can't imagine a better way to spend it than learning from your team on a real problem. I'm available for a continuous three-month block over the break, and I'd happily keep going part-time around my classes if it runs longer.
>
> That one robot has kept me busy ever since. I built it with an Arduino and a Raspberry Pi, wrote a backend that controls it over Wi-Fi, and later tested that backend against a simulated fleet of 5,000 robots. Software is where I'm strongest, but what excites me most about your program is that everyone touches everything. I'd love to get my hands on closed-loop control and your LIDAR hardware, both of which would be brand new to me.
>
> If there's any room for someone in my position this intake, I would be so grateful for the chance, and I promise to make the most of every minute of it. And if the timing isn't right, I'd still really value hearing what would make me a strong fit for a future intake.
>
> My resume, cover letter, portfolio (with demo videos) and my grades are linked above. Thank you so much for taking the time to read this, and for running a program like this for students.
>
> Warm regards,
>
> Manit Khera
> 0412 761 206 | manitkhera26@gmail.com
> linkedin.com/in/manit-khera-603957252

---

## Earlier draft (superseded)

Form: https://nxtgenindustries.com.au/careers/nxtgen-intern-challenge/
Fallback: careers@nxtgenindustries.com

They ask for: your details, a link to your resume, what you've built, and the areas you most
want to work in. The resume link must be a shareable link (Google Drive set to "anyone with the
link can view"), not an attachment.

---

## What I've built

One cardboard two-wheel robot that I keep giving new jobs.

First it was a smart clothesline: an Arduino Nano reading three line sensors, two light sensors
and a rain sensor, with a Raspberry Pi running a Python/Flask dashboard over MQTT. It drives the
washing to shelter when rain is coming, and cross-checks a flaky rain sensor against a weather
forecast before trusting it. For a while it only behaved on fresh batteries. I eventually traced
that to voltage sag at a failing buck converter, using the robot's own boot and reset logs rather
than a multimeter.

Then I wrote a C#/.NET backend to control it: 18 controllers, about 120 endpoints, device auth and
a CI/CD pipeline. I built Wi-Fi-loss recovery as a "what if": the robot keeps an undo stack, drives
itself back when it loses connection, and the server replays its report through a simulation
before recording where it is. On real hardware it came back to the exact predicted grid square.
That project scored 100/100 and went on show at Deakin Open Day.

Last, I load-tested the dispatch side with 5,000 simulated robots. The original API completed zero
jobs; after fixing 12 bottlenecks it sustained about 1,008 jobs per second across two Azure
replicas.

Code and demos: github.com/uiqvb

## Areas I most want to work in

1. **Software and hardware integration.** The code where the robot meets the backend is the part I
   enjoy most, and the part I have the most evidence for.
2. **Sensors and perception.** I've fused cheap sensors and learned not to trust them; I'd love to
   do the same with real LIDAR.
3. **Control systems.** My line following is a state machine, not closed-loop control. Motor
   controllers and proper feedback loops are the gap I most want to close.

I'm a Software Engineering (Honours) student at Deakin, available for a continuous 3 to 6 month
block, and happy to pick up anything outside software the team needs.
