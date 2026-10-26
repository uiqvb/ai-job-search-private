# CLAUDE.md

Instructions for working on Manit Khera's job applications. Read this before touching any
resume or cover letter.

---

## The two sources of truth

There are exactly two, and they answer different questions. Do not confuse them.

### 1. `Guides/` decides HOW anything is written and formatted

**The official DeakinTALENT guides are the single most important source of truth while
building a resume or cover letter.** They override my defaults, general resume advice, and
anything a previous version of a document happened to do.

| Question | Answer lives in |
| --- | --- |
| Structure, length, sections, fonts, what is banned | `Guides/Resume-Guide.md`, `Guides/Cover-Letter-Guide.md` |
| How to phrase a bullet | `Guides/Resume-Guide.md`, the APR formula and action verb bank |
| How to read an ad and pull keywords | `Guides/Reading-a-Job-Advertisement.md`, `Guides/Tailoring-Your-Application.md` |
| Final pass before anything ships | `Guides/Checklists.md`, both official checklists |
| The originals, if there is ever any doubt | `Guides/Source/` (the two PDFs and two transcripts) |

If a formatting instinct conflicts with the guides, the guides win. If the guides are silent,
say so rather than inventing a rule.

#### Always build on the official templates in `Templates/`

**Every resume and every cover letter is built by opening the DeakinTALENT template and editing
it. Never recreate the layout from scratch, and never fork a previously built document.** This
is the guide's own step 3: "Start with a DeakinTALENT resume template. Select your preferred
format from the options available and save/rename the file. You can then edit the document
directly rather than starting from scratch."

| Document | Base file |
| --- | --- |
| Resume | `Templates/Resume-Template-3-Casual-Part-time-work-310122.docx` |
| Cover letter | `Templates/Cover-Letter-Template.docx` |

Template 3 is preferred over Template 1: it is the 2022 revision, it carries real list
numbering, and Template 1 is Times New Roman from 2020.

In practice this means opening the template with python-docx, stripping the placeholder body
while keeping `sectPr`, and writing content back using the template's own styles. See
`Scripts/build_sea_assistant_resume.py` for the pattern, including `clear_body()`.

**What the template dictates and is not ours to change:** font (Verdana), name at 24pt bold,
headings at 11pt bold title case, body at 9.5pt, its bullet list (numId 6), margins, the
`Phone: / Email: / Address: / LinkedIn:` contact format, and the section names (Career Profile,
Education, Employment, Courses and Certificates, Volunteer Experience, Extra-Curricular
Activities, Referees).

**What may be edited, because the guide requires it:** which sections appear, and their order.
The template says "remove any sections that are not relevant to you", and the guide says to
order content by what is of most interest to the employer.

⚠️ **The two templates disagree on font.** The resume template is Verdana, the cover letter
template is Calibri. The cover letter checklist settles it: "Font style and font size is the
same as used in the resume", and the two must look like one application package. **The resume
wins, so cover letters are set in Verdana at the resume's body size.** Do not "correct" this
back to Calibri.

⚠️ **Verdana is wide.** Content that fits one page in Calibri will not fit in Verdana. Budget
for roughly a third less text, and check the page count with Word COM rather than guessing.

### 2. This file decides WHAT goes in

Everything below the line is the authoritative record of Manit's actual content: education,
experience, projects, numbers, what has been verified, what has been ruled out, and what is
still open. It absorbed the old `README.md` on 2026-08-13.

**Never write a count, a score, a date or a pattern name from memory.** Check it here. This file
records a code audit that corrected four claims which had already shipped on a real resume.

`Stories/` is the narrative layer built on top of this content, for cover letters. Assemble a new
letter from `Stories/`, do not copy the last letter and edit it.

---

## The default resume

**`Current/1_Manit_Khera_Resume.docx` is the base for every new tailored resume.** Start from it,
cut and reorder for the specific role, save the tailored output under a new name. Do not start
from scratch and do not start from an archived tailored version.

**It is a technical resume.** It is built for backend and embedded software roles, and its
content, ordering and keyword surface all assume a technical reader.

**If the target role is not technical, stop and ask before tailoring.** A non-technical or
partly-technical target (student ambassador, customer-facing, admin, research-support,
generalist graduate program) changes which experience leads, which projects survive the cut,
whether the club and volunteer work moves up, and what the career profile claims. Ask about:

- What the role actually is, and the ad or position description if there is one
- Which experience he wants leading
- Whether the technical projects stay, get compressed, or come out
- Length, since the guides cap the resume at three pages and cover letters at one

Do not guess at any of that. The precedent for a non-technical tailoring exists in
`Archive/Resumes/Manit_Khera_Resume_Deakin_SEA*.docx`, but confirm rather than assume it applies.

---

## Repository layout

| Folder | Contents |
| --- | --- |
| `CLAUDE.md` | This file. Source of truth for resume and cover letter **content**. |
| `Current/` | The live default resume, `1_Manit_Khera_Resume.docx` / `.pdf`. Technical. |
| `Guides/` | Source of truth for **formatting and process**. Extracted DeakinTALENT guidance plus originals in `Guides/Source/`. |
| `Stories/` | Story bank for cover letters, extracted from every letter sent. Index at `Stories/README.md`. |
| `Applications/` | Live application outputs, one folder per role, files named for submission. |
| `Templates/` | Official DeakinTALENT .docx templates. |
| `Job_Ads/` | Saved position descriptions. |
| `Scripts/` | python-docx build scripts for every document produced so far. |
| `Personal_Documents/` | Visa, IELTS, passport. Not application material. |
| `Archive/` | Every superseded resume and every cover letter sent, plus old backups. Read-only history. |

## Work log

**`log.md` is the running, timestamped record of what happened.** At the start of every
session run `python Scripts/log_recent.py` to read the last 3 days. During the session,
append a `- HH:MM` line under today's `## YYYY-MM-DD` heading (add the heading if missing)
for every decision, application sent, reply received, correction, and anything left pending.
Append only; never rewrite old entries.

## Working rules

- **Build .docx files with python-docx**, never by unzipping, editing `document.xml` and
  rezipping. See the file-state note at the end of this document for why.
- **No em dashes.** Anywhere: resume bullets, cover letters, chat replies. Older notes in this
  file still contain them, leave those, do not add more.
- **UK spelling** throughout: organisation, optimise, programs.
- **Dates:** Manit writes numeric dates US-style (M/D/YYYY) despite being in Melbourne. Convert
  to unambiguous written form ("November 2025") and read it back to him.
- **Verify before printing.** Anything marked ❓ or ⚠️ below is unresolved. Resolve it or leave
  it out, do not print it and hope.
- Items marked ❌ or "do not reinstate" are closed decisions. They are recorded so they are not
  reinvented later.

---

# Resume content, verified

Last content update: 2026-07-24. Merged into this file 2026-08-13.

**Target roles:** backend and embedded software internships / part-time tech roles.

## Status legend

- ✅ **Confirmed** — verified with Manit, safe to print.
- ❓ **OPEN** — unanswered. In the .docx these appear as red (`C00000`) `[TBC: ...]` text.
  Red text == unanswered question. When answered, strip the red colour too.
- ⚠️ **Decision** — needs Manit to choose before the resume goes out.

---

## Header ✅

```
Manit Khera
0412 761 206  |  manitkhera26@gmail.com
Blackburn South, VIC  |  linkedin.com/in/manit-khera-603957252
```

## Career Profile ✅

> Software Engineering (Honours) student at Deakin University (WAM 81.33) seeking backend
> and embedded software roles, with perfect scores in Backend Development and Data
> Structures & Algorithms, and 93 in Embedded Systems. Particularly drawn to the
> hardware–software boundary: for my backend unit I integrated a REST API with a
> self-built 2WD line-tracking robot as a smart clothesline proof of concept, earning
> 100/100 and selection for the Deakin Open Day showcase. Experienced in C#/ASP.NET Core
> and Entity Framework Core, alongside a year maintaining the website of a community
> not-for-profit.

**Changed 2026-07-24:** previously read "a year managing the website **and IT
infrastructure** of a community not-for-profit". Manit confirmed the role was website
maintenance only — there is no separate IT-infrastructure work. Do not reinstate.

## Technical Skills

```
Languages:          C#, C++, Python, JavaScript, TypeScript, SQL
Backend:            ASP.NET Core, Entity Framework Core, REST API design
Databases:          MySQL, PostgreSQL
Frontend:           React, Next.js, Vite, HTML/CSS
Tools & Platforms:  Git, GitHub, Docker, Jenkins, Postman, Swagger/OpenAPI,
                    WordPress, Elementor
```

MySQL is real experience — from the Database Fundamentals unit at Deakin. PostgreSQL is
from the Robot Controller API. Both verified 2026-07-24.

**Corrected 2026-08-08:** this line previously read "C#, Java, ..." while the built .docx
said C++. Manit confirmed **C++, not Java.** The .docx was right; this file was wrong.

## Education ✅

```
Bachelor of Software Engineering (Honours)        March 2025 – 2028 (expected)
Deakin University, Burwood
Weighted Average Mark: 81.33
100 — Data Structures & Algorithms  |  100 — Backend Development
93 — Embedded Systems  |  92 — Object-Oriented Programming
Backend unit project selected for showcase at Deakin Open Day
```

---

## Experience

### IT Support (Volunteer) — Boroondara Stroke Support Group ✅

**July 2025 – Present** (12 months as at July 2026)

**FINALISED 2026-07-24.** These six bullets are confirmed and signed off — use verbatim.

- Maintained the WordPress site (OceanWP, Elementor) that publishes a community
  not-for-profit's programs, calendars and donation information, as part of a small
  volunteer team.
- Ran the monthly activity-calendar publication cycle across 12 months — uploading each
  new schedule, superseding the outdated version, updating page links and verifying the
  document opened correctly for visitors.
- Designed and built new pages in Elementor for a proposed site refresh, working within
  an established multi-plugin production environment.
- Diagnosed and rolled back a change that broke a live page, restoring service without
  external developer support.
- Authored a redevelopment plan for the site, backed by a WordPress Site Health audit of
  PHP memory ceilings, upload limits, server and database configuration and storage
  footprint — which identified the hosting tier's memory limit as the blocker to
  implementation.
- Trained new volunteers to publish the monthly activity sheet themselves.

**Confirmed facts behind these bullets:**

- Maintained an existing site. Made a few page changes — **not** a revamp or rebuild.
- **NOT the sole person maintaining the website** (corrected 2026-07-24). An earlier
  draft claimed "sole technical point of contact" — wrong. Do not reinstate.
- Updated the monthly calendar activity sheet every month.
- **Built new pages in Elementor**, which were subsequently discarded.
- Broke something once, rolled it back, fixed it.
- Audited technical issues but did **not** remediate them.
- **Authored a redevelopment plan.** The organisation did not act on it because of
  memory constraints.
- Showed a few newer volunteers how to update the monthly activity sheet.
- Took requests mainly from Roohi Bhatia and Helena.

**Do NOT add these — explicitly ruled out (2026-07-24):**

A large AI-generated bullet dump exists for this role. Almost all of it is unusable —
"Recognised that…", "Considered…", "Supported planning for…" are awareness statements,
not accomplishments, and will not survive an interview. Specifically ruled out:

