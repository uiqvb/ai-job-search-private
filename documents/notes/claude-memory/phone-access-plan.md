---
name: phone-access-plan
description: Deferred plan (2026-10-21) to run the pipeline from his phone via a private repo + cloud sessions; nothing built yet
metadata:
  node_type: memory
  type: project
  originSessionId: 42e4c64a-46b7-40f7-9037-75f8d23028d5
  modified: 2026-10-26T08:52:04.612Z
---

Manit wants to start job-pipeline sessions from his phone, including when the laptop is asleep in his bag. He deferred the setup on 2026-10-21 ("we will set it up later"). Full plan is in `documents/notes/log.md` under 2026-10-21.

- Remote Control (`claude remote-control`) only works while the laptop is awake.
- Agreed direction: one new **private** GitHub repo for the whole workspace, including personal data. Keep MadsLorentzen as `upstream` for fetch only, and disable pushes to upstream and the public fork `uiqvb/ai-job-search`. Add a git-pull SessionStart hook and a commit+push Stop hook. `run_job.py` pulls/pushes around the night jobs. Cloud sessions push to master.
- Word builds stay on the laptop.
- Also to do later: Codex fallback in `run_job.py` (rerun with `codex exec` when Claude fails or is out of usage), plus a `codex exec` wrapper so the `/apply` reviewer step works under Codex. See log 2026-10-21.

**Status 2026-10-26:** private repo `uiqvb/ai-job-search-private` created; remote `origin` = private, `public-fork` and `upstream` are push-disabled. `tools/push_private.sh` force-adds personal files (no resumes, video media, config.json, .env) and mirrors memory to `documents/notes/claude-memory/`. First commit 25cf333 made, push still pending (needs `gh auth refresh -s workflow`). The auto-mode classifier blocks Claude from running the push, so Manit runs it with `!`. Brother will clone it; he runs /reset + /setup. Hooks not built yet.

**Why:** the repo was public, so personal files are git-ignored and a cloud session couldn't see them.

**How to apply:** when he says "set up phone access", start from the log entry and confirm before creating the repo. Related: [[automation-setup-in-progress]], [[job-records-locations]].
