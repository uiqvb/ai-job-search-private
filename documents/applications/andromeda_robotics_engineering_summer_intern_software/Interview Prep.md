# Andromeda Robotics: prep material

Engineering Summer Intern Program, Software Engineering stream (Software, Firmware & Autonomy).
Written 13 October 2026. Company facts come from Andromeda's site and press interviews; check
the dates, some numbers are old.

---

## 1. The company

- **Founded 2022** in Melbourne by Grace Brown (CEO, mechatronics engineer, building robots
  since she was 15) and Yan Chen.
- **Origin story:** Brown built the first Abi during COVID lockdown, alone in a uni dorm, after
  realising she had gone months without a hug. Her first goal was a robot that asked about her
  day. She then rang 40 Melbourne nursing homes to test the idea.
- **Funding:** Startmate 2022 intake. A$3 million seed in June 2024 (Purpose Ventures). A$23
  million Series A in September 2025 led by Forerunner Ventures (US), reported A$100 million
  valuation.
- **Now:** Brown has moved to San Francisco and opened a US headquarters. Engineering is in
  Southbank, 224-226 Normanby Road.
- **Their line on what they build:** "the social intelligence layer for humanoid robots".
- **Values:** Empathy, Play, Never Settle, Tenacity, Unity.

## 2. Abi

- **What she does:** leads group activities (tai chi, dancing, quizzes, singing, meditation) and
  visits residents one on one in their rooms.
- **Memory:** recognises faces and remembers conversations from days or months earlier, including
  family details.
- **Languages:** 90. This matters because residents with dementia often revert to their first
  language.
- **Perception:** reads expressions, tone of voice and gestures. Brown: Abi is "not just a
  conversational AI in a robot body".
- **Design:** bright, colourful, childlike on purpose, to look nothing like an industrial or
  sci-fi robot. Personality inspired by Disney characters. Height is reported as anywhere from
  about 1.2 to 1.5 metres, so do not quote a figure.
- **Genesis Abi (late 2025):** carers set a daily schedule and "she'll navigate the home
  independently". This is the autonomy work the Software stream would touch.
- **Customers:** mecwacare (22 facilities) and Medical & Aged Care Group. Now also offered in the
  US. In 2024 Brown promised investors 100 Abis in homes within 18 months.
- **Why it matters:** Brown says almost 40% of assisted-living seniors never receive visitors.

## 3. What has been hard for them

- **Unreliable Wi-Fi in care homes.** The main technical obstacle Brown names. Their answer is a
  hybrid design, part cloud and part on the robot.
- **Failing gracefully.** When the internet is slow, Abi jokes that she is sleepy and asks people
  not to ask too many questions. Brown: trust comes from how Abi handles her limits, not only
  from uptime.
- **Withdrawn residents.** Some would not engage at all until Abi spoke to them in their native
  language. Staff have said a resident "hasn't talked like that in months".
- **Staff shortages.** Abi is pitched as support for carers, never a replacement.
- **Scale.** The ad says they are going from early deployments to "thousands of real-world
  environments".

## 4. Where I connect (lead with the first one)

| Their problem | My matching work |
| --- | --- |
| Robot loses Wi-Fi in a real building | My robot notices the dropout after 7 seconds and retraces its last five moves on its own |
| Fail gracefully, stay trustworthy | My server replays the robot's report in a simulation before believing it |
| 22 homes to thousands | I asked "what if there were 5,000?", found the backend did zero jobs, and rebuilt it |
| Hybrid cloud and on-robot processing | My backend does the planning; the robot only polls over plain HTTP |
| A robot with personality | A cardboard robot with its own profile card |
| Care setting | A year volunteering with Boroondara Stroke Support Group |

## 5. Questions to ask them

- "Grace has said Abi jokes about being sleepy when the Wi-Fi is slow. How do you decide what
  Abi can still do offline?"
- "With Genesis Abi navigating a home on her own, what is the hardest part of a real care home
  that a lab never shows you?"
- "What changes when you go from 22 homes to thousands: the robot, or how you support it?"
- "Why design Abi to look childlike, and has that ever worked against her with residents or
  families?"
- "What has been the hardest part of getting Abi adopted: the technology, or earning the trust
  of residents, families and staff?"
- "This is your first intern program. What would make you call it a success in February?"

## 6. My stories, ready to tell

**Why I built it.** Two unrelated assignments, a robot (Embedded Systems, 93) and a backend
(Backend Development, 100/100). Nobody asked me to join them. I wanted to see my code move a
real thing across the floor. A month of build, break, rebuild.

**Maksym and the rage bait.** My unit chair Maksym Slavnenko would say "nah, you can't do that"
whenever I pitched an idea, not to put me off, but because he knew I do my best work proving him
wrong. Then he moved the target further out. Love-hate. In between we would sit going "okay, but
what if..." like two kids.

**The batteries.** The robot behaved on fresh batteries and acted up below about 90 percent. I
kept buying new ones, probably $100 worth, before I tracked the real fault, the voltage
converter, down in the robot's own logs. I now own a pile of 90 percent full batteries.