- ❌ "Rebuilt" the website — he did not.
- ❌ Applied plugin/theme updates — he identified pending updates only.
- ❌ Took backups or set up staging — recommended, never done.
- ❌ Performed optimisation (image resizing, DB cleanup, cache config) — diagnosis only.
- ❌ AI-assisted redevelopment scoping — speculative, not delivered work.
- ❌ Any metrics on visitors, audience size, or count of links fixed — unknown.
- ❌ "IT infrastructure" beyond the website.
- ❌ "Sole technical point of contact" — he shared the work with others.

(The redevelopment plan was previously listed here as ruled out. That was wrong — Manit
authored it. It is now bullet 5.)

**Unverified numbers** — the dump cites a 1.12 GB install, 645 MB media, 32 MB upload
limit, LiteSpeed, MariaDB, GD, no OPcache. These came from an AI summary, not from
Manit directly. The audit bullet above deliberately omits them. Only add specific
figures after re-reading the actual Site Health screen.

### Customer Service Assistant — 7-Eleven, Noble Park, VIC

**July 2025 – October 2025**

**Updated 2026-07-24** — confirmed by Manit, wording drafted, not yet signed off.

- Delivered front-line customer service in a high-volume retail environment, handling
  transactions, enquiries and escalated complaints through to resolution without
  manager involvement.
- Opened and closed the store unsupervised — cash float set-up, safe drops, end-of-shift
  EFTPOS and cash reconciliation, and investigating variances to resolution.
- Operated the POS and fuel console systems, resolving pump authorisations and transaction
  disputes, and processing digital, fuel-app and loyalty payments.
- Trained new starters on POS, food safety and shift routines, and maintained compliance
  with food-handling procedures and age-restricted sales legislation.

**Confirmed facts behind these bullets:**

Manit confirmed (2026-07-24) he did all of the following: solo/unsupervised shifts,
open and close including float and safe, trained new starters, high-volume peak service,
food-safety and temperature procedures, stock rotation and markdowns, deliveries and
replenishment, age-restricted sales compliance, fuel console and store management system,
digital/fuel-app/loyalty payments, EFTPOS and cash reconciliation including variance
investigation, and escalated complaint handling.

Four bullets selected from that set on relevance — trust/responsibility and systems
first, routine retail duties (stock rotation, deliveries, planogram) omitted as low value
for a backend/embedded application.

**Deliberately omitted:**

- ❌ Any recognition or commendation bullet. Manit and his manager parted on bad terms.
  Nothing dishonest about leaving it out — but **do not list 7-Eleven as a referee** and
  do not invent a positive-relationship claim that a reference check would contradict.

- ❓ **OPEN:** customers served per shift at peak. A real number would strengthen bullet 1
  ("200+ customers per shift" beats "high-volume"). Do not print a figure until Manit
  gives one — an invented number is the kind of detail an interviewer probes.

---

## Projects & Competitions

### Robot Controller API — Deakin University, Backend Development Unit ✅

**Trimester 1, 2026**

**Tech line:** .NET 8 · ASP.NET Core · C# · PostgreSQL · EF Core · ADO.NET/Npgsql

**Links:** demo video https://youtu.be/ZW7Ps9AMmc0 ·
code https://github.com/uiqvb/RobotControllerApi

**DECIDED 2026-08-08 — Manit's call, closed. Stop raising this.** The committed
`appsettings.json` connection string was flagged to him repeatedly across sessions. He has
decided the repo link ships as is. Do not re-raise it, do not add caveats about it to
future resume versions, and do not drop the source link "just to be safe".

(Kept for the record only: `appsettings.json` carries a live PostgreSQL connection string
with user `postgres`. If he ever asks to fix it, the steps are move secrets to
user-secrets or environment variables, commit placeholders only, gitignore
`appsettings.Development.json`, and rotate the password anywhere it is reused, noting it
stays in git history unless the history is rewritten.)

**REVISED 2026-08-08 after a code audit of the actual repo.** Supersedes the 2026-07-24
"finalised" wording. Four claims in that version were wrong or overstated and are
corrected below. See "Code audit corrections" after the bullets.

- Built a hardware-neutral REST control plane for fleet robotics across 18 controllers
  and 16 bounded contexts, keeping all planning server-side so the robots run no logic of
  their own. Awarded 100/100 and selected from the cohort for showcase at Deakin Open Day.
- Designed a compensating-transaction rollback engine that ships each command's inverse to
  the robot at dispatch, so a disconnected robot reverses its own movements from a LIFO
  undo stack; reported actions are replayed through simulation before commit, so a partial
  rollback can never record a false position. Verified end to end on hardware.
- Secured every endpoint behind named authorization policies across two auth schemes,
  HMAC-SHA256 device credentials for robots and HTTP Basic for humans, with a 4-tier
  per-device permission model exposed through Swagger/OpenAPI.
- Implemented three interchangeable persistence layers (raw ADO.NET/Npgsql, EF Core, and a
  FastMember generic repository) behind one common interface set, selectable at runtime
  from a single config value with zero changes to business logic.
- Integrated the backend with a self-built 2WD line-tracking robot chassis developed for
  the embedded systems project, as a smart-clothesline proof of concept.

**Code audit corrections (2026-08-08).** Verified against the repo, not from memory:

| Old claim | Correction |
| --- | --- |
| "14 bounded contexts" | **16.** `BoundedContexts/` holds 17 folders; `Shared` is a shared kernel, not a context. The old number undersold it. |
| "5-tier per-device permission model" | **4 tiers**, rank-compared in `DevicePermissionAuthorizationService.cs:62`. Nothing defines a fifth. Fastest thing for an interviewer to catch. |
| "Documented the full API surface with Swagger/OpenAPI" | Overstated. Zero `/// <summary>` comments across the 18 controllers and no `GenerateDocumentationFile` in the .csproj; it is default Swashbuckle reflection. What *is* deliberate is wiring the custom Basic handler into the Swagger UI (`Program.cs:79`). Use **"exposed through"**, never "documented in". |
| "orchestrating autonomous robots" | Contradicts the design. `context.md:15`: "The robot deliberately holds no plan of its own." Intelligence is server-side. Calling them autonomous throws away the actual thesis. |
| "Saga-pattern" | A stretch. No orchestrator, no distributed coordination. It derives inverse commands from a catalogue (`InverseCommandName` + `RollbackKind`). **"Compensating-transaction" is accurate and tighter**; "Saga" invites a choreography-vs-orchestration question that would have to be walked back. |

Verified correct and safe to keep: 18 controllers; hardware-neutral REST platform;
HMAC-SHA256 device credentials (`HmacSha256DeviceCredentialSecretHasher`, keyed, secret
shown once); reversal of completed actions from auditable execution history
(`RollbackService` + `CompensationBuilder` over `JobHistory`/`WorkflowHistory`).
100/100 is not code-verifiable, and stays on Manit's word.

**The rollback mechanism, in the order that makes it land** (use for interviews):

1. Every claim response carries the command's inverse (`WorkItemClaimResponse`), so the
   robot is told how to undo a command at the moment it is given it, and builds a local
   LIFO undo stack as it works.
2. A 7-second watchdog detects connection loss; the robot pops 5 inverses and reverses
   itself unaided, driving back toward connectivity.
3. On reconnect it reports what it executed. The backend replays that through simulation
   before committing any of it, because a half-applied rollback would otherwise record a
   position the robot was never at.
4. Both the dashboard path and the offline path call one `CompensationBuilder`, so the two
   cannot drift apart.

**The design decision worth leading with:** rollback used to be keyed by workflow id,
which is wrong in principle. Position is cumulative and ignores workflow boundaries, so
undoing a non-top-of-stack workflow produces off-grid nonsense. Making the offline path
LIFO by construction makes that broken case unrepresentable rather than merely
discouraged. Hardware-verified 1 Aug 2026.

✅ **RESOLVED 2026-08-08 — third persistence layer is the FastMember generic repository.**
Manit confirmed. The three layers are raw ADO.NET/Npgsql, EF Core, and a FastMember
generic repository. The 2026-08-08 audit's "in-memory" reading was wrong. Safe to
enumerate them.

**Held back as interview material, not bullets** (all verified, any could buy back a line
if a version needs one): the interchangeable persistence layers; the timestamp-skew bug
that silently disabled lease expiry; and the buck-converter fix proved via
`bootId`/`resetCause` telemetry rather than a multimeter.

  **Changed 2026-07-24:** previously read "…and validated all 14 bounded contexts with
  idempotent Newman/Postman regression suites". **Newman/Postman testing removed at
  Manit's instruction.** It also conflicted with his repo README, which states the project
  has thin test coverage — a reviewer reading both would have spotted it. Do not reinstate.
  (Postman remains in the skills list: the repo does contain Postman collection and
  environment files, so the tool experience is genuine.)

**Interview leads:** the offline LIFO self-rollback (the robot reverses itself with no
backend at all, and the replay-before-commit rule that keeps recorded position honest),
and the workflow-id-to-LIFO redesign that made the broken case unrepresentable.

**Keywords this entry surfaces:** .NET 8, ASP.NET Core Web API, C#, PostgreSQL, Entity
Framework Core, ADO.NET, Npgsql, REST, Domain-Driven Design, Dependency Injection,
Repository Pattern, compensating transactions, HMAC-SHA256, authorization policies, RBAC,
Swagger/OpenAPI, Postman, IoT.

⚠️ **Do not reinstate "Saga"** anywhere in this entry. Removed 2026-08-08 as inaccurate.

**Note:** the old bullet "Built a RESTful control API in C#/ASP.NET Core with Entity
Framework Core for persistence" is superseded and inaccurate — EF Core is one of three
interchangeable layers, not the persistence choice. Do not reinstate.

### Smart Clothesline Robot — Deakin University, SIT210 Embedded Systems ✅

**Trimester 1, 2026** (same trimester as the Robot Controller API — they interoperate)

**Tech line:** Arduino Nano · C/C++ · Raspberry Pi · Python/Flask · MQTT · I²C · systemd

**Links:** demo video https://youtu.be/7QVj2lUGF2s ·
code https://github.com/uiqvb/SIT210/tree/main/Task11.1HD

**Added 2026-07-24.** Previously missing entirely — the robot appeared only as a
sub-clause of the Robot Controller API entry, leaving **zero embedded content** on a
resume targeting embedded roles. Details below were read from the actual sketch
(`Final_project_ino_script.ino`), not from memory.

**Expanded 2026-07-24** — the Raspberry Pi tier was added after reading the repo README.
The first draft was written from the `.ino` alone and covered only the Arduino, which
badly undersold the system. Confirmed true by Manit.

- Designed and built a two-tier autonomous clothesline robot — an Arduino Nano controller
  for real-time sensing and motion, and a Raspberry Pi backend for supervision — moving
  washing between drying and sheltered zones without intervention. Awarded 93.
- Fused three sensor subsystems across I²C and analog inputs: 3× TCRT5000 infrared line
  sensors, 2× BH1750 ambient light sensors for sun tracking, and a threshold-based rain
  sensor driving the safety response.
- Implemented line-following as a 3-bit sensor-pattern state machine driving an L298N
  dual-channel motor driver, with discrete correction states for progressive off-line
  recovery.
