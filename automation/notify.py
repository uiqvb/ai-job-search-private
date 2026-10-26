"""Send a push notification through ntfy (https://ntfy.sh).

Config comes from automation/config.json (gitignored): {"ntfy_server": "...", "ntfy_topic": "..."}.
The topic name is the only secret: anyone who knows it can read and post, so keep it random.

    python automation/notify.py "Title" "Message" [--priority high] [--tags calendar]
"""

import json
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONFIG = HERE / "config.json"


def load_config():
    if not CONFIG.exists():
        sys.exit(f"Missing {CONFIG}. Copy config.example.json and set your ntfy topic.")
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def morning_delivery():
    """Unix time of today's delivery slot (config "deliver_at", default 07:30) if it is still ahead,
    else None (send now). Night runs use it so pushes arrive in the morning, not at 1 am."""
    import datetime as dt
    hh, mm = map(int, load_config().get("deliver_at", "07:30").split(":"))
    slot = dt.datetime.now().replace(hour=hh, minute=mm, second=0, microsecond=0)
    return int(slot.timestamp()) if slot > dt.datetime.now() + dt.timedelta(seconds=30) else None


def send(title, message, priority="default", tags="", actions="", at=None):
    cfg = load_config()
    url = cfg.get("ntfy_server", "https://ntfy.sh").rstrip("/") + "/" + cfg["ntfy_topic"]
    req = urllib.request.Request(url, data=message.encode("utf-8"), method="POST")
    # HTTP headers must be latin-1; ntfy accepts RFC 2047 encoded titles for anything else
    req.add_header("Title", "=?UTF-8?B?" + __import__("base64").b64encode(title.encode()).decode() + "?=")
    req.add_header("Priority", priority)
    if tags:
        req.add_header("Tags", tags)
    if at:  # ntfy holds the message on its server until this Unix time (max 3 days ahead)
        req.add_header("At", str(at))
    if actions:  # ntfy action buttons, e.g. "view, Open, https://..."; URLs are ASCII
        req.add_header("Actions", actions.encode("ascii", "ignore").decode())
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.status


if __name__ == "__main__":
    args = sys.argv[1:]
    prio, tags = "default", ""
    if "--priority" in args:
        i = args.index("--priority"); prio = args[i + 1]; del args[i:i + 2]
    if "--tags" in args:
        i = args.index("--tags"); tags = args[i + 1]; del args[i:i + 2]
    if len(args) != 2:
        sys.exit('usage: notify.py "Title" "Message" [--priority high] [--tags x]')
    print("sent", send(args[0], args[1], prio, tags))
