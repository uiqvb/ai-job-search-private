---
name: pending-decisions-2026-10-20
description: Open questions to Manit from the 2026-10-20 Gmail sync and Capgemini application; check and resolve before acting on these rows
metadata:
  node_type: memory
  type: project
  originSessionId: f501b398-3f78-43f2-807b-216f97410542
  modified: 2026-10-20T10:02:58.352Z
---

Unresolved at the end of 2026-10-20. Ask Manit or resolve, then delete each line here once it's done.

1. **Capgemini:** applied (done). Intro video sent to Rachna 2026-10-21. Still open: confirm with Akash S / Rachna V that a student visa (subclass 500) is accepted and that the role really ends 26 Feb (GradConnection said 5 Mar). GradConnection gives the closing date as 30 Nov 2026.
2. **Arcitecta:** did he submit the Student Internship application, or only sign up for Hack2Hire (sign-up email 2026-10-20)? The row is still `drafted`.
3. **Bosch and KPMG:** add them to the tracker as `rejected`? Also add a note to the Suncorp outcome that it reached the online assessment stage.
4. **Old LaTeX files:** `cv/main_arcitecta_student_internship.tex` and `cover_letters/cover_arcitecta_student_internship.tex` are unused. Delete them?
5. **CV template name spacing:** the letter-spaced "MANIT KHERA" extracts as "M A N IT K H E R A" in pypdf. The fix is planned for `templates/cv/master-v7/build_cv.py` before the next application.
6. **Git:** none of the template, command or skill changes from 2026-10-20 are committed.

`gmail_sync/state.json` holds the Capgemini and Arcitecta message IDs under `pending_user_decision`. Set `last_sync` once those two are resolved.

**Why:** Manit asked to keep this context; these items were left hanging mid-conversation.

**How to apply:** raise them at the start of the next session. Related: [[application-history-from-gmail]].