- Built the supervisory backend in Python/Flask on a Raspberry Pi — serving a live
  dashboard of robot state, line patterns, lux readings and rain values, logging
  telemetry, and issuing commands. Deployed as a systemd service starting automatically
  on boot.
- Engineered a weather fallback layer that cross-checks unreliable rain-sensor readings
  against the Open-Meteo forecast API, issuing a MOVE_TO_SAFE command when local telemetry is
  uncertain but forecast risk is high — with location fully configurable from the
  dashboard rather than hardcoded.
- Connected both tiers over an MQTT command-and-telemetry channel — dashboard to Flask to
  broker to microcontroller, with the Arduino publishing JSON telemetry on a 5-second
  interval.
- Exposed the robot to my SIT331 Robot Controller API backend, making the same chassis
  controllable from a REST service — the integration that earned 100/100 in that unit and
  selection for the Deakin Open Day showcase.

**Pi tier confirmed detail (from repo README):** Python/Flask serving the dashboard on
port 5050 over the Pi's Tailscale IP; runs as `smartclothesline.service` under systemd;
dashboard shows robot state, target location, recent events, line pattern, rain value and
left/right BH1750 lux; weather location (name, lat, lon, timezone) configurable at runtime.
Command path: dashboard → Flask → MQTT broker → Arduino; telemetry returns the same way.

**Weather API: Open-Meteo** — confirmed by Manit 2026-07-24. Named in the bullet.

**Confirmed hardware (from source):** Arduino Nano; TCRT5000 ×3 on pins 8/9/10, active-low;
BH1750 ×2 at I²C 0x23 and 0x5C; analog rain sensor on A0; L298N with IN1=2, IN2=3 (left),
IN3=4, IN4=7 (right), ENA/ENB jumpered. Libraries: Wire, BH1750, WiFiNINA, ArduinoJson,
PubSubClient. Broker: broker.hivemq.com (public). MQTT commands: MOVE_TO_SAFE,
RETURN_TO_DRYING, STOP, SET_ACTIVE_TRUE/FALSE.

⚠️ **Control logic is bang-bang / pattern-matching, NOT PID.** Do not describe it as PID or
"proportional control" — it matches 3-bit sensor patterns to discrete movement commands.
If asked in interview, saying so plainly (and noting PID would be the next step) is a
better answer than overclaiming.

### First Place — DDSC Hackathon, Deakin Data Science Club

**November 2025 – January 2026** — resolved, see below

**Project: ParkSense** — Melbourne CBD parking availability prediction.
**Tech line:** FastAPI · Python · Supabase/PostgreSQL · XGBoost · Next.js · MapLibre GL

**Links:** live app https://parksense-ddsc.netlify.app/ ·
backend https://github.com/nnpvaan/parksense-be

**Decision 2026-07-24:** Manit pushed back on the earlier "don't link" advice and he is
right — it is a genuine team project he contributed to, and linking a team repo is not a
claim of sole authorship. Links included. The entry already reads as a team effort
("won a trimester-long inter-team build competition"), and the bullet says "reviewed
backend pull requests", which is exactly what the PR history shows.
Note the backend repo is under a teammate's account (`nnpvaan`), not Manit's.

**Updated 2026-07-24.** Format now understood: a Trimester 3 (summer break) hackathon run
over the non-teaching period as an exposure exercise for first-year students to build
something end to end. Best project at the end of T3 wins $100 split across the team. This
explains the 2.5-month span — **Decision 2 is resolved, the dates are correct as written.**

- Won a trimester-long inter-team build competition with ParkSense, a Melbourne CBD
  parking-availability predictor combining live City of Melbourne sensor data with a
  short-horizon occupancy model.
- Originated the ParkSense concept and ran the early data-viability research that shaped
  it — identifying usable public data sources and assessing whether the sensor feed could
  support prediction at all.
- Reviewed backend pull requests against the FastAPI/PostgreSQL service, building the
  foundations that led into my later backend work.

**Confirmed facts:**

- Format: T3 / uni-break hackathon, first-year exposure focus, $100 prize split by team.
- Manit **was not the team lead.** Team lead and data science lead was another member.
- **Manit originated the ParkSense idea.**
- His actual hands-on contribution: **auditing the code and reviewing 2 pull requests**,
  plus research-oriented tasks (data sourcing, data usability assessment, signal-vs-noise
  analysis) assigned to him as someone newer to data science.
- He credits the project with strengthening his backend foundations — which is consistent
  with the Robot Controller API coming later.

⚠️ **Honesty constraint — read before editing this entry.**

The team lead has published a detailed public write-up of ParkSense that explicitly
credits himself with the FastAPI endpoints, the MapLibre frontend, the data pipeline,
the aggregation strategy and the modelling, and describes Manit's role as research-
oriented. **Do not write bullets claiming Manit implemented the backend, built the map,
designed the pipeline or trained the model.** Those claims are contradicted by a public
source from the same small club and would not survive a technical interview.

Manit asked that the "audited code / reviewed 2 PRs" detail not appear as such. Omitting
the PR count is fine — no resume itemises that. The bullet above says "reviewed backend
pull requests" without a number, which is true and defensible.

**DECIDED 2026-08-05 — Manit's call, closed. Stop re-raising this.** He states he did work
on the backend, and has decided the shipped PDF's "Built backend foundations using FastAPI
and PostgreSQL" bullet stays. Flagged to him twice; he's reaffirmed. It ships as written.
The only live consideration left is an interviewer asking him to walk through the FastAPI
code — that's a prep item for him, not a wording problem to keep reopening.

**Resolved 2026-07-24:**

- **Field size: 4 teams.** Deliberately **not printed.** "First out of 4" undersells the
  work; the entry says "First Place" with no field size, which is standard resume practice
  and not a misrepresentation. If asked in interview, answer "four teams" plainly — do not
  imply a larger field anywhere in writing.
- **Prize was $25 per member.** Deliberately **not printed.** Prize money only helps when
  the figure signals scale; $25 makes the win read smaller than the work actually was.
- **Dates confirmed correct by Manit: November 2025 – January 2026.** The "2024" heading
  on the team lead's public write-up is disregarded. Closed.

### ~~UniHack~~ — CUT 2026-07-24

**Removed from the resume. Do not reinstate by default.**

Manit's assessment: the team built on a no-code platform, the project was weak, and while
it was a good learning experience the output doesn't stand up. Cutting because:

- It would be the weakest entry on a page that already carries a 100/100 backend project
  and a hackathon win — and it invites an interview question whose honest answer is
  "it wasn't very good".
- There is no gap to fill. The resume is already over length; removing this eases the
  trimming problem rather than creating a hole.

**Reinstate only if** applying somewhere that explicitly values rapid prototyping, low-code
or no-code tooling — in that narrow case it becomes relevant and worth writing up.
Otherwise it stays a talking point, not a bullet.

---

## Leadership & Involvement

### Committee Member — Deakin Software Engineering Club (DSEC)

**July 2025 – April 2026**

**Updated 2026-07-24** — content confirmed by Manit, wording drafted, not yet signed off.

- Built the React to-do application used as the teaching artefact for a 30-attendee club
  workshop as part of the development team, and solely designed the seeded defects
  attendees had to locate and fix as a debugging exercise.
- Floated the workshop as a helper, unblocking attendees who stalled on setup and
  debugging.
- Fronted the club's Market Day stall, pitching to prospective members face to face and
  driving 100+ new sign-ups.
- Contributed to weekly committee planning, proposing initiatives including an open-source
  development program and a club hackathon.
- Photographed club events for use in promotional material.

**Confirmed facts behind these bullets:**

- Role was **committee member** — general committee support, not a named portfolio.
- **Did NOT run the React to-do session** (corrected 2026-07-24). He was on the
  development team: he **built the actual to-do application** the session was based on and
  **injected bugs into it** for the audience to find. Someone else delivered the session.
  Do not reinstate any "taught / delivered a workshop" wording.
- Was the front for Market Day; helped many people join the club. **100+ sign-ups —
  Manit confirmed 2026-07-24 that this figure applies to DSEC as well as DDSC.**
- Helped host sessions and did general work to help out.
- **No anchoring in DSEC** — that was DDSC only.
- To-do app: built **as part of the dev team**, but **the bug injection was solo**. Keep
  that distinction — it is the defensible individual claim.
- ~30 attendees at the React session.
- Committee met **every Sunday**.
- Proposed initiatives including an **open-source development program** and a **hackathon**.
  ⚠️ These were ideas/proposals — no confirmation any were adopted or delivered. Bullet is
  worded as "proposing", not "launched". Do not upgrade the verb without evidence.
- Did event **photography**.
- Roamed sessions as a helper unblocking stuck attendees.

- DSEC has **200+ members overall** (confirmed 2026-07-24).
- ❓ **OPEN:** were the OSS program or hackathon proposals ever actually adopted or run?
  If yes, that is a far stronger bullet than "proposed".

**Note on the duplicated 100+ figure:** the same number now appears in both the DDSC and
DSEC entries. Manit approved this. If both clubs shared one Market Day appearance, a
reader may notice the repetition — consider varying the phrasing, or dropping the number
from one entry, before the resume goes out.

### LinkedIn Manager — Deakin Data Science Club (DDSC)

**January 2026 – Present**

**Updated 2026-07-24** — content confirmed by Manit, wording drafted, not yet signed off.

- Own the club's LinkedIn strategy end to end — content direction, design, scheduling and
  performance measurement — consistently reaching 1,000+ impressions per post through
  tailored copy, hashtag and tagging strategy, and format/timing testing against LinkedIn
  analytics.
- Designed event graphics and promotional creative for the club's campaigns.
- Built an alumni outreach and re-engagement pipeline, contacting Deakin data science
  alumni directly to bring them back into the club's network as speakers and contacts.
- Hosted and anchored networking sessions connecting current students with alumni and
  industry guests.
- Coordinated with sponsors on co-branded content and managed the club's inbox, fielding
  enquiries from students, speakers and recruiters.
- Fronted the club at Market Day, pitching to prospective members face to face and driving
  100+ new sign-ups.

**Confirmed facts behind these bullets:**

- **The LinkedIn strategy was his own**, not inherited or executed on someone else's brief.
- Designed graphics for events.
- Tracked follower count, impressions and engagement rate in LinkedIn analytics.
- Tested posting times and formats to see what performed.
- Ran a hashtag/tagging strategy — tagging Deakin, sponsors and speakers to reach their
  networks; got the exec team to reshare posts to multiply reach.
- Alumni outreach and re-engagement; cold-messaged industry speakers and sponsors.
- Managed the inbox — replied to student and recruiter DMs.
- Coordinated with sponsors on co-branded posts.
- Hosted networking sessions **and did the anchoring** (DDSC only — not DSEC).
- Market Day: 100+ sign-ups.
- 1,000+ impressions per post, attributed to careful tailoring of content.

- ~~follower growth~~ — **dropped 2026-07-24 at Manit's instruction.** Don't re-ask.
- ❓ **OPEN:** posting cadence (posts per week/month)
- ❓ **OPEN:** how many alumni contacted / how many networking sessions run?
- ❓ **OPEN:** is the 100+ Market Day figure DDSC, DSEC, or both combined? Currently
  claimed under DDSC only — the same claim cannot appear in both entries.

