# Story Bank

Every distinct story extracted from the seven cover letters written between July and August 2026.
Each file holds the story, what it evidences, length variants, and the facts that must be checked
before it is reused.

The originals live in `../Archive/Cover_Letters/`. This folder exists so that a new cover letter
is assembled from stories rather than copied from the last letter and edited.

---

## Index

| # | Story | Evidences | Used in |
| --- | --- | --- | --- |
| [01](01-frankenstein-integration.md) | The Frankenstein Integration | Initiative, calculated risk, persistence, systems thinking | Asta, Deloitte, Suncorp, CSIRO x2 |
| [02](02-taking-ownership-of-the-degree.md) | Taking Ownership of the Degree | Self-awareness, intrinsic motivation, growth | Asta, Deloitte, Suncorp |
| [03](03-scientist-to-extended-essay.md) | The Scientist and the Extended Essay | Research instinct, long-horizon focus | CSIRO Final |
| [04](04-designing-the-defects.md) | Designing the Defects | Experimental design, teaching restraint | CSIRO, Deakin x2, Suncorp |
| [05](05-pink-shirts-at-orientation.md) | The Students in the Pink Shirts | Empathy from lived experience, motivation | Deakin SEA |
| [06](06-market-day-hesitation.md) | The Student Who Hovers | Engagement, noticing, initiating contact | Deakin SEA |
| [07](07-rain-sensor-cross-check.md) | Making the Rain Sensor Prove Itself | Reliability, sensor cross-validation | CSIRO |
| [08](08-a-log-is-not-evidence.md) | A Log Is Not Yet Evidence | Data integrity, failure-mode design | CSIRO |
| [09](09-brownout-in-the-telemetry.md) | The Brownout in the Telemetry | Debugging depth, observability | CSIRO, interview material |
| [10](10-naming-the-ros-gap.md) | Naming the Gap | Honest self-calibration | CSIRO x2 |
| [11](11-leadership-by-becoming-unnecessary.md) | Leadership by Becoming Unnecessary | Leadership without a title, handover | Deakin Assistant |
| [12](12-trust-and-challenge.md) | Trust and Challenge | Culture fit, response to feedback | Suncorp |
| [13](13-can-the-evidence-bear-the-weight.md) | Can the Evidence Bear the Weight | Feasibility research, honest scoping | CSIRO |
| [14](14-reading-their-paper.md) | Reading Their Paper | Genuine preparation, critical reading | CSIRO |
| [15](15-club-involvement-track-record.md) | Club Involvement Track Record | Supporting evidence stock | Deakin x2, Suncorp |

## Pick by what the role asks for

| The role asks for | Reach for |
| --- | --- |
| Initiative, going beyond the brief | 01, with 02 as setup |
| Growth, self-awareness, a "tell us about yourself" | 02, then 01 |
| Research aptitude, why research | 03, 14, 13, 08 |
| Backend or distributed systems depth | 08, then 01 |
| Embedded, hardware, reliability | 07, 09, 01 |
| Experimental or user-study design | 04, 14 |
| Student-facing, ambassador, orientation | 05, 06, 15 |
| Leadership without a title | 11, 04 |
| Culture fit, environment, feedback | 12, 02 |
| A requirement I clearly do not meet | 10 (this is a move, not a story) |
| Customer service, patience under pressure | 11, 15 (7-Eleven) |

## How to build a letter from these

1. Work the ad through `../Guides/Reading-a-Job-Advertisement.md` and pull the keywords.
2. Pick **one** story to carry the letter. Almost always 01, 03, 05 or 11 depending on the role
   type.
3. Pick **two or three** supporting items, one per body paragraph, each mapped to a keyword. The
   guide is explicit that each body paragraph should be built on one keyword from the research.
4. If a listed requirement is missing, run the move in 10 rather than hiding it.
5. Do the organisation-specific paragraph properly, using the template in 14.
6. Run `../Guides/Checklists.md` before submitting. One page, no em dashes, UK English, numbers
   one to ten as words.

## Standing rules for every story

- **Never write a count, a score, or a pattern name from memory.** `../CLAUDE.md` is the source of
  truth, and it records a code audit that corrected four claims that had already shipped.
- Facts flagged ⚠️ in a story file are unresolved. Resolve or drop them, do not print them.
- Facts flagged ❌ are ruled out permanently. They are recorded so they do not get reinvented.
- No em dashes anywhere.
