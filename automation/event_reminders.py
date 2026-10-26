"""Morning reminder for today's events. Plain Python, no Claude usage.

Reads the "Upcoming" table in documents/notes/events.md (maintained by /gmail-sync Step 8a)
and sends one notification per event dated today, delivered at the morning slot
(config "deliver_at", default 07:30) when run before it. Rows start with "| YYYY-MM-DD".

    python automation/event_reminders.py [--date YYYY-MM-DD]   # --date = pretend today is this
"""

import datetime as dt
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from notify import morning_delivery, send  # noqa: E402
from power import night_run  # noqa: E402
from daily import record, should_run  # noqa: E402

EVENTS = HERE.parent / "documents" / "notes" / "events.md"


def upcoming_rows(text):
    m = re.search(r"^## Upcoming.*?$(.*?)(?=^## )", text, flags=re.M | re.S)
    if not m:
        return []
    rows = []
    for line in m.group(1).splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 6 and re.match(r"\d{4}-\d{2}-\d{2}", cells[0]):
            rows.append(dict(date=cells[0][:10], time=cells[1], event=cells[2], group=cells[3],
                             venue=cells[4], status=re.sub(r"\*|\(.*?\)", "", cells[5]).strip()))
    return rows


def main():
    today = dt.date.today()
    if "--date" in sys.argv:
        today = dt.date.fromisoformat(sys.argv[sys.argv.index("--date") + 1])
    day = today.isoformat()
    if not EVENTS.exists():
        print("no events.md"); return
    rows = [r for r in upcoming_rows(EVENTS.read_text(encoding="utf-8")) if r["date"] == day]
    for r in rows:
        if r["status"].lower().startswith("cancel"):
            continue
        msg = f"{r['time']} {r['event']} @ {r['venue']}"
        if "wait" in r["status"].lower():
            msg += " (you're WAITLISTED, check Meetup for a spot)"
        send("Today: " + r["event"][:60], msg[:400], tags="calendar", at=morning_delivery())
        print("reminded:", r["event"])
    if not rows:
        print("no events today", day)


if __name__ == "__main__":
    manual = "--date" in sys.argv or "--force" in sys.argv
    # Task also fires at sign-in/unlock: remind once a day only
    if not manual and not should_run("event_reminders"):
        print("event_reminders: already done today, skipping")
        sys.exit(0)
    # --date is a manual test: never hibernate then
    with night_run(hibernate="--date" not in sys.argv):
        main()
    if not manual:
        record("event_reminders", True)