---

## Referees

✅ **RESOLVED 2026-07-24 — both have agreed to be listed.** No longer the critical path.

1. **Maksym Slavnenko** — Unit Chair, SIT331 Backend Development, Deakin University
   - m.slavnenko@deakin.edu.au  |  +61 3 9244 5749
2. **Roohi Bhatia** — Hub Administrator, Boroondara Stroke Support Group
   - info@bssg.org.au  |  +61 478 092 028

⚠️ **Two things to verify before printing:**

- **Surname spelling.** Earlier notes recorded "Maksym **Slavenko**", but the email he gave
  is `m.slav**n**enko@deakin.edu.au`. The email spelling (Slavnenko) is almost certainly
  correct and is used above — but confirm, because misspelling a referee's name is the
  kind of error that gets noticed by the referee.
- **Phone formatting.** Manit gave "+61 3 924 45749"; a Melbourne landline is
  `+61 3 XXXX XXXX`, so this is written above as **+61 3 9244 5749**. Same digits,
  regrouped. Confirm the digits are right.

Note: Roohi's email is the organisation's general inbox (`info@bssg.org.au`), not a
personal address — fine to list, but worth knowing a caller may not reach her directly.

---

## Open decisions ⚠️

1. ~~**Frontend skills line.**~~ **DECIDED 2026-07-24.** Manit's call: keep React, Vite
   and Next.js; **remove Svelte and Vue.** Applied.

   **Angular removed too** — confirmed 2026-07-24. Final line:
   `React, Next.js, Vite, HTML/CSS`. Decision fully closed, nothing further to raise.
2. ~~**DDSC Hackathon dates.**~~ **CLOSED 2026-07-24.** T3 / uni-break hackathon running
   across the non-teaching period, hence the 2.5-month span. Manit confirmed
   "November 2025 – January 2026" is correct. No further checking needed.

## Length policy — DECIDED 2026-07-24

**Do NOT trim to one page.** Manit is engaging a professional resume writer to cut it down.
The .docx should therefore be the **detailed master version** — maximum accurate detail,
every confirmed bullet included, nothing dropped for space.

Rationale: a professional can cut, but cannot invent facts they were never given. Handing
them a pre-trimmed page throws away the material they need to make choices with.

All earlier trimming suggestions in this file (DSEC → 3, DDSC → 4, BSSG → 4–5,
7-Eleven → 3) are **superseded and should not be applied**. They are retained only as
notes for whoever does the eventual cut.

## CSIRO Undergraduate Vacation Studentship 2026/27 — built 2026-08-10

🔴 **OUTCOME: REJECTED.** Reported by Manit 2026-10-14. Rejection date and any feedback not
recorded. Closed; the notes below are kept as history and for reuse.

**Deadline: 10 August 2026, 11:00pm AEST.** Same day it was built.

Two separate files at Manit's instruction, 2 pages each, despite CSIRO's posting asking
for "resume/CV and cover letter (combined single document)". If the form has one upload
slot, merge them then.

- `Scripts/build_resume_csiro.py` → `Resume_Versions/Manit_Khera_Resume_CSIRO.docx`
- `Scripts/build_cover_letter_csiro.py` → `Cover_Letters/Manit_Khera_Cover_Letter_CSIRO.docx`

**Preferences (only 2 allowed):**

1. **Technology 11** — Human-in-the-Loop Planning for Heterogeneous Robot Teams.
   Clayton VIC. Supervisor **Kavindie Katuwandeniya** (Kavi.Katuwandeniya@csiro.au),
   Research Scientist, CSIRO Robotics. Extends an internal HRI interface called
   **RobotLinq** (unpublished, no public trace). Tests whether plan representation (text,
   diagram, video preview, spatial map) changes whether operators catch errors. Includes
   a user study with deliberately introduced plan errors. Requires 2 years study + basic
   Python; ROS/HCI/stats explicitly "advantageous but not essential". On-site lab work.
2. **Technology 14** — Learning Engine and Fleet Knowledge from Robot Experience, HART OS.
   Clayton VIC. Supervisor **Kartik Yellapantula** (kartik.yellapantula@csiro.au),
   Robotics Software Engineer. ROS2 bag data and logs → structured queryable knowledge.
   Bounded case study is a Grass Traversability Planner (grass as *conditionally*
   traversable). ⚠️ **"Most suited for final year students"** — Manit is entering 3rd of 4.
   That seniority flag is why it is preference 2, not 1.

**The three tailoring hooks (do not lose these in a later edit):**

| Their ask | Manit's evidence |
| --- | --- |
| Tech 11: planning server-side, operator reviews before execution | Robot Controller: "the robot deliberately holds no plan of its own". Same thesis as RobotLinq. |
| Tech 11: participants review plans with deliberately introduced errors | DSEC: he **solely designed the seeded defects** for 30 attendees to find. He has built their experimental instrument. Strongest line in the application. |
| Tech 14: logs → trustworthy knowledge; recovery events | `JobHistory`/`WorkflowHistory` execution history + replay-through-simulation-before-commit. Plus the clothesline weather fallback: a signal treated as *conditionally* reliable, matching *conditionally* traversable. |

**Key research find:** Katuwandeniya, Tian & Kulić, *"What did the Robot do in my
Absence? Video Foundation Models to Enhance Intermittent Supervision"*, IEEE RA-L 2025,
https://arxiv.org/html/2411.10016. Direct precursor to Tech 11: compared storyboard vs
video vs text summaries of robot activity across 30 participants; storyboards won the
accuracy/effort trade-off, users preferred visual over text, storyboards were **weaker on
event-related than object-related questions**. 🔴 **The cover letter cites this paper.
Manit must actually read it before sending, or cut those paragraphs.**

**Deliberate choices in this version:**

- ❌ **No ROS/ROS2 claim anywhere.** Manit confirmed zero exposure 2026-08-10. The letter
  names the gap outright and pairs it with the MQTT/JSON-telemetry substrate that genuinely
  transfers. Do not let a later edit soften this to "familiar with ROS" — Tech 14 runs on
  ROS2 bag data and it would be found out immediately.
- Python leads the languages line, not C#. Both briefs ask for Python.
- Projects above Experience; a research panel assesses build evidence, not retail.
- Referees **kept** (unlike the Suncorp cut). A research panel will call them, and
  Slavnenko supervised the 100/100 robot integration.
- The three-interchangeable-persistence-layers bullet was **cut** from the Robot Controller
  entry: a .NET DI detail, least relevant thing on the page to a robotics panel. Cutting it
  also kept the clothesline entry whole on page 1.
- 7-Eleven trimmed to 2 bullets.

### Resume v1 vs v2 — both live, Manit judging (2026-08-10)

| | v1 | v2 |
| --- | --- | --- |
| Output | `Manit_Khera_Resume_CSIRO.docx` | `Manit_Khera_Resume_CSIRO_v2.docx` |
| Script | `build_resume_csiro.py` | `build_resume_csiro_v2.py` |
| Length | 2 pages, 952 words | 2 pages, 851 words |

🔴 **`Manit_Khera_Resume_CSIRO.docx` (v1) has been hand-edited in Word and no longer
matches `build_resume_csiro.py`. Re-running that script will destroy the edits.** He
replaced the plain-text URLs with six labelled clickable hyperlinks (Demo video, Source
code, Live app, Backend repo). Those edits are now reproduced properly in the v2 script
via an `add_hyperlink` helper, so v2 can be rebuilt safely. If v1 wins, port the
hyperlink code into its script before ever re-running it.

**v2 changes:** profile cut 6 lines to 3 (it was repeating the project bullets below it);
every bullet front-loads its result; Robot Controller ~15% shorter with all eight
technical points kept; Swagger clause dropped entirely; key figures bolded; ParkSense
"First Place" moved into the entry title; Clothesline, Leadership and Experience tightened.

**Rejected for v2, deliberately:**

- ❌ **Promoting the seeded-defects work into PROJECTS.** Floated because Tech 11's user
  study has participants review plans with deliberately introduced errors. Manit pushed
  back and was right: it was ~15 defects in a React to-do app, a teaching exercise, and
  placing it beside the fleet control platform reads as inflation and invites a deflating
  question. Same reasoning that correctly cut UniHack. It keeps one precise bullet in
  Leadership **with the real number (15)**, and does its real work in the cover letter
  where there is room to describe the reasoning rather than imply scale.
- ❌ **Removing referees.** CSIRO does not ask for them (verified), but Manit's call is
  they stay, and it is right for a research application: Slavnenko supervised the 100/100
  robot integration. Do not remove again.
- ❌ **Plain-Englishing "bounded contexts" / "compensating-transaction rollback".** The
  readers are a robotics research scientist and a robotics software engineer, not a
  recruiter. Those terms read as competence to that audience.
- ❌ **Upgrading ParkSense to "built the FastAPI/PostgreSQL backend".** Stays "backend
  foundations". Closed twice; the team lead's public write-up claims the endpoints.

❓ **OPEN — needed for the application form, not the resume: GPA on UAC's 7-point
methodology.** Not derivable from WAM 81.33; UAC computes per unit (HD=7, D=6, C=5, P=4).
Needs the full grade list or transcript. The resume ships without it (WAM + four unit
marks carry the academic record), so the documents are submittable as they stand.

❓ **Verify before submitting:** eligibility asks for "international student with full work
rights". Subclass 500 allows unrestricted hours during scheduled course breaks, and
Nov–Feb is the break, so the placement period is fine, but confirm the wording matches
what the form asks.

## Deakin Student Experience Ambassador, Burwood — built 2026-08-12

**Closing date: 12 August 2026.** Same day it was built. HEW 1 casual, $40.55/hr,
~100 hrs/year, 6-month contract with possible 6-month extension. Requires enrolment
continuing through **Trimesters 1 and 2, 2027** (he qualifies; degree runs to 2028).

- `Scripts/build_resume_deakin_sea.py` → `Resume_Versions/Manit_Khera_Resume_Deakin_SEA.docx` / `.pdf`
- 2 pages, 728 words, 6 hyperlinks. Page break falls cleanly at SKILLS.
- Forked from `build_resume_csiro_v2.py` for the layout helpers only; content rebuilt.

🟢 **NEW FACT, stated by Manit 2026-08-12: he has already been selected as a Student
Ambassador with Deakin Future Students for Open Day.** This is the differentiator for
this application: same employer, adjacent work, already vetted. It opens the profile and
is the first entry of the first content section.
⚠️ **Written with no invented detail** (no dates, no team structure, no duties beyond
representing Deakin and speaking to prospective students). Expand it there first once he
supplies the real dates and duties.

✅ **CONFIRMED 2026-08-13: the Student Ambassador role is PAID.** It therefore belongs under
**Employment**, not Extra-Curricular Activities, and it satisfies the Student Experience
Assistant PD's special requirement "have held or currently hold an ambassador role **or job**
on campus" on the job limb rather than only the ambassador limb. Date used on the resume:
**Open Day, August 2026**.
⚠️ The tense guard still applies. Paid does not mean performed. He was selected and has not
yet worked the shift, so the bullet stays "Selected as a Student Ambassador" and any cover
letter stays "by the time this contract begins I **will have** worked that shift myself".

