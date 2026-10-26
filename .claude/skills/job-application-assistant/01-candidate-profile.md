---
framework_version: 1.1.1
---

# Candidate Profile

<!-- Populated by /setup on 2026-10-20 from ~/Documents/Resume (CLAUDE.md master notes, v7 master
resume, Stories/, tracker) and ~/Documents/Projects. The Resume folder's CLAUDE.md is the
fact-checked source of truth: it records a code audit and many ruled-out claims. When this file
and that one disagree, that one wins; update this file to match. -->

## Identity
- **Name:** Manit Khera
- **Location:** Blackburn South, VIC 3130, Australia
- **Street address (cover letter sender block only, never on the resume):** 12 Jenner Street, Blackburn South, VIC 3130 (as on his sent DeakinTALENT-template letters)
- **Phone:** 0412 761 206
- **Email:** manitkhera26@gmail.com
- **LinkedIn:** https://www.linkedin.com/in/manit-khera-603957252
- **GitHub:** https://github.com/uiqvb
- **Status:** Full-time student, Bachelor of Software Engineering (Honours), Deakin University, Burwood. Third-year (penultimate-year) student, of four years. Never write second-year. Seeking internships, vacation programs and part-time/casual technical roles.
- **Work rights:** International student, Australian student visa (subclass 500). Assumed standard conditions: capped hours per fortnight during study periods, unrestricted during scheduled course breaks (Nov to Feb). Verify against the visa grant before stating it on a form.
- **Constraints:** **No driver's licence, public transport only.** Melbourne onsite or hybrid roles must be reachable by train/tram/bus from Blackburn South. Remote roles anywhere are fine. Holds a **Working with Children Check (Employee)**.

### Languages

| Language | Level | Notes |
|----------|-------|-------|
| English | Fluent (professional, all four skills) | Studies and works in English; IELTS on file |
| Hindi | Spoken: good (speaking and listening). Written: weak (reading and writing) | Do not claim written Hindi |

**CV language:** English, Australian/UK spelling (organisation, optimise, programs).

## Education

| Degree | Period | Institution | Key Topics |
|--------|--------|-------------|------------|
| Bachelor of Software Engineering (Honours) | March 2025 to 2028 (expected, no month) | Deakin University, Burwood VIC | WAM **81.33** (as at Oct 2026; new results due ~30 Oct 2026, expected to rise; update then). Unit marks: **100** Data Structures & Algorithms, **100** Backend Development (SIT331), **93** Embedded Systems (SIT210), **92** Object-Oriented Programming. Backend unit project selected for showcase at Deakin Open Day. |

- First year: Distinction average with one Credit (only relevant to story 02, never printed).
- GPA on a 7-point scale has not been computed; needs the transcript.

## Professional Experience

### Student Ambassador (paid, casual) - Deakin Future Students (Aug 2026)
Burwood VIC
- Represented Deakin at Open Day, August 2026, speaking with prospective students and families. Worked the shift (confirmed 2026-09-17).
- Showcased his robot project (Robot Controller API) to prospective students and parents, showing what computing degree outcomes look like and encouraging them to choose Deakin (Manit, 2026-10-21). No conversion numbers; do not invent any.

### IT Support Volunteer - Boroondara Stroke Support Group (Jul 2025 - Present)
VIC (community not-for-profit)
- Maintained the WordPress site (OceanWP, Elementor) publishing the group's programs, calendars and donation information, as part of a small volunteer team.
- Ran the monthly activity-calendar publication cycle for 12+ months: upload, supersede the old version, update links, verify it opens.
- Designed and built new Elementor pages for a proposed site refresh (later discarded).
- Diagnosed and rolled back a change that broke a live page, without external developer support.
- Authored a redevelopment plan backed by a WordPress Site Health audit; identified the hosting tier's PHP memory limit as the blocker (the organisation did not act on it).
- Trained new volunteers to publish the monthly activity sheet themselves.
- ❌ Never claim: rebuilt the site, applied updates, took backups, performed optimisation, "IT infrastructure", "sole point of contact", visitor metrics.

