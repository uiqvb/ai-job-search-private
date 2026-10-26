"""Build job_scraper/scrape_history.md: every scraped job, grouped by the day it was found.

    python tools/scrape_history.py

Reads job_scraper/seen_jobs.json (the scraper's record of every job it has seen) and
rewrites the markdown file from it, newest day first. Run automatically after each
scheduled scrape (automation/run_job.py), so the history grows with every run.
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SEEN = REPO / "job_scraper" / "seen_jobs.json"
OUT = REPO / "job_scraper" / "scrape_history.md"
FIT_ORDER = {"high": 0, "medium": 1, "low": 2}


def cell(text):
    return str(text or "").replace("|", "/").replace("\n", " ").strip() or "-"


def table(jobs):
    rows = ["| Fit | Title | Company | Posted | Deadline | Score | Status | Link |",
            "|-----|-------|---------|--------|----------|-------|--------|------|"]
    for j in jobs:
        score = j.get("rank_score")
        rows.append("| " + " | ".join([
            cell(j.get("fit", "?").capitalize()), cell(j.get("title")), cell(j.get("company")),
            cell(j.get("posted_date")), cell(j.get("deadline")),
            cell(score if score is not None else ""), cell(j.get("status")),
            f"[Open]({j['url']})" if j.get("url") else "-",
        ]) + " |")
    return "\n".join(rows)


def build():
    seen = json.loads(SEEN.read_text(encoding="utf-8")).get("seen", {})
    by_day = defaultdict(list)
    for job in seen.values():
        by_day[job.get("first_seen") or "unknown"].append(job)

    out = ["# Scrape history", "",
           f"Every job the scraper has found ({len(seen)} total), newest day first. "
           "Rebuilt from `seen_jobs.json` after each scrape; edit that file, not this one.", ""]
    for day in sorted(by_day, reverse=True):
        jobs = sorted(by_day[day], key=lambda j: (FIT_ORDER.get(j.get("fit"), 3), -(j.get("rank_score") or 0)))
        good = [j for j in jobs if j.get("fit") in ("high", "medium")]
        low = [j for j in jobs if j not in good]
        counts = {f: sum(j.get("fit") == f for j in jobs) for f in FIT_ORDER}
        out += [f"## {day}", "",
                f"{len(jobs)} new: {counts['high']} high, {counts['medium']} medium, {counts['low']} low.", ""]
        if good:
            out += [table(good), ""]
        if low:
            out += [f"<details><summary>{len(low)} low-fit jobs</summary>", "", table(low), "", "</details>", ""]
    OUT.write_text("\n".join(out), encoding="utf-8")
    return len(seen), len(by_day)


if __name__ == "__main__":
    if not SEEN.exists():
        sys.exit(f"not found: {SEEN}")
    total, days = build()
    print(f"scrape_history.md: {total} jobs over {days} day(s)")