**Note this is a different fact from** the Robot Controller unit project being *selected
for showcase at* Deakin Open Day. Both appear on the resume and they are not the same
thing. Do not merge them.

**Structure**, deliberately not the technical order: Header, Profile, Education, Deakin
Involvement & Student Engagement, Work Experience, Skills, Academic Projects, Referees.
Engagement work is the job; the robots are supporting evidence at one bullet each.

**Header carries the posting's literal CV checklist** (first name, last name, degree,
email, phone, address). The degree is now its own header line. Address gained a postcode:
**Blackburn South, VIC 3130**. ❓ Confirm whether they want a full street address.

**Bullet selection maps to their five stated criteria:**

| Their criterion | Evidence used |
| --- | --- |
| Communication and interpersonal | Market Day pitching, anchoring networking sessions, 7-Eleven complaint resolution |
| Works in a diverse team | Two club committees, weekly planning, small volunteer team |
| Independent and proactive | Unsupervised open and close, rolling back a broken live page unaided, owning the LinkedIn presence |
| Time management | The 12-month monthly publication cycle, publishing to deadline |
| Knowledge of Deakin campuses and services | Burwood student, two Deakin clubs, Open Day showcase plus Open Day ambassador |

**Deliberate choices:**

- **The 100+ Market Day figure appears ONCE, under DSEC.** README's older note approved it
  under both clubs, but here the two entries sit adjacent and repeating it reads as
  padding. DDSC keeps the activity without the number. Nothing overstated either way.
- **"Two years of student engagement" was caught and corrected to "over a year."** DSEC
  starts Jul 2025; the dates are on the same page. Do not inflate it back.
- **Referee order flipped: Roohi Bhatia first**, Slavnenko second. Bhatia saw him work
  with people; the unit chair is the weaker witness for this role. ❓ If a DSEC or DDSC
  exec would agree to be listed, they beat Slavnenko here.
- **7-Eleven above BSSG**, reversing the CSIRO order. Front-line service is the closest
  analogue to the actual duties.
- **Line spacing dropped to 1.0** (CSIRO uses 1.05). At 1.05 the BSSG entry split across
  the page break and orphaned its last bullet. Re-check the break if copy changes.
- **BSSG cut to 3 bullets**, merging volunteer training into the publication-cycle bullet.
- Technical depth cut hard: no bounded contexts, HMAC, compensating transactions,
  persistence layers, I²C or systemd, and no tech lines. Kept 100/100 and the Open Day
  showcase because they are Deakin-facing.
- ParkSense drops its backend-foundations bullet **for space, not as a reversal**. The
  2026-08-05 decision stands if the entry is ever expanded.

### One-page variant — built 2026-08-12, both live

| | 2-page | 1-page |
| --- | --- | --- |
| Output | `Manit_Khera_Resume_Deakin_SEA.docx` | `Manit_Khera_Resume_Deakin_SEA_1page.docx` |
| Script | `build_resume_deakin_sea.py` | `build_resume_deakin_sea_1page.py` |
| Length | 2 pages, 728 words | 1 page, 538 words |
| Body size / margins | 10pt / 0.85in | 9.5pt / 0.75in |

**Recommendation: send the 1-page.** HEW 1 casual, ~100 hrs/year, screened in volume by
DeakinTALENT against a criteria list. The 190 words cut were project depth this reviewer
does not assess.

**How the page was found:** PROJECTS collapsed from three entries to one line carrying all
three results with links kept (the big saving); every entry capped at 2 bullets by
*merging*, not deleting; EDUCATION's two bullets merged; SKILLS 3 lines to 2; PROFILE 5
lines to 3.

**Nothing load-bearing was lost.** Every number survives (100+ sign-ups, 30 attendees,
1,000+ impressions, WAM 81.33, 12 months, 100/100, 93, first place, 200+ members), both
referees survive, the enrolment line survives, and the Open Day ambassador entry is still
first in the first content section.

## Deakin Student Experience ASSISTANT, Burwood — built 2026-08-12

**Separate posting from the Ambassador role above. Different file. Do not send the
ambassador resume for this one.** HEW 3, $45.80/hr, ~100 hrs/year, 6-month contract with
possible extension, 3 Burwood vacancies (also Geelong 4, Warrnambool 2). Same enrolment
gate: continuing through Trimesters 1 and 2, 2027.

- `Scripts/build_resume_deakin_assistant.py` → `Resume_Versions/Manit_Khera_Resume_Deakin_Assistant.docx` / `.pdf`
- 1 page, 607 words, 3 hyperlinks. Forked from the 1-page ambassador script.

**Why it is different:** this role's second responsibility is to *lead Student Experience
Ambassadors* at Orientation, and its cover letter question is entirely about leadership.
The ambassador resume presents Manit as a good participant; this one presents him as
someone who runs other people.

**The spine is TRAINING AND HANDOVER.** It is his real leadership evidence and it runs
through every role: new 7-Eleven starters on POS and food safety, new BSSG volunteers
taking over the monthly publication outright, attendees stalled mid-workshop. On the
ambassador version that thread was scattered; here those bullets lead with it.

**Deltas from the ambassador 1-pager:**

- Section renamed LEADERSHIP & STUDENT ENGAGEMENT.
- **DDSC moved above DSEC.** It is current, "LinkedIn Manager" is his only actual manager
  title, and it fixes the reverse-chronological order.
- 7-Eleven and BSSG bullets reordered training-first.
- Ambassador entry gains one clause: he knows the ambassador role from the inside, which
  is the role this position supervises. Sharpest line on the page for this posting.
- Header names the campus (**Burwood**), since the cover letter must confirm it.
- Skills line 1 renamed "Leadership and engagement", led by training and handover.

⚠️ **Titles are NOT inflated and must not be.** He was a committee *member* at DSEC, not
an exec or president, and the ambassador selection is a role he has been given, not one he
has performed yet. The leadership case rests on what he did (owning a channel end to end,
training people to replace him, running shifts solo), not on titles.

### Both cover letters — built 2026-08-12

| | Ambassador | Assistant |
| --- | --- | --- |
| Script | `build_cover_letter_deakin_sea.py` | `build_cover_letter_deakin_assistant.py` |
| Output | `Cover_Letters/Manit_Khera_Cover_Letter_Deakin_SEA.docx` | `..._Deakin_Assistant.docx` |
| Length | 1 page, 558 words | 1 page, 629 words |
| Questions answered | 2 (enrolment; why + standout) | 3 (campus; enrolment; leadership) |

**Both answer the posting's numbered questions explicitly and in order, in the first two
paragraphs.** These are hard eligibility gates screened in volume; they are not buried in
prose. The Assistant letter names **Burwood** in paragraph 2.

**Ambassador letter pitch:** he has already done the recruiting half of this job for a
year. Market Day stalls for two clubs is the same work as an Orientation stall, and the
100+ sign-ups are the evidence. Open Day ambassador selection goes in paragraph 3.

**Assistant letter argument, and the reason it works:** he has no leadership title worth
pitching, so paragraph 3 refuses the title frame outright ("I have not been a club
president") and replaces it with the thing he can evidence three times: in every role, the
work ended with someone else able to do it without him. Then four specific commitments on
how he would run an ambassador team (brief before the shift, take the first hard question
then hand back the second, watch for the third hour, name what went well). Those four are
the part a HEW 3 panel will remember, because most student applicants answer this question
with adjectives.

⚠️ **Tense matters in the Assistant letter.** The Open Day ambassador role is one he has
been SELECTED for, not performed. The letter says "by the time this contract starts I
**will have** worked the shift myself". Do not shift that to past tense.

⚠️ **Assistant letter geometry is tighter than the Ambassador letter's** (10pt, 0.5in top
and bottom, 0.8in sides) because it carries three answers plus the commitments. Re-check
the page count after any body edit.

❓ **Deliberately not written: any memory of Manit's own Orientation.** He has never
described one, and a fabricated version is exactly what an interviewer would ask him to
expand on. If he has a real one, it belongs in the Ambassador letter's paragraph 4 and
would improve it. The posting requires one answering two set
questions: (1) confirm enrolment continuing through Trimesters 1 and 2, 2027, and (2) why
this role and what makes him a standout candidate. Not built.

## Deakin Student Experience Assistant, Burwood — REBUILT 2026-08-13

**Supersedes the 12 August build above.** Manit rejected those files: they led with software
engineering, spent a third of a one-page resume on robotics and ParkSense, and listed Python,
C# and SQL in a student services application. **Do not fork from them.**

- `Scripts/build_sea_assistant_resume.py` → `Applications/Deakin-Student-Experience-Assistant/Manit Khera Resume.docx` / `.pdf`. **1 page, 557 words**, verified via Word COM.
- `Scripts/build_sea_assistant_cover_letter.py` → `.../Manit Khera Cover Letter.docx` / `.pdf`. **1 page, 607 body words.**
- Live application outputs now live in `Applications/<role>/`, named for submission.

**Read the position description**, `Job_Ads/Student Experience Assistant Position Description
August 2026 (1).pdf`. It carries four things the ad summary does not:

1. **Special requirement: "Have held or currently hold an ambassador role or job on campus."**
   Manit has been **selected** as an Open Day ambassador and has **not yet worked the shift**.
   ⚠️ Tense guard, same as the 12 Aug letter: "by the time this contract begins I **will have**
   worked that shift myself". Do not move to past tense until Open Day has happened.
2. **Working with Children Check required.** ✅ Manit confirmed 2026-08-13 he **holds one**.
   Stated on both documents.
3. **Infrequent evening and weekend work.** Availability line added to the letter close.
4. **Hiring manager named: Sarah Miocic**, Manager, Student Engagement and Orientation, Student
   Experience and Engagement Team, Student Services. The letter is addressed to her, not to the
   DeakinTALENT team, per the cover letter guide's instruction to address the named contact.

Also in the PD and worth reusing: **Students as Partners** is a formal framework splitting paid
rostered shifts from voluntary partnership work (focus groups, surveys, design workshops,
planning committees) recognised through a Rewards and Recognition program. The letter says
plainly that he wants the unpaid partnership half, which most applicants will not address.
❓ **Desired knowledge: Students Helping Students programs and Best Practice Principles.** Not
claimed anywhere, because he has not read them. Worth reading before the video interview.

**Formatting decision, applies to everything built from now on.** Both documents are built by
opening the official DeakinTALENT templates and editing them, per the rule at the top of this
file. That replaced a first attempt that recreated the look from scratch in Calibri, which
Manit rejected outright on 2026-08-13. The navy headings and horizontal rules used by every
earlier script are gone: the checklist bans colour and borders, and Template 3 says "change the
font colour to black". The cover letter's four shift-running commitments were converted from
bullets to prose for the same reason, since the checklist bans lists in a cover letter.

**Content decisions:**

- ~~Section order follows relevance, not the template's default.~~ **SUPERSEDED 2026-08-13,
  Manit's call: follow the template's own order.** Final order is Career Profile, Education,
  Employment, Volunteer Experience, Extra-Curricular Activities, Skills, Courses and
  Certificates, Referees. The relevance argument (put the Deakin club engagement first because
  it is the evidence being screened for) is answered instead by the **paid Student Ambassador
  entry leading Employment**, so the first entry on the page is still the Deakin-facing one.
  Do not reorder the sections again without asking.
