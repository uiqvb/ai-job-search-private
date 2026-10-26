"""Power helpers for the overnight jobs (Windows).

The laptop's lid action is hibernate (Modern Standby ignores wake timers on battery; hibernate
is woken by the firmware clock). A job woken by its timer must:
  1. keep the laptop awake while it runs (Windows would otherwise drop back to standby after ~2 min),
  2. wait for Wi-Fi to reconnect,
  3. hibernate again afterwards, but only if nobody touched the laptop during the run and it is
     still night, so it never hibernates under someone who is using it.

    with night_run() as run:
        ...job...
    # on exit: hibernates if run.should_hibernate()
"""

import contextlib
import ctypes
import datetime as dt
import socket
import subprocess
import sys
import time

NIGHT_END_HOUR = 6  # runs that finish before 06:00 with no user input put the laptop back to hibernate

_ES_CONTINUOUS, _ES_SYSTEM_REQUIRED = 0x80000000, 0x00000001


class _LastInput(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]


def last_input_tick():
    """Tick count of the last keyboard/mouse input, or None off Windows."""
    if sys.platform != "win32":
        return None
    li = _LastInput(ctypes.sizeof(_LastInput), 0)
    return li.dwTime if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(li)) else None


def keep_awake(on):
    if sys.platform == "win32":
        flags = _ES_CONTINUOUS | (_ES_SYSTEM_REQUIRED if on else 0)
        ctypes.windll.kernel32.SetThreadExecutionState(flags)


def wait_for_network(host="ntfy.sh", port=443, timeout_s=180):
    """After a wake, Wi-Fi takes a few seconds to come back. True once host is reachable."""
    end = time.monotonic() + timeout_s
    while time.monotonic() < end:
        try:
            socket.create_connection((host, port), timeout=5).close()
            return True
        except OSError:
            time.sleep(5)
    return False


def is_night(now=None):
    return (now or dt.datetime.now()).hour < NIGHT_END_HOUR


class NightRun:
    def __init__(self):
        self.start_input = last_input_tick()

    def should_hibernate(self, now=None):
        """Only at night, and only if there was no keyboard/mouse input since the job started."""
        if sys.platform != "win32" or self.start_input is None:
            return False
        return is_night(now) and last_input_tick() == self.start_input


@contextlib.contextmanager
def night_run(hibernate=True):
    run = NightRun()
    keep_awake(True)
    try:
        wait_for_network()
        yield run
    finally:
        keep_awake(False)
        if hibernate and run.should_hibernate():
            print("no one used the laptop during the run; hibernating")
            subprocess.run(["shutdown", "/h"], check=False)
