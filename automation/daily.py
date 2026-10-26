"""Once-a-day guard for the scheduled jobs.

Each task fires at its night time AND whenever Manit signs in or unlocks the laptop, because
wake timers don't work on this laptop and Windows' own catch-up is unreliable after hibernate.
This guard makes the extra triggers safe: a job that already succeeded today is skipped, and a
job that keeps failing stops after MAX_ATTEMPTS tries, so an unlock never repeats a run or
spams failure pushes.

State: automation/logs/daily_state.json (gitignored), {"<job>": {"date": ..., "ok": ..., "attempts": ...}}.
"""

import datetime as dt
import json
from pathlib import Path

STATE = Path(__file__).resolve().parent / "logs" / "daily_state.json"
MAX_ATTEMPTS = 2


def _load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def should_run(job, today=None, path=STATE):
    """False if the job already succeeded today, or already failed MAX_ATTEMPTS times today."""
    day = (today or dt.date.today()).isoformat()
    s = _load(path).get(job) or {}
    if s.get("date") != day:
        return True
    return not s.get("ok") and s.get("attempts", 0) < MAX_ATTEMPTS


def record(job, ok, today=None, path=STATE):
    day = (today or dt.date.today()).isoformat()
    state = _load(path)
    s = state.get(job) or {}
    attempts = s.get("attempts", 0) + 1 if s.get("date") == day else 1
    state[job] = {"date": day, "ok": bool(ok), "attempts": attempts,
                  "at": dt.datetime.now().strftime("%Y-%m-%d %H:%M")}
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(state, indent=2), encoding="utf-8")
