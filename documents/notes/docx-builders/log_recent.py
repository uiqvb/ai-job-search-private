"""Print the last N day sections of log.md (default 3).

Reads from the end of the file in growing chunks, so it never loads the
whole log just to show the recent days.

Usage: python Scripts/log_recent.py [days]
"""
import os
import re
import sys

LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "log.md")
HEADING = re.compile(rb"^## \d{4}-\d{2}-\d{2}", re.M)


def recent(days=3, chunk=16 * 1024):
    size = os.path.getsize(LOG)
    with open(LOG, "rb") as f:
        while True:
            start = max(0, size - chunk)
            f.seek(start)
            data = f.read()
            heads = [m.start() for m in HEADING.finditer(data)]
            # The first heading in a partial chunk may be cut off, so only
            # trust it once we have one more than we need or reached the start.
            if len(heads) > days or start == 0:
                return data[heads[-days]:] if len(heads) >= days else data[heads[0]:] if heads else data
            chunk *= 2


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    sys.stdout.buffer.write(recent(n))
