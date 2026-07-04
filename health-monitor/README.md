# Server & System Health Monitor

A lightweight terminal dashboard that watches your computer's CPU, memory, disk,
and open network ports — with color-coded status and sound alerts.

## What it does

- **Checks CPU, memory, and disk usage** every few seconds
- **Scans common ports on your own machine** to see what's listening
- **Shows a live color-coded dashboard** right in the terminal — green means
  healthy, yellow means warning, red means something needs attention
- **Plays a sound** whenever the overall health status changes: a low hum when
  things return to normal, a pulsing tone on a warning, a sharp ping on critical
- **Logs alerts** to `health_alerts.log` so you have a record of when things went wrong

## Setup

```
pip install -r requirements.txt
```

## Run it

```
python monitor.py
```

Leave the terminal window open — it keeps refreshing every 3 seconds. Press
`Ctrl+C` to stop it.

## How it's organized

- **[checks.py](checks.py)** — reads CPU/memory/disk from the OS, and scans a
  list of common ports (HTTP, SSH, MySQL, etc.) on `127.0.0.1` to see which are open
- **[alerts.py](alerts.py)** — decides what counts as "warning" (75%+) or
  "critical" (90%+), plays the matching sound, and writes to the alert log
- **[monitor.py](monitor.py)** — the main loop: pulls the latest checks, draws
  the dashboard, and re-runs every few seconds

## Tuning it

- Change `WARNING_THRESHOLD` / `CRITICAL_THRESHOLD` in `alerts.py` to make it
  more or less sensitive.
- Change `REFRESH_SECONDS` in `monitor.py` to check more or less often.
- Add or remove ports in `COMMON_PORTS` in `checks.py`.

## Note on the sound

Sound only plays when the overall status *changes* (e.g. healthy → warning),
not on every refresh — a continuous hum every 3 seconds would get annoying fast
in a tool meant to run in the background.