- **Referees are reduced to "Available on request."** Template 3's own instruction is "[Omit
  this section unless specifically requested by organisation]" and the ad requests only the six
  CV fields. Full details stay in this file, ready the moment they are asked for. This also
  retired the wrapping phone number that was breaking mid-digit at the foot of the page.
- Cut to hold one page in Verdana: the DDSC inbox and sponsor bullet, the DSEC committee
  planning bullet, and the standalone WordPress bullet, which is now merged with the rollback
  bullet. Evening and weekend availability moved to the cover letter close.

- The whole "Academic Projects & Awards" section is **cut**. The Open Day showcase survives as
  one Education bullet, which is the only part a student services panel needs.
- Python, C#, SQL and Git are **cut** from the skills line. Not a criterion in the ad or the PD.
- **The "15 defects" figure is removed** and did not ship this time. This file records no defect
  count, only "the seeded defects". Resolve the real number before it is ever printed again.
- **100+ sign-ups appears once**, under DSEC. The duplication between the DSEC and DDSC entries
  in this file is still unresolved.
- Education start month confirmed by Manit 2026-08-13: **March 2025**. The Education block above
  still reads "2025 – 2028" and should be updated.
- Address on the CV: suburb, state and postcode is sufficient. Manit's call, 2026-08-13.

⚠️ **Still unverified before this ships:** the referee surname spelling (Slavnenko) and the
regrouped phone number +61 3 9244 5749. Both flagged in the Referees section above.

## Microsoft / Clipchamp Software Engineering Intern, Summer 2026-27 - built 2026-08-27

🔴 **OUTCOME: REJECTED.** Reported by Manit 2026-10-14. Rejection date and any feedback not
recorded. Closed; the notes below are kept as history and for reuse.

Job **200050159**, posted 24 August 2026. Applications open until **early September 2026**,
reviewed on a **rolling basis**, so it is a first-in advantage. Ad saved at
`Job_Ads/Microsoft-Clipchamp-Software-Engineering-Intern-2026.md`.

12-week full-time internship, late November 2026 to February 2027, **fully on-site** in
Brisbane, Sydney or Melbourne. No remote option. Clipchamp is Microsoft's browser-based video
editor inside Microsoft 365, so the stack is web, TypeScript and AI.

- `Scripts/build_clipchamp_resume.py` -> `Applications/Microsoft-Clipchamp-SWE-Intern/Manit Khera Resume.docx` / `.pdf`
- **2 pages, 924 words, 8 clickable links**, verified via Word COM. Page 2 starts cleanly at
  the ParkSense entry.
- Built on Template 3 like every document from 13 August onwards. Verdana, black, template
  bullet list, template section rule.
- **Resume only.** Manit's call 2026-08-27: Microsoft's form takes a resume, no cover letter
  was built.

**Section order, chosen for a software reader:** Career Profile, Education, Technical Skills,
Projects, Extra-Curricular Activities, Employment, Volunteer Experience, Referees. Education
and Skills sit above Projects because their two hard required qualifications are the degree
and computer science fundamentals; the 100 in Data Structures and Algorithms leads the
Education bullets and answers the second outright. The checklist explicitly permits a
"Projects" heading.

**Angle on the Robot Controller entry is new and deliberate.** Their responsibilities name
availability, reliability, efficiency, **observability** and performance. So the bullets are
cut to replay-before-commit and the auditable execution history, and a new bullet was written
for `JobHistory`/`WorkflowHistory` as a recoverability story. This is not the DDD-and-robotics
angle used for CSIRO. Both are true of the same code.

**Confirmed with Manit 2026-08-27:**

- **He has barely any TypeScript.** His year of object-oriented programming is **C# and C++**.
  Their required qualification says "an object-oriented language (preferably TypeScript)", so
  the preference is unmet and the requirement is met. TypeScript appears once, mid-line, paired
  with JavaScript. ❌ **Do not promote TypeScript to the front of the languages line to match
  their wording.** It would not survive a technical screen.
- **AI tooling: he uses Claude and Claude Code, not GitHub Copilot.** The ad says "GitHub
  Copilot (or similar tools)", so the skills block names what he actually uses. Do not write
  Copilot.
- ❌ **No claimed interest in online video.** Their preferred qualifications ask for one and he
  does not have it. Left unclaimed rather than invented.

**DECIDED 2026-08-27 - Manit's call, closed. Stop raising this.** The program says graduating
August 2027 to July 2028; he finishes end of 2028. He is applying anyway. The resume carries
**"March 2025 to 2028 (expected)"**, with no month, which is what every other version of his
resume says and is not a claim either way. Do not add a month, do not invent one inside their
window, and do not re-raise the eligibility gap in future sessions.

**Applying to CSIRO as well, deliberately.** The CSIRO Undergraduate Vacation Studentship runs
the same November-to-February window. Manit is applying to both and will take whichever he gets.
Not a conflict to flag.

❓ **Open, for the form rather than the resume:** whether the visa's course-break work rights
wording covers a 12-week full-time placement running into February, after Trimester 1 2027
starts in March.

## DeakinTALENT Career Ambassador, Burwood - built 2026-09-17

Ad saved at `Job_Ads/DeakinTALENT-Career-Ambassador-2027.md` (saved 16 September 2026).
HEW 1 casual, $40.55/hr, ~4 hrs/week on campus Monday to Friday, year-round, 2027 intake.
**Resume only. The ad states outright that no cover letter is required**, so the resume
carries the whole application.

- `Scripts/build_career_ambassador_resume.py` -> `Applications/DeakinTALENT-Career-Ambassador/Manit Khera Resume.docx` / `.pdf`
- **1 page, 469 words, 52 body lines**, verified via Word COM. Built on Template 3.
- Section order is the template's own, as decided 2026-08-13. Not reordered.

🟢 **FACT CHANGED 2026-09-17, confirmed by Manit: he WORKED the Open Day Student
Ambassador shift.** The tense guard that ran through every document from 12 August to
13 August ("Selected as", never performed) is now **spent**. The entry reads "Represented
Deakin at Open Day" in past tense. Do not revert it to "Selected as". The two earlier
warnings above are superseded and are kept only as history.

🟢 **NEW CONTENT, stated by Manit 2026-09-17: he advises fellow students and club members
informally on their LinkedIn profiles and resumes.** This is the closest thing he has to
the role's core duty (peer career support, resume reviews, LinkedIn). It ships as one
bullet under the DDSC entry with **no number and no named program**, because neither was
confirmed.
❓ **OPEN:** roughly how many students, and whether any of it ran through a club rather
than being purely informal. A real figure or a program name would make this the strongest
bullet on the page.

**Why the DDSC LinkedIn Manager entry leads Extra-Curricular Activities here:** "contributing
to social media content and promotional campaigns" is a named key responsibility in this ad
and was not one in either August Deakin ad. It is the single best keyword match Manit has.

**The one layout change, and it is deliberate:** the organisation name moves onto the role
line (`Title, Organisation, Location` + right-aligned dates) instead of taking the
template's second line. That saved six lines with nothing lost, and it is what bought the
single page. Everything the checklist asks for is still present.

⚠️ **52 body lines is the exact one-page ceiling in this geometry** (Verdana 9.5pt,
template margins, 1.0 spacing, headings at 2pt before / 1pt after). Line 53 breaks it.
Two things were tried, measured and cut for that reason: a "Deakin knowledge" skills line,
and the fuller club-inbox clause. **If any copy is added, re-check the page count with
Word COM. Do not estimate.**

**Cut for the page, recorded so they are not hunted for again:** the Open Day showcase
Education bullet, the 7-Eleven second bullet (merged into the first), POS and cash
reconciliation from Skills, and the DSEC seeded-defects bullet. Referees are
**"Available upon request."** per the checklist, since this ad asks for a resume and a
short form only. Full referee details stay in the Referees section above.

**Hard gates in the ad, all answered on the page** in Courses and Certificates so a
screener does not have to ask: Working with Children Check (Employee, confirmed held),
three-plus trimesters still to complete, four hours per week on campus, and availability
for the **compulsory Group Assessment Centre, Thursday 29 October at Burwood**. Manit
confirmed all of these 2026-09-17.

**Still unverified, same as every other version:** the referee surname spelling
(Slavnenko) and the regrouped phone number +61 3 9244 5749. Neither is printed on this
resume, so it ships either way.

## Deakin Applied AI Initiative research internships x3 - built 2026-09-18

Three separate project briefs, saved in `Job_Ads/` as the PDFs named for their supervisors.
**All three are the same program**, so they share one resume: Burwood on campus, **10 weeks,
UNPAID, 2 days per week, about 160 hours**, to be completed inside a 12-week trimester.
**A/Prof Scott Barnett supervises two of the three**, which is the single most important
fact about how these are read.

| # | Project | Supervisors | Manit's rank |
| --- | --- | --- | --- |
| 1 | Benchmarking Agent Workflows for Software Development | Dr Wannita Takerngsaksiri, A/Prof Scott Barnett | **First. His stated preference.** |
| 2 | Curating Real-World Manufacturing Evaluation Datasets (Overseer) | A/Prof Scott Barnett, Stefanus Kurniawan | Second |
| 3 | Smarter AI Agent Routing Through Task Understanding | Dr Aleksandar Pasquini, Prof Rajesh Vasa | Third |

- `Scripts/build_a2i2_research_resume.py` -> `Applications/Deakin-A2I2-Research-Internships/Manit Khera Resume.docx` / `.pdf`
  **2 pages, 1,047 words, 8 hyperlinks**, page 2 starts cleanly at ParkSense. Verified via Word COM.
- `Scripts/build_a2i2_cover_letters.py` -> three letters in the same folder, one per project.
  **1 page each, 633 body words each.** Verified via Word COM.
- `Scripts/verify_docs.py` is new and shared: opens a .docx in Word, prints page/word/hyperlink
  counts and exports the PDF beside it. Use it instead of another per-script copy.

🔴 **DECIDED 2026-09-18, LATER THE SAME DAY, MANIT'S CALL: HE IS APPLYING TO THE
BENCHMARKING PROJECT ONLY.** Not to all three. Three applications into one institute read
as spraying, and benchmarking is both the one he actually wants and the one his evidence
fits best. **Only `Manit Khera Cover Letter - Benchmarking Agent Workflows.docx` is live.**
The other two built letters were deleted from `Applications/` so the wrong file cannot be
attached; their text is kept in full in the build script and `python
Scripts/build_a2i2_cover_letters.py --all` regenerates them. A plain run builds only the
live one. Do not rebuild all three into the application folder.

