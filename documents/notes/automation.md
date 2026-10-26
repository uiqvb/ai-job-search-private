# Job-search automation

Private (documents/notes/ is gitignored). Never put the topic in a tracked file: the repo is public.

## Phone notifications (ntfy)
- App: ntfy (Play Store / App Store)
- Server: https://ntfy.sh (default)
- Topic: `manit-jobs-ab049e4bfb76`
- Anyone who knows the topic can read and post to it. If it leaks, pick a new random name, update `automation/config.json`, and resubscribe in the app.
- Working on his phone since 2026-10-20.

## Scheduled tasks (Task Scheduler folder \JobSearch\)
| Task | Time | What |
|------|------|------|
| gmail_sync | 01:00 | `/gmail-sync --unattended`: queues status changes in gmail_sync/pending.md, updates events |
| scrape | 03:00 | `/scrape`: new matches to job_scraper/latest_scrape.md |
| event_reminders | 05:00 | Push for today's events (no Claude usage) |

- Jobs run overnight; ntfy holds every push until 07:30 (`deliver_at` in automation/config.json). A run that catches up after 07:30 pushes straight away.
- Wakes the laptop on mains power and battery (battery enabled 2026-10-20). Missed runs catch up when it wakes.
- One push per run: headline title, bullet list, up to 3 tap-to-open posting buttons.
- Must stay signed in to Windows (sleep/lock is fine).
- Logs: automation/logs/
- Reinstall: `powershell -ExecutionPolicy Bypass -File automation\install_tasks.ps1`
- Remove: same command with `-Remove`
