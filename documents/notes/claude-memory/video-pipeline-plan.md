---
name: video-pipeline-plan
description: "Deferred plan (2026-10-21) for a two-phase intro-video pipeline with approval gates; build later, not now"
metadata:
  node_type: memory
  type: project
  originSessionId: 2b5088f9-1551-4967-931a-bbb8b7cb9c34
  modified: 2026-10-21T11:40:12.160Z
---

Manit's idea (2026-10-21), **to build later, not now**: make the intro-video workflow a phased pipeline.

**Phase 1 (autonomous):** from the raw takes, auto-produce the full talking-track cut and add background music. A separate reviewer agent checks every cut transition (dead air, clipped words, visible turn-away) and fixes it before handing over. Human gate: Manit approves the music cut.

**Phase 2 (after approval):** first lay out a visual plan: which B-roll goes where, graphics and stat cards, animations, captions. Manit approves the plan, then it's rendered on top of the approved cut. Human gate: Manit watches the final, describes changes, iterate until approved.

**Why:** the Capgemini video (21 Oct) took many manual rounds (rough cut v1-v3 trimming dead air and turn-aways); Phase 1 should finish with little human input.

**How to apply:** when he says to build it, start from the existing pieces in `documents/video/` (PROTOCOL.md, SCRIPT-RULES.md, capgemini/ cut_talking_track.py, build_timeline.py, Remotion editor) and confirm the design before coding. Related: [[intro-video-outreach]], [[video-script-style]], [[automation-setup-in-progress]].
