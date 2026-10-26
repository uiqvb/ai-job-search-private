# To do

What's left to build, fix or decide. One line each, with a pointer to the details. Keep it current: tick or delete a line when it's done, and log it in `log.md`.

Last updated: 2026-10-26.

## Applications (time-sensitive)
- [ ] **RMIT Web Application Developer video**: film from `documents/video/rmit/Filming Sheet.txt`, then edit with `/video`. Closes Wed 28 Oct. Delivery route still open (LinkedIn note, or hold for interview).
- [ ] **Capgemini follow-up to Rachna V**: due 28 Oct. Ask whether a student visa (subclass 500) is OK, and whether the role ends 26 Feb or 5 Mar.
- [ ] **Tekt Industries nudge**: they promised a reply by ~23 Oct; none came.
- [ ] **14-day follow-ups**: due 30 Oct for the 16 Oct batch (ReSource, NxtGen, Tekt, 8 cold emails).
- [ ] **Drafted, never sent**: Inspire Robotics (16 Oct), Arcitecta (20 Oct), Syncrowin (22 Oct), Schoolbox (23 Oct).
- [ ] **Gmail drafts not sent**: ReSource follow-up; thank-you to the Infosys recruiter contact from the Deakin talent showcase (name not recorded).

## Decisions waiting on Manit
- [ ] **Arcitecta**: was the internship application submitted, or only the Hack2Hire sign-up? (`gmail_sync/pending.md`)
- [ ] **Bosch and KPMG**: add to the tracker as rejected? Add to Suncorp's outcome that it reached the online assessment. (memory: application-history-from-gmail)
- [ ] **Old LaTeX files**: delete `cv/main_arcitecta_student_internship.tex` and `cover_letters/cover_arcitecta_student_internship.tex`?
- [ ] **Status notes from the 26 Oct catch-up**: Infosys (Shweta Dhall's 25 Oct reply), Andromeda (rejection email 25 Oct; cancel the 28 Oct nudge to Natalie).

## Video pipeline (`/video`)
- [ ] **Finish the test run**: only seconds 0-15 of the Infosys test went through visual review. Run the rest with `/video build infosys all`.
- [ ] **Open questions from the test**: springy or wobbly sticker pop; robot sticker crossing the face at 13.1-13.3 s; music mismatch (plan says Pixel Peeker Polka, project.json says A Stroll); sfx levels; gate 2 (Visual Plan) approval never confirmed. (log.md, 25 Oct 20:35)
- [ ] **First real video through the full pipeline**: RMIT.
- [ ] **Script/storyboard step**: `/video` starts from an approved storyboard. Writing the script is still manual (`documents/video/SCRIPT-RULES.md`).

## Automation
- [ ] **Turn on the Task Scheduler history log** (admin terminal): `wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true`
- [ ] **Check the 25 Oct fix holds**: jobs should run 2 min after sign-in once a day. Check `automation/logs/` for a log every day.
- [ ] **Overnight Gmail sync can't write to `log.md`**: unattended runs can't get approval for that write. Fix the permission or have `run_job.py` append the line.
- [ ] **Tune `/catchup`**: only run a few times; trim noisy sweep queries (Premium Graduate, Indeed digests, birthday mail).

## CV and documents
- [ ] **CV name spacing bug**: the letter-spaced "MANIT KHERA" extracts as "M A N IT K H E R A" for ATS. Fix in `templates/cv/master-v7/build_cv.py`.
- [ ] **Old CSIRO builder** still says "second year ... two full years" (`documents/notes/docx-builders/build_cover_letter_csiro.py`). Left as is; reword only if reused.

## Deferred plans
- [ ] **Skill to make**: Manit wants to make a new skill, topic not remembered yet. Ask him; don't guess. (memory: skill-to-make-later)
- [ ] **Phone access**: cloud sessions on this private repo, plus a git-pull SessionStart hook and a commit+push Stop hook; Word builds stay on the laptop. (memory: phone-access-plan; log.md 21 Oct)
- [ ] **Codex fallback** in `automation/run_job.py`: rerun with `codex exec` when Claude fails or is out of usage; a `codex exec` wrapper for the `/apply` reviewer step.

## Repo
- [x] Private repo for the whole workspace (2026-10-26). Push with `bash tools/push_private.sh`. Resumes, video media, `automation/config.json` and `.env` stay out. The public fork (`public-fork`) and `upstream` are fetch-only.
- [ ] Brother: invite him on GitHub (Settings > Collaborators). He runs `/reset` then `/setup` for his own profile.

Claude's memory is mirrored in `documents/notes/claude-memory/` (refreshed on every push).
