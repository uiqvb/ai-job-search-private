---
name: job-records-locations
description: "Where Manit's applications, scraped jobs and outreach lists are stored (all inside ai-job-search since 2026-10-20)"
metadata:
  node_type: memory
  type: reference
  originSessionId: db590f69-c67c-4633-ae52-9d0821e545a9
  modified: 2026-10-20T05:48:54.734Z
---

- Applications: `ai-job-search/job_search_tracker.csv` (28 rows, migrated 2026-10-20) and `documents/applications/<company>_<role>/`. Work log: `documents/notes/log.md`. `~/Documents/Resume` is now an archive (videos + ID docs only remain there).
- Planned-but-not-sent list: `planned_applications.csv` (repo root, 37 rows on 2026-10-20; columns priority, company, opportunity, type, send_as, location, deadline, why, contact, source, next_step). `/html-report` shows it as "Planned: to send". When the user names a company with no URL, search this file first (fuzzy: "artitecta" was Arcitecta).
- Scraped postings: `job_scraper/seen_jobs.json`.
- Cold-outreach pack + EOI target list: `documents/applications/cold_outreach_2026_10_16/`.
- Bun is not installed, so portal CLIs (linkedin-search etc.) don't run; /scrape falls back to web search.

Related: [[intro-video-outreach]], [[only-finished-projects]]
- Academic transcript (Deakin WebConnect PDF): documents/academic/Deakin_Academic_Transcript_WebConnect.pdf. Attach it when an application asks for a transcript.
