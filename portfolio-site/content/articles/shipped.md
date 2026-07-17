Title: Shipped
Date: 2026-07-18
Tags: python, ai, productivity
Summary: A Rovo Agent concept for Atlassian -- turns your Jira ticket history into a shareable, Spotify-Wrapped-style sprint recap.

Turns raw Jira ticket history into a shareable sprint recap -- Spotify
Wrapped energy, but for what you actually shipped. Real stats computed
from real ticket data, plus an AI-written recap that's told never to
invent a number or a ticket that isn't there.

## How it works

- Upload a CSV of ticket title, type, and resolved date (or use the
  built-in sample sprint)
- Free, deterministic stats: total shipped, breakdown by type, busiest day
  of the week, longest streak of consecutive shipping days
- Claude writes a punchy, Wrapped-style headline, narrative, and fun fact,
  referencing at least one real ticket title, grounded only in the actual
  computed stats

## Why this project exists

Atlassian's biggest current push is Rovo -- their AI agent platform, where
Rovo Studio now lets teams build and deploy custom agents without writing
code. Shipped is designed as a plausible Rovo Agent: built on their own
current AI infrastructure, solving a real, unglamorous problem -- nobody
remembers what they actually did last sprint at performance-review time,
and standup recaps are tedious to write from scratch.

## Stack

Python, Streamlit, Claude API.