### Customer Service Assistant - 7-Eleven (Jul 2025 - Oct 2025)
Noble Park VIC
- Front-line service in a high-volume store; resolved transactions, enquiries and escalated complaints without manager involvement.
- Opened and closed unsupervised: float set-up, safe drops, EFTPOS and cash reconciliation, variance investigation.
- Operated POS and fuel console; digital, fuel-app and loyalty payments.
- Trained new starters on POS, food safety and shift routines; age-restricted sales compliance.
- ⚠️ Not a referee (parted on bad terms). No commendation claims. Customers-per-shift figure unknown, do not invent.

## Leadership & Involvement

### LinkedIn Manager - Deakin Data Science Club (Jan 2026 - Present)
- Owns the club's LinkedIn strategy end to end (content, design, scheduling, analytics); **1,000+ impressions per post**.
- Event graphics; alumni outreach and re-engagement; hosted and anchored networking sessions; sponsor co-branded content; club inbox.
- Informally advises fellow students on LinkedIn profiles and resumes (no count, no program name).

### Committee Member - Deakin Software Engineering Club (Jul 2025 - Apr 2026)
- On the dev team that built the React to-do app used for a ~**30-attendee** debugging workshop; **solely designed the seeded defects**. Did NOT deliver the workshop. Defect count unconfirmed (do not print "15").
- Floated the workshop as a helper; fronted Market Day (**100+ sign-ups**; print this figure once, under DSEC, not also under DDSC); weekly committee planning (proposed an open-source program and a hackathon; adoption unconfirmed, so "proposed", never "launched"); event photography. DSEC has 200+ members.

## Independent Projects

All university projects are solo unless marked. Links are in the master resume and portfolio.

