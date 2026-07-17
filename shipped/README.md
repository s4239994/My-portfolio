# Shipped

A Rovo Agent concept for Atlassian -- turns your Jira ticket history into a
shareable sprint recap. Spotify Wrapped energy, but for what you actually
shipped: real stats computed from real ticket data, plus an AI-written
recap that's told never to invent a number or a ticket that isn't there.

## Why this project exists

Atlassian's biggest current push is Rovo -- their AI agent platform, where
Rovo Studio now lets teams build and deploy custom agents without writing
code, and agents can be assigned work, mentioned in comments, and embedded
into Jira workflows directly. Shipped is designed as a plausible Rovo
Agent: something built on their own current AI infrastructure, solving a
real, unglamorous problem -- nobody remembers what they actually did last
sprint when it's performance-review time, and standup recaps are tedious
to write from scratch. This turns raw ticket IDs into something people
would actually want to screenshot and share.

## What it does

1. **Upload or use sample data** -- a CSV of ticket title, type, and
   resolved date (or use the built-in sample sprint)
2. **Free stats** -- total shipped, breakdown by type, busiest day of the
   week, longest streak of consecutive shipping days -- all computed
   directly from your data, no API needed
3. **AI recap** -- Claude writes a punchy, Wrapped-style headline,
   narrative, and fun fact, referencing at least one of your real ticket
   titles, grounded only in the stats actually computed

## Setup

```
pip install -r requirements.txt
```

Get a free Anthropic API key at https://console.anthropic.com/settings/keys,
then copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and
fill in your key. The stats and charts work without a key -- only the AI
recap needs it.

## Running it

```
streamlit run app.py
```

## How it's organized

- **[parser.py](parser.py)** -- loads tickets and computes the free, deterministic stats
- **[recap_ai.py](recap_ai.py)** -- the Claude call that writes the Wrapped-style recap
- **[app.py](app.py)** -- the dashboard and the Wrapped card display

## Cost

The AI recap costs a small fraction of a cent per generation. The stats,
streak calculation, and chart are completely free -- no API calls involved.
