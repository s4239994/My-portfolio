# Pulse

A 5-second team check-in people actually do -- tap an emoji, add a one-liner
if you feel like it. No 40-question annual survey, no login wall. Managers
get a live mood trend chart and an AI-written weekly briefing grounded in
what the team actually wrote, not generic HR language.

## Why this project exists

Built with Melbourne HR/workplace-tech companies in mind (Culture Amp,
Employment Hero) -- both sell employee engagement tools built around
periodic surveys, which have a well-known problem: completion rates drop
off fast because filling out a long survey is a chore. The fix isn't a
better survey, it's not making people fill out a survey at all. This is a
consumer-app-style daily check-in instead, aimed at the same underlying
business need (understand team morale before it becomes a resignation).

## What it does

1. **Check in** -- pick your mood from five emoji options, optionally add
   one line about your day
2. **Live dashboard** -- a running mood trend chart, this-week's average,
   and a feed of recent notes, computed from real stored check-ins (SQLite)
3. **AI briefing** -- Claude reads the last 7 days of check-ins and writes
   a headline, summary, a specific thing to watch out for, and one
   suggested action for the manager -- grounded in the actual notes people
   left, never invented
4. **Demo mode** -- a "Load demo team" button seeds 28 days of realistic
   check-ins for a 12-person team, including a deliberate mid-month crunch
   week dip and recovery, so the trend chart and AI briefing have a real
   pattern to work with

## Setup

```
pip install -r requirements.txt
```

Get a free Anthropic API key at https://console.anthropic.com/settings/keys,
then copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and
fill in your key. The check-in flow and dashboard work without a key --
only the AI briefing needs it.

## Running it

```
streamlit run app.py
```

## How it's organized

- **[db.py](db.py)** -- SQLite storage for check-ins
- **[seed.py](seed.py)** -- generates a realistic demo team's check-in history
- **[briefing_ai.py](briefing_ai.py)** -- the Claude call that writes the weekly briefing
- **[app.py](app.py)** -- the check-in flow and dashboard

## Cost

The AI briefing costs a small fraction of a cent per generation. Checking in
and viewing the dashboard are completely free -- no API calls involved.

## Data note

This demo stores check-ins in a local SQLite file for the sake of a working
end-to-end demo. A real deployment would need proper auth, per-team data
isolation, and a hosted database -- this is a proof of concept of the
product idea, not a production multi-tenant app.
