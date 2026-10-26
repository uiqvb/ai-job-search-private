# 08. A Log Is Not Yet Evidence

**Hook:** The rollback engine reconstructs robot state from the record rather than from whatever
the robot reports, because a half-applied reversal would log the robot at a position it was
never in.

**Used in:** CSIRO (Technology 14, the Learning Engine preference).

**Best for:** backend and distributed systems roles, data integrity, auditability, research
projects that turn history into knowledge.

---

## The story

- The backend records every dispatched and completed action to a queryable job and workflow
  execution history.
- The rollback engine reconstructs robot state **from that record**, not from whatever the robot
  reports, because a half-applied reversal would otherwise log the robot at a position it was
  never in.
- Every reported action is replayed through **simulation before anything is committed**.

## The idea worth stating

> A log is not yet evidence. The work is in deciding what the record has to guarantee before
> anyone is allowed to draw a conclusion from it.

That sentence is the whole reason this story exists. It converts an implementation detail into a
research-shaped claim, which is why it carried the Technology 14 preference.

## The mechanism, in the order that lands (for interviews)

1. Every claim response carries the command's inverse, so the robot is told how to undo a command
   at the moment it is given it, and builds a local LIFO undo stack as it works.
2. A seven-second watchdog detects connection loss. The robot pops five inverses and reverses
   itself unaided, driving back toward connectivity.
3. On reconnect it reports what it executed. The backend replays that through simulation before
   committing any of it.
4. Both the dashboard path and the offline path call one `CompensationBuilder`, so the two cannot
   drift apart.

**The design decision worth leading with.** Rollback used to be keyed by workflow id, which is
wrong in principle: position is cumulative and ignores workflow boundaries, so undoing a
non-top-of-stack workflow produces off-grid nonsense. Making the offline path LIFO by
construction makes that broken case unrepresentable rather than merely discouraged.
Hardware-verified 1 August 2026.

## What it evidences

- Distinguishing what a system recorded from what actually happened
- Designing for the failure mode rather than the happy path
- Making an invalid state unrepresentable, which is a stronger claim than validating against it

## Length variants

**One line.** I built a compensating-transaction rollback engine that reconstructs robot state
from an auditable execution history rather than from the robot's own report.

**Short.** My backend records every dispatched and completed action to a queryable job and
workflow history, and the rollback engine reconstructs state from that record rather than from
whatever the robot reports, because a half-applied reversal would log the robot at a position it
was never in. Every reported action is replayed through simulation before commit. Building it
taught me that a log is not yet evidence, and the work is in deciding what the record has to
guarantee before anyone draws a conclusion from it.

## Facts and verification

Verified against the repo in `../CLAUDE.md` (audit dated 2026-08-08):

- Compensating transactions, `RollbackService` and `CompensationBuilder` over `JobHistory` and
  `WorkflowHistory`. Reversal of completed actions from auditable execution history: verified.
- ❌ **"Saga pattern" is banned.** No orchestrator, no distributed coordination. Do not reinstate.
- Verified safe: 18 controllers, 16 bounded contexts, hardware-neutral REST platform,
  HMAC-SHA256 device credentials, four-tier per-device permission model.
- "Exposed through Swagger/OpenAPI", never "documented in".

## Do not say

- "Autonomous robots". `context.md:15` states the robot deliberately holds no plan of its own.
  Intelligence is server-side, and that is the actual thesis.
- "14 bounded contexts" or "5-tier permissions". Both were corrected by the audit to 16 and 4.
