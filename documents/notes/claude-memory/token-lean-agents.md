---
name: token-lean-agents
description: "Videos: one pass each (one cutter, one planner), no reviewer agents, Manit checks; small fixes in main chat; portal postings fetched directly"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 7b847045-70e9-41dc-8bea-c101f7204eb0
  modified: 2026-10-27T07:55:39.775Z
---

Manit noticed subagents burn far more tokens than the main chat (2026-10-27: Tesla video used ~500-600k tokens across 3 cutter/reviewer rounds). On 2026-10-27 (Affinda) he went further: "This fast approach should be everytime instead of 3 times of cutting and checking. Move fast. Let me check and then we move ahead."

1. `/video cut`: one video-cutter, **no cut-reviewer**. Glance at check_cut's report, fix only clear failures in main chat, then straight to gate 1. Manit is the reviewer.
2. `/video plan` / `build`: one visual-planner, **no visual-reviewer**. Render once, spot-check a few frames, hand to Manit. His notes are applied in main chat (SendMessage the same planner only if real re-planning is needed).
3. Reviewer agents only when Manit asks for them.
4. `/apply` Step 0: installed-portal URLs fetched in main chat, output to a scratch file, read only after `posting_guard.py`.

**Why:** each agent starts cold and re-reads everything; review loops cost more than Manit watching the draft.

**How to apply:** encoded in `.claude/commands/video.md` and `apply.md`. Keep status updates to one line. Related: [[video-pipeline-plan]]