- **Robot Controller API** (SIT331 Backend Development, T1 2026; 100/100, Open Day showcase): hardware-neutral REST control platform, .NET 8 / ASP.NET Core / C# / PostgreSQL. 18 controllers, ~120 endpoints, 16 bounded contexts; the robot holds no plan of its own (not "autonomous"). Compensating-transaction rollback (never "Saga"): each claimed command carries its inverse, robot keeps a LIFO undo stack, 7-second watchdog, server replays reported actions through simulation before commit; hardware-verified, robot returned to its exact predicted grid position. Wi-Fi-loss recovery was **designed as a "what if"**; he never actually suffered Wi-Fi drops. HMAC-SHA256 device credentials + HTTP Basic for humans, 4-tier per-device permissions, exposed through Swagger/OpenAPI (not "documented"). Three interchangeable persistence layers (ADO.NET/Npgsql, EF Core, FastMember generic repository). Seven-stage Jenkins CI/CD with deployment rollback and security scanning; container vulnerability findings cut 93% (310 to 22), critical 4 to 0. Docker, Prometheus, Grafana, Trivy. Demo https://youtu.be/ZW7Ps9AMmc0, code https://github.com/uiqvb/RobotControllerApi (current work is on the `deploying` branch; public README is stale).
- **Smart Clothesline Robot** (SIT210 Embedded Systems, T1 2026; awarded 93): two-tier robot. Arduino Nano (C/C++) with 3x TCRT5000 line sensors, 2x BH1750 light sensors over I2C, analog rain sensor, L298N motor driver; line following is a 3-bit sensor-pattern state machine (**bang-bang, NOT PID**). Raspberry Pi Python/Flask dashboard as a systemd service; MQTT command and JSON telemetry (5 s); Open-Meteo forecast fallback for an unreliable rain sensor; wet tests and injected telemetry faults. Traced an intermittent brownout to a failing buck converter from `bootId`/`resetCause` telemetry. The real hardware problem he lived through was voltage sag. Integrated with the Robot Controller API so the backend drove the physical robot. Demo https://youtu.be/7QVj2lUGF2s, code https://github.com/uiqvb/SIT210/tree/main/Task11.1HD
- **Scaling a Robot Dispatch API** (SIT315): audited 12 dispatch bottlenecks and race conditions; async I/O, backpressure, less redundant SQL: **3.44x** single-replica throughput at 400 simulated robots; two Azure replicas with atomic PostgreSQL job claims: **6.05x** baseline; **~1,008 jobs/s at 5,000 robots** vs zero for the original; claim p50 766.5 ms to 59.5 ms; NBomber on Azure; **54 automated tests, 80 benchmark runs** (72 grid runs + 8 stress runs; grid points at 10/100/400 robots, stress at 2,000/5,000; **3 repeats per point, median reported**, 30 s measured after a 5 s warm-up; all 72 grid runs passed; verified from the repo README 2026-10-22). The 12 bottlenecks were found by an audit, not by the benchmark runs. C#, ASP.NET Core, PostgreSQL, Azure, xUnit.
- **DEV@Deakin**: full-stack developer platform, React, Node.js/Express, Firestore. JWT auth, TOTP two-factor login, hashed recovery codes, server-enforced premium content, cursor-based browsing, optimistic voting with rollback, XSS-sanitised Markdown; **24 automated tests**.
- ❌ **Not to be mentioned (Manit's call, 2026-10-20):** NetworkOS (job-search CRM, scrapped), Downloads Organizer (WPF app, abandoned), Prompt Toggles (Chrome extension, unfinished) and Access Lens (small MSA mini-hackathon win, team).
- ❌ **ParkSense / DDSC hackathon: excluded at Manit's request (2026-10-20).** Do not put it on any CV, cover letter or interview answer. If an interviewer raises it from LinkedIn: team project, he originated the idea and did the data research; the team lead built the model, endpoints and map.

## Technical Skills

### Programming & ML
- **C#** (strongest; .NET 8, ASP.NET Core, EF Core, ADO.NET/Npgsql, xUnit)
- **C++** (Arduino firmware; OOP unit)
- **Python** (Flask, Streamlit, SQLAlchemy, pytest; some pandas/XGBoost exposure via ParkSense)
- **TypeScript / JavaScript** (React, Next.js, Node.js/Express). TypeScript is newer and lighter; never lead the languages line with it.
- **SQL** (PostgreSQL, MySQL from Database Fundamentals)
- AI tooling: **Claude and Claude Code** in daily development (not GitHub Copilot). Has not written Claude Code skills, hooks or worktree setups.

### Domain Expertise
- Backend APIs, concurrency and throughput, reliability and rollback design
- Embedded systems and hardware integration (Arduino, Raspberry Pi, sensors, motor drivers, MQTT, I2C)
- DevOps and testing (Docker, Jenkins CI/CD, Azure, Trivy, Prometheus, Grafana, Postman, Swagger/OpenAPI)
- CAD: **Fusion 360** (multi-part pot assembly, loft, exploded/sectional views, technical drawing). Nothing 3D printed.

### Software & Tools
- Git/GitHub, Docker, Jenkins, Azure, Postman, Swagger/OpenAPI, Supabase, Firestore, WordPress/Elementor, Fusion 360, Remotion/ffmpeg (video editing)
- **Microsoft Office**: self-rated good (Manit, 2026-10-20). No specific apps or certifications recorded; do not claim advanced Excel (macros, VBA, pivot tables) without asking.

### Known gaps (never claim)
- ROS/ROS2, PID control, computer vision/OpenCV, OCR, barcodes, 3D printing, laser cutting, PCB design, LIDAR, formal statistics/experimental design, ML model training, Java, online video.
- Confirmed by Manit 2026-10-22 (Syncrowin application): has taken **no statistics, probability, linear algebra or machine learning units/courses**. Willing to learn and says he produces results when needed. Frame as an honest gap with a learning bridge, never as coursework.

## Publications
None.

## Awards
- Robot Controller API selected from the SIT331 cohort for showcase at **Deakin Open Day (August 2026)**: demonstrated the working robot, including the live offline rollback, to prospective students and parents. Demo https://youtu.be/unDSeDkGBI0
- 100/100 in Backend Development (2026)

## References
- Maksym Slavnenko, Unit Chair, SIT331 Backend Development, Deakin University (m.slavnenko@deakin.edu.au, +61 3 9244 5749). ⚠️ Title is "Associate Teaching Fellow" on one resume; confirm.
- Dr Clement Asogwa, Associate Teaching Fellow, Software Engineering, School of IT, Deakin University (clement.asogwa@deakin.edu.au, +61 3 9918 9029)
- Roohi Bhatia, Hub Administrator, Boroondara Stroke Support Group (info@bssg.org.au, +61 478 092 028). Lead with her for people-facing roles.

Default on CVs: "Available upon request." unless the employer asks for referees.