**The Wi-Fi what-if.** I never actually had Wi-Fi dropping problems. I built the recovery
deliberately, as a "what if", and then tested it on the real robot. Say it that way; the real
problem I lived through was voltage sag. Every command is sent with its undo. After 7 seconds of silence the robot
retraces its last five moves by itself, then reports. The server checks the report in a
simulation before saving it. On the real robot it ended up exactly where predicted.

**Party trick.** It is also an RC car: WASD keys on the dashboard, plain web requests and
polling underneath.

**5,000 robots.** One robot worked. At 5,000 simulated robots the original backend finished zero
jobs. I found 12 problems, including two robots claiming the same job, fixed them, added a
second server: about 1,000 jobs a second, none failed. 80 benchmark runs, 54 automated tests. I
never found the new breaking point.

**How I tested the clothesline robot.** Got it wet on purpose. Fed it fake rain readings to check
it trusted the forecast over a broken sensor.

**Be ready to say plainly:** no ROS, no PID (steering is pattern matching), no board or
mechanical design. If asked how many teams were in the hackathon: four.

## 7. What I submitted on the form

**Top 3 strengths (127 character box):**

> 1. Testing absurd ideas. 2. Debugging until the problem gives. 3. Rising to a challenge when told it can't be done.

**People I would pick:** Dr Maksym Slavnenko (m.slavnenko@deakin.edu.au), Dr Clement Asogwa
(clement.asogwa@deakin.edu.au), Dr Daniel Lai (no email given; I have not met him). Closing line:
they are the people I have had the most fun studying with, and I want people better and more
experienced than me on my team.

**Files:** `Manit Khera Resume.pdf` (1 page, three referees) and `Manit Khera Portfolio.pdf`
(2 pages) in this folder.

## 8. People contacted

| Who | Role | Status | Next step |
| --- | --- | --- | --- |
| Natalie Badawy | Talent Acquisition Specialist | Emailed 13 Oct. Auto-reply: on leave 12 to 23 Oct, back Mon 26 Oct | One follow-up around Wed 28 Oct if no reply |
| Nelson Quach | Robotics Technician (since Nov 2025), 1st-degree connection | LinkedIn message drafted | Send it. Asks about a normal week and what he wishes he had known |
| Carina Parisella | Chief People Officer, Natalie's named backup (Carina.Parisella@dromeda.com.au) | Short timing email drafted | Send about 9am Wed 14 Oct with the portfolio attached. No follow-up if she does not answer |
| Erika Choong | Founding AI & Robotics Engineer | Connection request sent (no Premium, cannot message) | Message only if she accepts |
| Nilp Amin | Autonomy Team Lead | Connection request sent | Message only if he accepts |
| Alex Hofmann | Special Projects Engineer | Connection request sent. Email to the address on his portfolio site drafted, not sent yet; Manit plans to send it | After sending, wait. No follow-up |
| Josh Leivenzon | DevOps & Software Engineer | Email scheduled for the morning of 14 Oct, to the address on his GitHub profile. Built on his team video (bubble gun, real-world problems) | Wait. If he replies, ask about nix-ros-workspace |
| Tom Cameron | Tech Lead, AI Engineering ("building robot brains"); Nelson is a mutual | Connection note drafted | Send with the note |
| Sophie Lane | HRI and AI Engineer | Connection note drafted | Send with the note |

That is the ceiling. Do not use the website contact form or abi@andromedarobotics.ai, and do not
contact Grace Brown (CEO) or Brian McCarthy (CCO). If anyone replies, ask "is there anyone else
you would suggest I talk to?"

Others seen on LinkedIn, to read and follow only: Rohan Nowell (ML Engineer), Jason Chan (Head
of Machine Learning).

## 9. Still to check

- Both Panopto demo links, the LinkedIn post and the Hackster.io page open in a private window.
- The public `RobotControllerApi` README still says the robot was "not validated end to end" and
  has "no automated test suite". Update it before someone clicks through.
- Give Maksym and Clement a heads-up that they are named as referees and on the form.
- Visa wording for a placement starting in late October, 5 days a week onsite.
- Read the mecwacare case study and the News page on their site before any interview.

## Sources

- https://andromedarobotics.ai/ and https://andromedarobotics.ai/product
- Pulse 2.0 interview with Grace Brown, 24 June 2026: https://pulse2.com/andromeda-robotics-profile-grace-brown-interview/
- Forbes Australia 30 Under 30 profile, 14 October 2024 (team of 15 and revenue figures are old): https://www.forbes.com.au/news/30-under-30/inside-grace-browns-quest-to-revolutionise-aged-care/
- SmartCompany on the Series A, 9 September 2025: https://www.smartcompany.com.au/startupsmart/andromeda-raises-23-million-robot-abi-grace-brown-us-expansion/
- Inside Ageing on the Series A: https://insideageing.com.au/andromeda-raises-23-million-and-sets-record-in-women-led-series-a-funding/