🔴 **REVERSED 2026-09-24, MANIT'S CALL: he has sent the Benchmarking application and now
wants letters for the other two (Overseer datasets, Agent routing) as well.** He also says he
has added referee details to the resume himself; the Slavnenko spelling and phone regrouping
were not explicitly re-confirmed in that message. The duplicate PDFs he left in the repo root
were deleted, and identical copies stay in `Job_Ads/`.
Built 2026-09-24: `Scripts/build_a2i2_letters_from_template.py` fills the reviewed drafts
`Draft - Overseer Datasets.md` and `Draft - AI Agent Routing.md` into a copy of
`Templates/Cover-Letter-Template.docx` IN PLACE, keeping its layout (right-aligned sender,
Calibri, same as the sent Benchmarking letter), at Manit's explicit instruction. 1 page each,
Word COM verified. **The .md drafts are the source; edit them and re-run.** Manit reviews
content in .md first and does not want .docx built until he asks.
Style is inquisitive, per his sent Benchmarking letter (`Sent - Benchmarking Agent Workflows.md`),
built from his answers in `Interview Answers - Overseer and Routing.md`. The old
`build_a2i2_cover_letters.py` texts for these two projects are superseded.

⚠️ **Nobody knows who reads these.** Manit asked directly. The three briefs carry **no
submission instructions, no contact address and no closing date**, so the selection process
is genuinely unrecorded. Do not assert anything about it. The only certainty is that
Barnett is named on two of the three.

**THREE LETTERS WERE DRAFTED, and the reasoning is kept because it still applies if he ever
applies to more than one.** Barnett reads
two of the three, so a single generic letter has a real chance of being read twice by the
same person, and a letter that could have gone to any of the three says nothing about which
one Manit wants. The three share a spine (P1 application and availability, P2 why research,
P6 close) and diverge completely in P3 to P5.

**The hook per letter, and why:**

| Letter | Lead hook | Second hook | Gap named |
| --- | --- | --- | --- |
| Benchmarking | Seeded defects as **benchmark-task design**. Their objective 2 is choosing the benchmark tasks; he has already solved the same problem choosing defects. | Run logs: "a log is not yet evidence" (`JobHistory`/`WorkflowHistory`, replay before commit) against their expected outcome of run logs for every workflow. | Agent configuration, and no controlled experiment with statistics |
| Datasets | ParkSense **data-viability research**, story 13. Their objective 1 is curating messy real data with checkable ground truth. | Defect design plus replay-before-commit, both answering "deterministic, checkable success criteria over subjective judgement". | No manufacturing data, no eval harness or model benchmarking |
| Routing | The **rain-sensor cross-check**, story 07. Conditionally reliable signal, act only when an independent source agrees. Plain-English cousin of their uncertainty-aware thesis. | Defect calibration as ambiguity calibration, for their objective 3 (a task set graded clear to ambiguous). | Conformal prediction and statistics, named hardest here |

**RESUME ANGLE IS NEW AND DELIBERATE.** The Robot Controller entry is cut to the **evidence**
angle: execution history, reconstructing state from the record rather than the robot's
report, replay through simulation before commit. That is a third angle on the same code,
after the DDD/robotics angle used for CSIRO and the observability angle used for Microsoft.
All three are true of the same repo.

**Other deliberate choices:**

- **Python leads the languages line**, as with CSIRO. All three briefs run on Python.
- **The seeded-defects bullet leads Extra-Curricular Activities**, out of reverse-chronological
  order, ahead of the current DDSC role. It is the closest thing Manit owns to their method.
  Note this is the opposite of the 2026-08-10 decision that refused to promote it into
  PROJECTS: it stays one bullet in its real section, it just goes first.
- **The brownout diagnosis is promoted out of interview-only material** into a resume bullet
  (`bootId`/`resetCause` telemetry rather than a multimeter). CLAUDE.md always said it could
  "buy back a line if a version needs one"; this version needs it, because debugging from the
  record is the thesis all three projects run on. Wording taken from `Stories/09`, verified.
- **The persistence-layers bullet is cut**, same as CSIRO, and cutting it is what makes the
  page break fall cleanly at ParkSense.
- **Referees are "Available on request."** See the open item below.

**GUARDS, all confirmed 2026-09-18:**

- 🟢 **Agent tooling, confirmed by Manit: he uses Claude Code normally and has NOT written
  skills, hooks or worktree setups.** Ad 1 lists those as skills the internship *develops*,
  so they are not a requirement. The resume says "AI coding assistants (Claude, Claude Code)
  in daily development" and nothing more, and the benchmarking letter **names it as a gap**
  rather than hiding it, because it is the thing that reader is most likely to probe.
  ❌ Do not upgrade this to match their wording in a later edit.
- ❌ No statistics, experimental-controls or conformal-prediction claim anywhere.
- ❌ No ML or modelling claim on ParkSense. Viability research and backend foundations only,
  per the closed 2026-08-05 decision and the team lead's public write-up.
- ❌ No research experience or publications.
- ❌ **The IB Psychology Extended Essay grade is not printed.** `Stories/03` flags the A as
  needing verification against the transcript. The essay is used in every letter's P2, the
  grade is not. Resolve it if it is ever to be printed.
- ❌ No "ran" or "delivered" the workshop. Defect design was solo; someone else delivered.
- The institute is written **"Deakin Applied Artificial Intelligence Initiative"**, exactly as
  the briefs write it. They say Initiative, not Institute, and never use the abbreviation.

**❓ OPEN, needed before sending:**

1. **Availability is a commitment, not a verified fact.** Every letter states two days per week
   on campus at Burwood for ten weeks. Confirm against his actual timetable for the trimester
   these run in, and confirm which trimester that is. The briefs do not name one.
2. **How to apply, and the deadline.** The three PDFs are project descriptions only. They carry
   no closing date, no submission instructions and no document list. Nothing in the repo
   records them.
3. **Referees.** Slavnenko is a Deakin unit chair and would be a strong in-house referee for a
   Deakin research internship, but the surname spelling and the regrouped phone number are
   still unverified (see the Referees section above), so the resume says "Available on
   request." **Flip it to full details the moment both are confirmed.**
4. **Unpaid, and the visa.** A subclass 500 holder doing a 160-hour unpaid placement is
   normally fine, but it is not verified here and is worth checking alongside the same open
   question recorded for Clipchamp.
5. Whether applying to all three from one institute is preferred or discouraged. Not stated
   anywhere in the briefs.

## Andromeda Robotics Engineering Summer Intern - built 2026-10-13

Ad saved at `Job_Ads/Andromeda.md`. Their first intern program, up to 6 students, paid,
late October 2026 to end of February 2027, **onsite 5 days per week in Southbank**. Closes
as soon as the positions fill, so apply early. Stream: **Software Engineering (Software,
Firmware and Autonomy)**. Andromeda builds Abi, a companion robot for aged care and
healthcare.

🔴 **Manit rejected the first build the same day** (2 pages, DeakinTALENT Template 3, content
from the older sections of this file). His instruction: **base it on the current master,
`Current/Manit_Khera_Resume_Rewrite.md` (v7), and keep it to one page.** For technical
applications, tailor from that .md and build with the master builder, not Template 3.

- Content: `Applications/Andromeda-Engineering-Summer-Intern/Manit Khera Resume.md`, a
  tailored copy of the master .md. **Edit that file, then re-run the script.**
- `Scripts/build_andromeda_resume.py` calls `build_master_resume_rewrite.py` with that .md
  -> `Manit Khera Resume.docx` / `.pdf` in the same folder.
- **1 page, 617 words, 8 links, 2.3pt spare at the foot**, verified via Word COM. Any added
  line breaks the page.

**Changes against the master, nothing else touched:**

- Profile re-pointed from backend throughput to software that drives real hardware.
- Project order: Robot Controller API, Smart Clothesline Robot, Scaling a Robot Dispatch
  API, DEV@Deakin. The two physical robots lead.
- Skills: C++ leads Languages, and a new **Embedded & Robotics** line.
- Clothesline gains a firmware bullet (3-bit state machine, L298N, the brownout diagnosis),
  all from the verified notes above. DEV@Deakin is cut to one bullet to pay for it.

**Three referees on this resume: Slavnenko, Clement Asogwa, Roohi Bhatia.** Asogwa was added
2026-10-13 and Bhatia, first dropped to hold the page, was put back as third the same day; the
script tightens `section_before` and `entry_before` to pay for the extra line. Details copied from the referees Manit typed into the A2I2 resume himself:
Dr Clement Asogwa, Associate Teaching Fellow, Software Engineering, School of Information
Technology, Deakin University, clement.asogwa@deakin.edu.au, +61 3 9918 9029 (he wrote
"+61 3 991 89029"; regrouped, same digits). The override sits in the build script, the master
is untouched.
⚠️ That same A2I2 resume lists Slavnenko as "Associate Teaching Fellow" at
`maksym.slavnenko@deakin.edu.au`, while the master and the Referees section above say "Unit
Chair" at `m.slavnenko@deakin.edu.au`. ✅ **Email resolved 2026-10-13, Manit's call: use
`m.slavnenko@deakin.edu.au`.** The title was not addressed; this resume keeps the master's
"Unit Chair, Backend Development".

**Portfolio for the form's work-sample upload, built 2026-10-13:** `Manit Khera Portfolio.pdf`
in the same folder, 2 pages, 12 links. Source is `Manit Khera Portfolio.html` (hand-written,
images in `portfolio-assets/`, both frames from his own demo videos). Rebuild by printing the
HTML to PDF with headless Edge (`msedge --headless --no-pdf-header-footer --print-to-pdf=...`).
Three case studies: Smart Clothesline Robot, Robot Controller API, Scaling the Robot Dispatch
API. DEV@Deakin is left out as not relevant to robotics. Dispatch numbers were read from the
`SIT315-RobotDispatch` README on 2026-10-13 (176.7 / 607.7 / 1,069.0 jobs/s at 400 robots;
0.0 vs 1,007.8 at 5,000; claim p50 766.5 ms to 59.5 ms; limiter 64 running, 32 queued; NBomber
on Azure; 72 grid + 8 stress runs; 54 tests).
⚠️ **The public `RobotControllerApi` README is stale and contradicts the resume and portfolio:**
it says grid movement has "not been validated end to end against the physical robot", "no
automated test suite", five permission tiers, and calls the robots autonomous. Flagged to
Manit 2026-10-13. Either update that README or link the newer `SIT315-RobotDispatch` repo.
✅ **Rewrite drafted 2026-10-14:** `Applications/Andromeda-Engineering-Summer-Intern/RobotControllerApi README.md`,
checked against the `deploying` branch code (4 tiers in `DomainConstants.cs`, inverse on claim,
`report-offline-rollback`, `StaleWorkExpiryService`, history GETs behind `HumanUser`, tests,
Jenkinsfile, monitoring). Not yet pushed; Manit pushes it himself. `main` was last committed
24 July, so the work lives on `deploying`.
Each project carries a "Follow the build" link trail, added at Manit's instruction with links
he supplied: clothesline (first demo on YouTube, second demo on Panopto, Hackster.io write-up,
GitHub); Robot Controller (LinkedIn post of the first in-class demo with the unit chair, Open
Day demo `youtu.be/unDSeDkGBI0`, GitHub `main`, `openday` and `deploying` branches, all three
verified to exist); Dispatch (`old` branch as the baseline, the repo, Panopto demo, report PDF).
15 links in total.
**Rewritten the same day at Manit's request to be less technical, more fun and matched to
Andromeda's five values** (Empathy, Play, Never Settle, Tenacity, Unity). It now has an About
Me (he cannot leave a finished project alone; one robot repurposed across three units), a
"Meet the robot" card, a values strip with one real piece of evidence per value, three
"chapters", handwritten-style margin notes, and "Three things this robot taught me". Every
joke rests on a recorded fact. The unit chair's warning comes from `Stories/01`.
❓ Two demo videos are on Deakin Panopto and may need a Deakin login to open.

