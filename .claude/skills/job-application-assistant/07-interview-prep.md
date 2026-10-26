---
framework_version: 1.0.0
---

# Interview Preparation Guide

<!-- SETUP: STAR examples are personalized by running /setup based on your actual experience -->

## STAR Format

Structure answers as: **Situation** (context), **Task** (your responsibility), **Action** (what you did), **Result** (outcome).

Keep answers to 1-2 minutes. Be specific. End with what you learned or would do differently.

## Ready-Made STAR Examples

Built from Manit's story bank (`documents/notes/stories/`) and verified notes. Full story text and length variants live there.

### 1. The Frankenstein Integration (initiative, calculated risk)
**S:** In Trimester 1 2026 I had two unrelated final projects: a REST robot-control backend for Backend Development, and a physical Arduino/Raspberry Pi robot for Embedded Systems.
**T:** Nothing required them to meet. I wanted the backend to drive the real robot, knowing it could leave me finishing neither properly.
**A:** Took the idea to my unit chair, who was honest that it was ambitious and that I might spread myself thin. I chose to do it anyway and spent about a month building, breaking and rebuilding the integration, chasing cases where the robot moved but the software believed something else had happened.
**R:** The backend drove the robot. 100/100, and the project was selected from the cohort for the Deakin Open Day showcase, where I demoed it to prospective students and families.
**Use for:** "Tell me about going beyond what was asked", "a risk you took", "your proudest project"

### 2. Designing rollback the robot can do alone (systems design)
**S:** A robot that loses its connection mid-task cannot be told how to undo what it has done. I designed for that "what if" (it was never a failure I suffered).
**T:** Make recovery safe without the server, and keep the recorded position honest.
**A:** Every claimed command carries its inverse, so the robot builds a LIFO undo stack as it works. A 7-second watchdog triggers self-reversal. On reconnect, the server replays what the robot reports through simulation before committing anything. I also replaced rollback keyed by workflow id, which was wrong in principle because position is cumulative, so LIFO makes the broken case unrepresentable.
**R:** Hardware-verified: the robot returned to its exact predicted grid position. Shown live at Open Day.
**Use for:** "Walk me through a design decision", "a technical challenge", "how do you handle failure modes"

### 3. The brownout in the telemetry (debugging)
**S:** My clothesline robot misbehaved intermittently. Voltage sag meant it only behaved on fresh batteries; I bought about $100 of batteries before finding the cause.
**T:** Find the root cause of a fault I couldn't reproduce on demand.
**A:** Used the `bootId` and `resetCause` fields in the logged MQTT telemetry to see the board was resetting, and traced it to a failing buck converter instead of probing blindly with a multimeter.
**R:** Fixed the converter; the robot became stable. Lesson: instrument systems so the record answers questions the hardware won't reproduce.
**Use for:** "Hardest bug you've fixed", "embedded/hardware experience", "how do you debug"
**Backup answer:** the timestamp-skew bug that silently disabled lease expiry in the Robot Controller API.

### 4. Scaling the dispatch API (performance, measurement)
**S:** A robot dispatch API fell over under load: zero throughput at 5,000 simulated robots.
**T:** Find the bottlenecks and prove every improvement with numbers.
**A:** Audited 12 bottlenecks and race conditions; cut redundant SQL; added async I/O and backpressure; scaled to two Azure replicas using atomic PostgreSQL job claims and coordinated background sweeps. Load-tested with NBomber.
**R:** 3.44x single-replica throughput and 6.05x with two replicas at 400 robots; ~1,008 jobs/s at 5,000 robots; claim p50 from 766.5 ms to 59.5 ms. Backed by 54 automated tests and 80 benchmark runs.
**Use for:** "Performance work", "data-driven decisions", "concurrency"

### 5. Designing the defects (teaching, quality)
**S:** The Software Engineering Club ran a debugging workshop for about 30 students on a React to-do app our dev team built.
**T:** I solely designed the bugs attendees had to find (someone else delivered the session).
**A:** Chose defects that were neither too obvious nor too subtle, favouring ones a person would confidently declare fixed without fixing. Floated the room and unblocked people without taking the keyboard.
**R:** Saw which faults people caught, walked past, or wrongly believed fixed. Useful for testing, QA, research and teaching roles.
**Use for:** "Teamwork", "teaching or mentoring", "testing mindset"

