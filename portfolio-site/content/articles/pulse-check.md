Title: Pulse
Date: 2026-07-08
Tags: python, ai, culture
Summary: A 5-second emoji team check-in instead of a long survey, with a live mood trend and an AI-written weekly manager briefing.

Tap an emoji, add a one-liner if you feel like it. No 40-question annual
survey, no login wall. Managers get a live mood trend chart and an
AI-written weekly briefing grounded in what the team actually wrote.

## How it works

- Pick a mood from five emoji options, optionally add one line about your day
- A live dashboard tracks the running mood trend, this week's average, and
  a feed of recent notes, computed from real stored check-ins
- Claude reads the last 7 days of check-ins and writes a headline, summary,
  a specific thing to watch out for, and one suggested action for the
  manager -- grounded in the actual notes people left, never invented
- A demo mode seeds 28 days of realistic check-ins for a 12-person team,
  including a deliberate mid-month crunch-week dip and recovery, so the
  trend chart and AI briefing have a real pattern to work with

## Why this project exists

Built with Melbourne HR/workplace-tech companies in mind (Culture Amp,
Employment Hero) -- both sell employee engagement tools built around
periodic surveys, which have a well-known problem: completion rates drop
fast because filling out a long survey is a chore. The fix isn't a better
survey, it's not making people fill one out at all. This applies a
consumer-app check-in pattern to the same underlying business need:
understand team morale before it becomes a resignation.

## Stack

Python, Streamlit, SQLite, Claude API.