🟢 **NEW STORY, told by Manit 2026-10-13, for the "top 3 strengths" answer and future letters:**
his unit chair Maksym Slavnenko would tell him, cockily and not discouragingly, "nah, you can't
do this", knowing Manit does his best work trying to prove him wrong, and kept pushing him
toward more ambitious goals that way (Manit's word: "ragebaiting"). A fun love-hate
relationship. They discussed many ideas; Maksym treated them as creative imagination and the
two shared a childlike "what if..." experimentation mindset, which Manit credits for how far he
got in that unit. This extends `Stories/01`, which only records "supportive but honest".
🔴 **CORRECTION from Manit 2026-10-13: he NEVER had Wi-Fi dropping issues.** The Wi-Fi-loss
recovery (undo stack, 7-second watchdog, replay before commit) was designed deliberately and
then tested on hardware; it was not a response to a problem he suffered. The real-world problem
he lived through was **voltage sag**. Claude had written "the Wi-Fi dropped" and "real Wi-Fi
kept dropping mid-task" as events in the portfolio and an email draft; both were wrong and are
fixed. Never narrate Wi-Fi drops as something that happened to him. Describe the feature as a
"what if" he built for. Also: his demo videos are demos, not something "for a laugh".
🟢 **Battery story, told by Manit 2026-10-13:** because of the unstable voltage, and before the
converter was sorted, the robot only behaved on fresh batteries and started acting up once they
dropped below about 90 percent charge. He kept buying new ones, "probably 100 dollars" worth,
and now has a pile of roughly 90 percent full batteries lying around. Both figures are his
estimates. He prefers the term "rage bait" for the Maksym story.
Manit's feedback on the first strengths draft: make it more fun, drop "making myself
unnecessary", and stop repeating the same evidence (100/100, 5,000 robots) everywhere.

❌ No ROS, no PID. The stroke-support "interest in robots built for people" sentence from the
rejected build is gone and should not come back unless Manit says it himself.

❓ **Open, for the form:** the work sample upload, the top 3 strengths answer, the transcript,
and the sponsorship question (same visa wording question as Clipchamp and CSIRO; the program
also starts in late October, before the Trimester 2 break).

## Rosterfy Expression of Interest - built 2026-10-14

Ad saved at `Job_Ads/Rosterfy-Expression-of-Interest.md`. A talent-community EOI, not a
named opening: no closing date, no document list. Rosterfy is a Melbourne volunteer
management SaaS for not-for-profits, government and major events. Hybrid.

- Content: `Applications/Rosterfy-Expression-of-Interest/Manit Khera Resume.md`, a tailored
  copy of the v7 master. **Edit that file, then re-run the script.**
- `Scripts/build_rosterfy_resume.py` -> `Manit Khera Resume.docx` / `.pdf` in the same folder.
- **1 page, 593 words, 8 links, 2.3pt spare at the foot**, verified via Word COM. Any added
  line breaks the page.
- **Submitted 2026-10-14**, with the cover letter and a "Why do you want to work for
  Rosterfy?" form answer. He answered Yes to the sponsorship question. Tracker row
  `rosterfy-eoi`, status awaiting.

**Changes against the master, nothing else touched:**

- Profile names the not-for-profit IT support volunteering and wanting to build software for
  volunteer-run organisations. The rest of the profile is the master's.
- Project order: Scaling a Robot Dispatch API, DEV@Deakin, Robot Controller API, Smart
  Clothesline Robot. The web product moves up; the hardware goes last.
- Boroondara Stroke Support Group gains the redevelopment-plan and Site Health audit bullet
  (verified above). The clothesline entry is merged to one bullet to pay for it.
- Referees are the master's two (Slavnenko, Bhatia).

❌ Nothing claimed on machine learning, data pipelines, LLM integrations or their stack. The
ad lists those as things an intern would be exposed to, not requirements.

**Cover letter, built the same day.** Source is `Manit Khera Cover Letter.md` in the same
folder; `Scripts/build_rosterfy_cover_letter.py` fills it into
`Templates/Cover-Letter-Template.docx` in place (the A2I2 method, template layout kept).
**1 page, 586 words**, Word COM verified. Edit the .md and re-run.

- Structure follows the template's blocks in `Guides/Cover-Letter-Guide.md` section 4a.
- Stories used: 01 (the integration nobody asked for) carries body one; 15 (BSSG calendar
  and volunteer training, Market Day 100+ once) carries body two; the move in 10 names the
  machine learning and data pipeline gap.
- Organisation paragraph ties their volunteer-to-shift matching to the dispatch project's
  atomic job claims. Figures are from the ad (160 million hours, 77 countries, seven Super
  Bowls, Lifeline, Oxfam).
- Addressed to "Hiring Manager, Engineering and Technology Team", since no contact is named.
  Office address from rosterfy.com/contact-us on 2026-10-14: L6/395 Collins St, Melbourne
  VIC 3000.

❓ **Open:** where he found the listing. The letter says "in response to your Expression of
Interest listing" and names no board. The guide asks for the source, so add it once he says.

## ReSource Imaging Station Engineering Intern - built 2026-10-15

Ad saved at `Job_Ads/ReSource-Imaging-Station-Intern.md`. ReSource Pty Ltd is an IT asset
disposition (ITAD) business in Keilor East. Two interns build a multi-camera imaging and
identification station (Sony A7 III proof of concept, vision pipeline, OCR and barcodes, posting
to their RazorERP system). 12 weeks full-time, November to February, mainly on site. Apply by
email to careers@re-source.au with a CV and a project example. Founder **Troy Rowe** (Deakin
alum) accepted Manit's LinkedIn connection request 2026-10-15, before he applied. He did not reach out first.

- `Applications/ReSource-Imaging-Station-Intern/Manit Khera Resume.md` -> `Scripts/build_resource_resume.py`.
  **1 page, 593 words, 8 links, 37.8pt spare**, Word COM verified.
- `Manit Khera Portfolio.html` / `.pdf`: the Andromeda portfolio retargeted. The values strip
  is replaced by "What you asked to see" (built, Python and APIs, testing, when it broke,
  handover), and the footer names the CV gap. 2 pages, clean break at Chapter 2.
- `Application Email.md`: the email body answering their four questions.

**Confirmed by Manit 2026-10-15:** software is his stronger area; solo application; available
12 weeks full-time on site; **no computer vision, OCR or barcode experience at all.**
❌ Do not claim OpenCV, OCR, barcode or image processing anywhere. The gap is named in the
email and the portfolio, paired with the validate-before-recording logic that does transfer.
⚠️ The ad asks for final-year or Masters students; he is in third (penultimate) year, finishing 2028. The email
says so plainly. Same Nov to Feb window as Andromeda.

Plan: send the application first, then a short LinkedIn note to Troy saying he has applied.

## Conventions

- Manit writes numeric dates in **US M/D/YYYY** order despite being Melbourne-based.
  Always convert to unambiguous written form ("November 2025") and state the reading
  back to him.
- Australian/British spelling throughout: organisation, optimise, programs.
- **No em dashes** (stated 2026-08-08). Applies to everything that ships: resume bullets,
  cover letters, and chat replies. Use commas, semicolons, colons or parentheses instead.
  This file's older notes still contain them; leave those, just don't add more.
- In the .docx, unresolved gaps are red (`C00000`) runs containing `[TBC: ...]`.
  When a gap is filled, strip the red colour from that run or the resume ships with
  red text in it.

## File state — 2026-07-24 (rebuilt, verified)

✅ **`Manit_Khera_Resume.docx` was rebuilt from scratch and verified.**

- Generated with **python-docx 1.2.0** (Python 3.13) — not by hand-editing or rezipping XML.
- Verified: 17 zip entries, **0 with backslashes**; opens in Word via COM without error.
- **3 pages, 1,163 words, 6 working hyperlinks** (verified via Word COM). Three pages is
  intentional — this is the detailed master for a professional to cut. See length policy.
- The previous corrupt file (backslash zip entries, confirmed broken) is preserved at
  `Archive\Backup\Manit_Khera_Resume_BROKEN_20260724.docx` (moved there 2026-08-13).
  Safe to delete once the new file has been eyeballed in Word.

**To regenerate:** the build script is `build_resume.py`. It was written to the session
scratchpad, which will not survive — **copy it into this folder if the resume will need
rebuilding later.** It is a single self-contained script; editing content means editing
the bullet lists inside it, then re-running `python build_resume.py`.

**Lesson retained:** do not unzip/edit/rezip a .docx on Windows PowerShell 5.1 —
`ZipFile::CreateFromDirectory` writes backslash entry names and produces a file Word may
refuse to open. Generate the document instead.

## Tekt Industries Mechatronics Engineering Intern - built 2026-10-16

Product design and manufacturing studio, Level 2, 351 Elizabeth St, Melbourne. Paid, 6 months,
2 to 3 days a week, Concept Development team. Wants mechatronics/electrical/mechanical students in
penultimate or final year, basic CAD, microcontroller exposure. Apply by form: CV + cover note of
at most 2,000 characters describing something you've built.

🟢 **NEW FACT, Manit 2026-10-16: CAD is Fusion 360.** Modelled a multi-part pot assembly in a Deakin
unit (body, lid, lid grip, handles, spout, support legs) with exploded, sectional and iso views and
a technical drawing; learned loft among other features. **Nothing 3D printed.** Do not claim printing,
laser cutting or machining. Unit name not recorded.

- `Applications/Tekt-Mechatronics-Engineering-Intern/Manit Khera Resume.md` -> `Scripts/build_tekt_resume.py`.
  1 page, 609 words, 15.5pt spare. NxtGen copy with a prototyping profile, "Embedded & Prototyping"
  skills line with Fusion 360 CAD, clothesline first, dispatch cut to two bullets.
- `Cover Note.txt`, 1,627 characters: the clothesline build, the voltage sag, Fusion 360, and the
  software-not-mechatronics degree named plainly.

## Inspire Robotics Junior Facilitator - built 2026-10-16

Casual, Ferntree Gully (4/756 Burwood Hwy), delivering engineering projects in schools; at least
one weekday per term at one school; training over the Term 1 break, schools from Term 2. Wants a
STEM degree, communication, hands-on technical skills; licence and car desirable. Apply by email
to info@inspirerobotics.com.au (the site's form gives no document list).

🟢 **Confirmed by Manit 2026-10-16: NO driver's licence** (public transport only), and weekday
availability is set each term around his timetable. WWCC (Employee) held.

- `Scripts/build_inspire_resume.py`, 1 page, 601 words. Teaching-led profile, SKILLS (not
  TECHNICAL SKILLS; the master builder accepts both now), Open Day ambassador entry, referees
  Bhatia then Slavnenko.
- Portfolio: values strip mapped to facilitator needs; "Three classroom lessons hiding inside this
  robot" replaces the Fusion block. 2 pages, break at Chapter 2.
- `Application Email.txt`.
