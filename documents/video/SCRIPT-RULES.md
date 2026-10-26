# Video script rules (read before writing or editing any intro-video script)

Manit's corrections, collected so they are not repeated. Applies to Claude, Codex or any other agent
working in `documents/video/`. Process and editing steps are in `PROTOCOL.md`; this file is about the
words.

## 1. One or two achievements, told properly (21 Oct 2026)
- Pick **one** main story, at most two, chosen for what *this* company values. Never a highlight reel.
- Give each story its context before its result: what the project was, why it existed, what went
  wrong or what was hard, what he did, how it turned out. A number with no setup means nothing.
- Leave out everything else. If an achievement needs one line to mention, it doesn't belong.
- Rejected example (v1): eight achievements in 90 seconds (robot, security scan, 6x Azure, 7-Eleven,
  stroke group, Claude Code...). Manit: "super unnatural and move through ideas very quickly. They
  don't even give proper pretext to projects or situations."

## 2. Every sentence hands off to the next (21 Oct 2026)
- Start each sentence from something the listener already has: the thing just mentioned, "it",
  "that", "but", "so", "instead". Then add one new thing. Old information first, new information last.
- Don't open a sentence with a brand-new subject that hasn't been introduced ("An Arduino reads the
  sensors..." straight after describing what the robot does).
- Manit's fix, the model to copy:
  - Before: "...when it's sunny it turns toward the light. **An Arduino reads the sensors** and drives the motors."
  - After: "...when it's sunny, it turns toward the light. **It's powered by an Arduino that** reads the sensors and drives the motors."
- Link sections too: the "why <company>" section opens from the story's theme ("Trust is also why
  your report caught my eye", "Connecting software to something physical is what I enjoy most, and
  it's why..."), not with a cold "So why X?".

## 3. Written to be spoken
- Short sentences, contractions, words he'd actually say to a friend. Read it aloud; if a line is hard
  to say in one breath, split it.
- No lists of tech in one breath. Two named parts per sentence at most.
- Close (updated 21 Oct 2026, Manit's call): "So yeah, I'm Manit Khera..." plus **one** casual line that
  calls back to the video's theme, then "Thanks for watching." Example (Capgemini, trust theme):
  "So yeah, I'm Manit Khera. I build things people tell me I can't. Thanks for watching." Keep it in his voice and tied to the story; avoid generic slogans that could end any
  video ("I make software move things").

## 4. Keep his edits
- When Manit edits a script himself, keep his wording. Fix only typos and spelling ("autnomously" →
  "autonomously", "Its" → "It's", "arduino" → "Arduino"), and say what you fixed.

## 5. Facts (same rules as the CV and cover letter)
- Every claim must be in `.claude/skills/job-application-assistant/01-candidate-profile.md` or the
  company research cache. Don't add outcomes that aren't recorded (e.g. "swapped it and the resets
  stopped", "bought more batteries"; the battery line was flagged as wrong in the Andromeda takes).
- The Wi-Fi loss is a "what if" he designed for, never something that happened; say it as a question.
- Company facts must be verified from a fetched source, and named plainly ("your report on agentic AI").
- Say "third year of Software Engineering" / "Software Engineering student", never "software
  engineer" or "second-year".
- No availability caveats (visa hours, part-time) in videos either; see the CV/letter rule.

## 6. Shape
- About 90 to 110 seconds, ~220 to 240 words: hook, who I am, the story (setup, problem, result),
  why this company, close.
- Every shot-list row names the exact clip and time in the source (`broll/cuts/<file> @ m:ss-m:ss`) and
  links to the file, plus the approximate time in the new video.
- One idea on screen at a time; leave the punchline lines bare so they land.

## 7. Don't over-fit one company value (21 Oct 2026)
- A company value or report is a hook for **one** section ("why <company>"), not the theme of the
  whole video. v3 of the Capgemini script said "trust" about eight times; Manit asked why it was so
  trust-centric and had to re-plan the shoot.
- The theme comes from Manit: his own pattern is "what if" problems and building things people said
  he couldn't. Map the company's value onto that, not the other way round.
- Before he films, check the theme with him in one line ("Theme: X, because Y. OK?"). Rewrites after
  filming cost him reshoots. When a script changes after filming, keep unchanged sections word for word
  and list exactly which sections need reshooting.

## 8. Outlines, not scripts; about them, not him (22 Oct 2026, Syncrowin)
- Memorised lines made him speak slowly and forget words. Write the full script as a reference, then
  a filming table of keywords only (a few words per point, never full lines) that he speaks from.
- Centre the video on the company: where they are now, what they're doing next, what they need.
  He appears only where he fills one of those needs, one quick line each. Achievements are proof,
  never the subject.
- If a section says "you don't want to hear about achievements", nothing after it may be an
  achievement story.
