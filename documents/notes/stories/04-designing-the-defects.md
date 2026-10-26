# 04. Designing the Defects

**Hook:** Choosing which bugs to plant was harder and more interesting than building the
application they were planted in.

**Used in:** CSIRO (as an experimental-design credential), Deakin Assistant, Deakin SEA,
Suncorp (briefly).

**Best for:** experimental design, user studies, teaching and mentoring, thinking about how
other people fail, quality and testing roles.

---

## The story

- On the Deakin Software Engineering Club committee, the development team built a React to-do
  application as the teaching artefact for a debugging workshop.
- I was on the development team that built the application. **I solely designed the seeded
  defects** attendees had to find and fix.
- About 30 attendees worked through it.
- Choosing the faults was harder and more interesting than building the application. A defect
  that is too obvious measures nothing. A defect that is too subtle measures only patience. The
  ones worth planting are the ones a reviewer will confidently declare fixed without having
  fixed it.
- I then floated the room as a helper. Having written every bug myself, I knew where people
  would get stuck. The job was to get them unstuck without reaching over and taking the
  keyboard.
- What I got out of it: which faults people caught immediately, which they walked straight past,
  and which they believed they had resolved.

## The two very different uses

**As research instrument design (CSIRO).** The Technology 11 brief involves a user study where
participants review plans containing deliberately introduced errors. The letter argues this is
the same instrument, and therefore that error injection is not a detail you leave to the end of
a project. This is the strongest single paragraph in the CSIRO letter.

**As support and facilitation (Deakin roles).** Getting someone unstuck without taking the
keyboard is most of what supporting a team actually is. Pairs with story 11.

## What it evidences

- Designing a measurement instrument, not just a task
- Understanding of how people fail, and of false confidence in particular
- Restraint when helping (do not take the keyboard)
- Solo ownership of a defensible component within a team build

## Length variants

**One line.** I designed the seeded defects for a 30-attendee club debugging workshop, then
helped the room work through them.

**Short.** On the Software Engineering Club committee, the dev team built a React application for
a debugging workshop and I solely designed the defects seeded into it for about 30 attendees to
find. Choosing them was the interesting part: too obvious measures nothing, too subtle measures
only patience, and the ones worth planting are the ones someone will confidently declare fixed
without having fixed them.

**Full.** `../Archive/Cover_Letters/Manit_Khera_Cover_Letter_CSIRO.docx`, paragraph five.

## Facts and verification

Verified in `../CLAUDE.md` (DSEC entry):

- Committee member, general committee, **not** a named portfolio. July 2025 to April 2026.
- Built the to-do app **as part of the dev team**. The **bug injection was solo**. Keep that
  distinction, it is the defensible individual claim.
- Around 30 attendees. Confirmed.
- **Did NOT run or deliver the session.** Someone else delivered it. Never write "taught" or
  "delivered a workshop".

**Number to check before reuse.** The Deakin Assistant letter says "the 15 defects". The README
does not record a defect count anywhere, it says only "the seeded defects". Confirm the real
number before printing 15 again, or drop the figure.

## Do not say

- "Ran the workshop", "taught the workshop", "delivered the session". All false.
- That I built the app alone.