### 6. Leadership by becoming unnecessary (leadership without a title)
**S:** I have not held a president-type title.
**T:** Show leadership honestly.
**A:** Three cases where the work ended with others able to do it without me: trained new 7-Eleven starters on the POS and food safety while running shifts solo; ran the stroke support group's monthly calendar for a year, then trained volunteers to publish it themselves; unblocked workshop attendees without taking over.
**R:** Each handover stuck. Use the honest framing: "I'll give you the real version rather than the impressive one."
**Use for:** "Leadership", "training others", "working in a team"

## Common Tough Questions

### "Why did you leave 7-Eleven?"
> Keep it short and forward-looking: it was a casual job alongside first year, and I moved my time toward my degree, volunteering and club roles. Never criticise the manager. Do not offer them as a referee.

### "You don't have [ROS / computer vision / PID / statistics]."
> Use the "Naming the Gap" move (Story 10): name it plainly, say where it matters most in this role, give the concrete substrate (MQTT JSON telemetry, C++ and Python, debugging from logs, a bang-bang state machine, with PID as the obvious next step), and say what you will have learned by the start date. Then actually do it.

### "Where do you see yourself in 5 years?"
> Graduated (2028), working as an engineer on systems where software drives real hardware or real operations, owning a subsystem end to end. Tie it to the company's product.

### "What's your biggest weakness?"
> I take on more than the brief asks. Joining two final projects nearly cost me both. Mitigation: I now tell the stakeholder about the risk up front, set a cut-off point, and keep a working fallback version.

### "Tell me about yourself"
> Optional opener from Story 02: I was pushed into software engineering and coasted through first year, then in second year decided to find out what I could actually do, and started enjoying it. Lead into Story 1. Use only when there's time for both.

### "Walk me through the FastAPI code in ParkSense" (if raised from LinkedIn)
> ParkSense is off the CV by choice. If asked: team project, I came up with the idea and did the data research; the team lead built the model, endpoints and map. Don't claim more.

### "Why this company specifically?"
> Customize per company. Must reference: specific projects, company values, market position, or team structure. Never give a generic answer.

## Questions You Should Ask Interviewers

### About the Role
- "What does a typical week look like in this role?"
- "What would success look like in the first 6 months?"
- "What's the biggest challenge the team is facing right now?"

### About the Team
- "How big is the team, and how do you divide work?"
- "What does the development/project lifecycle look like, from idea to production?"
- "How do you onboard new team members?"

### About Tech & Growth
- "What's your current tech stack for [relevant area]?"
- "Is there room to grow into more architectural or strategic decisions?"
- "How does the team stay current with new tools and methods?"

### About Culture (use these to prevent disappointment)
- "How would you describe the team culture?"
- "What does professional development look like here?"
- "Is there flexibility for remote/hybrid work?"
- "What's the balance between development/new projects and maintenance work?"
- "How would you describe the leadership style in this team?"
- "What do people who thrive here have in common?"

## Phone/Video Interview Tips
- Have STAR examples written out (use this file)
- Keep a glass of water nearby
- Smile when speaking (it changes your tone)
- Ask for clarification if a question is vague
- It's OK to take 5 seconds to think before answering
- End with: "Is there anything else you'd like to know about my background?"

## After the Application (Best Practice)

### Follow-Up Etiquette
- **Don't call to "stand out"** or to learn more about the role post-submission - this risks a negative impression
- If the employer specified a timeline, respect it and wait
- If no timeline was given and significant time has passed (2+ weeks), a brief call to ask about status is acceptable
- If you have genuinely new, relevant information to share, a short follow-up is fine

### Thank-You Notes
- When you receive any update (interview invitation, rejection, or status update), send a brief thank-you message
- Express appreciation for their time and the process
- Keep it short (2-3 sentences)

## Roleplay Guidelines
When the user asks for interview practice:
1. Ask which role/company to simulate
2. Start with easy warm-up questions ("Tell me about yourself")
3. Progress to role-specific technical questions
4. Include 1-2 behavioral questions using the competencies from the job posting
5. End with a tough question or curveball
6. After each answer, give brief feedback: what worked, what to sharpen
7. Suggest which STAR example would work best for each question
