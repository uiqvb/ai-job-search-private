---
name: automation-setup-in-progress
description: Scheduled job-search automation (wake-from-sleep + ntfy push) built and scheduled 2026-10-20; only phone setup and wake verification remain
metadata:
  node_type: memory
  type: project
  originSessionId: 54963496-05c7-490b-8512-460e05ab295f
  modified: 2026-10-25T03:03:58.868Z
---

Manit wants `/gmail-sync`, Meetup event tracking and `/scrape` to run on a schedule and push to his phone.

**Design (his choice, 2026-10-20):** laptop sleeps, Windows wake timers wake it per job (wake timers on AC and battery since 2026-10-20; laptop not in a bag at night). Notifications via ntfy, topic in gitignored `automation/config.json`. Repo `uiqvb/ai-job-search` is **public**: never commit personal data.

**Built and tested 2026-10-20:** automation/notify.py, event_reminders.py, run_job.py (Sonnet since 2026-10-21, token use logged to automation/logs/usage.csv; gmail_sync timeout 40 min, scrape 60 min; these are ceilings, real runs took ~5 min), install_tasks.ps1 (`-Remove` deletes). Both Claude jobs passed end to end. Tasks registered in Task Scheduler folder `\JobSearch\`: gmail_sync 01:00, scrape 03:00 daily (was every 3 days briefly; Manit reverted 2026-10-21: "we can't afford to miss jobs"), event_reminders 05:00 (today's events), others daily; ntfy holds pushes until 07:30 (deliver_at); one push per run with bullets + link buttons, WakeToRun, StartWhenAvailable, Interactive logon (must stay signed in). 771 tests pass.

**Still open:**
1. DONE: ntfy works on his phone (confirmed 2026-10-20). Topic `manit-jobs-ab049e4bfb76`, also saved in documents/notes/automation.md.
2. Wake timers FAILED 21 Oct: laptop slept 01:11-08:39 without waking, so 03:00 scrape and 05:00 reminders missed. Needs a fix (no sleep on AC overnight, or run at morning logon). Checked 25 Oct: wake timers have never worked any night (Modern Standby laptop that hibernates); every run 21-24 Oct was a StartWhenAvailable catch-up ~6 min after morning wake. On 25 Oct even the catch-up failed (woke 08:54, no run all day; Task Scheduler log is disabled so exact cause unknown). FIXED 25 Oct: tasks also fire 2 min after sign-in/unlock; automation/daily.py once-a-day guard (logs/daily_state.json, max 2 tries; `--force` overrides). Task Scheduler history log still off (needs admin: `wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true`).

**Why:** he cleared context mid-build once and does not want details invented; verify files exist. Related: [[pending-decisions-2026-10-20]], [[events-calendar]].
