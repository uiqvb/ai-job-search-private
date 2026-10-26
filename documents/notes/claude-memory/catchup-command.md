---
name: catchup-command
description: "/catchup is Manit's one-command daily update (scrape + gmail sync + buried-reply sweep + dashboard); built 2026-10-25"
metadata:
  node_type: memory
  type: project
  originSessionId: b62f6b40-1258-4111-9cb5-405316f2cd3b
  modified: 2026-10-25T03:30:47.820Z
---

Manit asked (2026-10-25) for a single command that runs scrape and Gmail sync, finds important updates he hasn't seen (e.g. a reply buried in email), flags important jobs, and rebuilds the dashboard. Built as `.claude/commands/catchup.md` (`/catchup`, args `fresh` / `quick`). It runs `automation/run_job.py <job> --no-push` in parallel, reusing today's scheduled runs unless `fresh`.

**Why:** /gmail-sync only searches tracked companies + ATS domains, so EOI replies from planned-list startups or mail in Spam/Promotions could be missed.

**How to apply:** when he says "catch me up", "what's new" or similar, run /catchup. First real run on 2026-10-25 was not yet done; check its output and refine the sweep queries if noisy. Related: [[automation-setup-in-progress]], [[job-records-locations]].
