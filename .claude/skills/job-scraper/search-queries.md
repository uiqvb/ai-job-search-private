# Search Queries for Job Scraper

<!-- SETUP: Customize these queries based on your skills, target roles, and location -->

## Installed portal CLIs (primary for `/scrape`)

`/scrape` discovers every portal skill under `.agents/skills/*/SKILL.md` and runs its CLI first. Shipped country-agnostic CLIs include `linkedin-search` and `freehire-search`; Danish demos and any skill you add with `/add-portal` are included the same way. You do **not** need a matching `site:` line below for those CLIs to run.

The `site:` query templates in this file are the **WebSearch fallback** — for portals without a CLI, company career pages, or when a CLI fails.

**Language scope:** write every query category in every language listed in your CLAUDE.md Languages table (typically 1-2, sometimes more). A posting requiring a language you have *not* declared, as a job condition, is excluded before scoring; a posting requiring a *higher level* than you declared in a language you *do* work in is flagged for your own judgment, not excluded — see `04-job-evaluation.md`'s Language Gate, the single source of truth for this rule. Translate each category's keywords rather than machine-translating word-for-word (e.g. "Frontend Developer" -> "Desarrollador Frontend", not a literal word-for-word translation) if you work in more than one language.

## Search Sites

Market: **Melbourne, Australia** (plus remote roles anywhere). Installed CLIs `linkedin-search` and `freehire-search` run first; the Danish portals stay disabled.

Primary:
- **seek.com.au** - Australia's largest board (no CLI yet; add one with `/add-portal`, until then use the `site:` queries below)
- **linkedin.com/jobs** - also covered by the `linkedin-search` CLI (location: Melbourne, Victoria, Australia)
- **gradconnection.com** and **prosple.com** - Australian intern/vacation program boards
- **Deakin Jobs and Internships Board (DeakinTALENT)** - student-only listings, check manually

Secondary (company career pages via Google):
- Melbourne robotics/hardware/AI startups: Andromeda Robotics, Tekt Industries, NxtGen Industries, ReSource, Aurova, Element Robotics, August Robotics, black.ai, AOS Group, Exergenics, Apollo Medical Imaging, Rosterfy, Clipchamp
- Kids' STEM / coding education (bridging roles): Code Camp, Rocket Academy, Bricks 4 Kidz Boroondara, Innovate Technology & Robotics Academy, Skill Samurai, Play AI, Kids2Coding, STEM Birds, ThinkerLab, Inspire Robotics

## Query Categories

Queries are in English only (Hindi is spoken-only and not a working language for postings). Most results should be **intern / vacation / junior / casual / part-time**: add those words to queries. Skip anything requiring a graduate degree already held, citizenship/PR, a security clearance, or a driver's licence and car.

### Priority 1: Robotics, embedded and firmware software (internships)

Software that drives real hardware: firmware, sensor integration, robot control backends.

```
site:seek.com.au "robotics" intern Melbourne
site:seek.com.au "embedded software" intern OR graduate Melbourne
site:seek.com.au "firmware" intern Melbourne
site:seek.com.au "mechatronics" intern Melbourne
site:linkedin.com/jobs "robotics software" intern Melbourne
site:linkedin.com/jobs "embedded" "summer intern" Australia
site:gradconnection.com robotics OR embedded internship Victoria
```

### Priority 2: Backend / software engineering internships

C#/.NET, APIs, PostgreSQL, cloud, testing.

```
site:seek.com.au "software engineering intern" Melbourne
site:seek.com.au "backend developer" intern OR junior Melbourne
site:seek.com.au ".NET" OR "C#" intern OR junior Melbourne
site:linkedin.com/jobs "software engineer intern" Melbourne
site:linkedin.com/jobs "software developer" "part-time" student Melbourne
site:prosple.com software engineering internship Melbourne
site:gradconnection.com "summer internship" software Melbourne
```

### Priority 3: AI and agent research / applied AI

```
site:linkedin.com/jobs "AI engineer" intern Melbourne OR remote Australia
site:seek.com.au "machine learning" OR "AI" intern Melbourne
site:linkedin.com/jobs "research intern" AI Australia remote
"research internship" "applied AI" Deakin OR Monash OR RMIT OR Melbourne
```

### Priority 4: Tutoring and kids' STEM facilitation (bridging roles, casual)

Eastern suburbs preferred: Glen Waverley, Mount Waverley, Box Hill, Burwood, Blackburn, Camberwell, Hawthorn, Doncaster, Chadstone.

```
site:seek.com.au "STEM" facilitator OR educator casual Melbourne
site:seek.com.au "coding" tutor OR instructor casual Melbourne
site:seek.com.au "robotics" instructor OR teacher casual Melbourne
site:linkedin.com/jobs "coding instructor" Melbourne
"PASS Leader" OR "peer mentor" Deakin careers
```

### Priority 5: Remote software roles (wider net)

```
site:linkedin.com/jobs "software engineer intern" remote Australia
site:linkedin.com/jobs "junior developer" remote "C#" OR "TypeScript"
```

## Location Filter

Home: Blackburn South VIC 3130. **No driver's licence; public transport only.**
- **Ideal:** Box Hill, Burwood, Blackburn, Glen Waverley, Mount Waverley, Camberwell, Hawthorn, Doncaster, Chadstone, Clayton, Ringwood
- **Acceptable:** Melbourne CBD, Southbank, Docklands, Richmond, Cremorne, Collingwood, any suburb on the Belgrave/Lilydale/Glen Waverley lines
- **Borderline (~75+ min by transit, check the route):** Keilor East, Tullamarine, Dandenong South, outer west and north industrial estates
- **Too far / FAIL:** anything requiring a car; onsite roles outside Melbourne (Sydney, Brisbane, regional VIC)
- **Remote:** PASS from anywhere

## Language Filter

Your working languages and levels are in CLAUDE.md's Languages table. When filtering scraped results, apply `04-job-evaluation.md`'s Language Gate: a posting requiring a language you haven't declared at all is excluded; a posting requiring a higher level than you declared in a language you do work in is not excluded, flag it clearly instead (see `job-scraper/SKILL.md`'s Step 3 "Quick Fit Assessment" for how the flag surfaces in `/scrape` output). Postings simply *written* in a language you don't work in, that don't require it on the job, are fine.

## Date Filter

Only include jobs posted within the last 14 days, or with an application deadline that has not yet passed. If a posting date cannot be determined, include it but flag as "date unknown".

## Adapting Queries

If the user specifies a focus area, select queries from the matching category and also generate 2-3 custom queries for that focus. For example:
- "/scrape [focus_area]" -> relevant category queries + custom focus-specific queries
