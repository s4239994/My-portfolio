# Signal Engine

An AI-powered lead enrichment and outreach automation pipeline — upload a
list of companies, get each one scored against your ideal customer profile
using *real* public signals, plus a genuinely personalized outreach opener,
streamed live one lead at a time.

## Why this project exists

This is a self-built version of the exact category of tool a modern GTM/RevOps
studio sells as a service: connecting prospecting, enrichment, scoring, and
outreach into one live system (the same idea behind tools like Clay). The
goal wasn't to *use* that kind of tool, but to build the underlying engine
myself, end to end.

## What it does

1. **Upload leads** — a CSV of company names + websites (or use the sample set)
2. **Enrich** — fetches each company's real public homepage (respecting
   `robots.txt`, the same as a browser would) and detects actual signals:
   tech stack in use, whether they have a careers page (a growth signal),
   and what their own marketing copy says about them
3. **Score** — a fully configurable rules engine (edit the target tech,
   keywords, and weights live in the sidebar) blends those signals into a
   0-100 fit score
4. **Personalize** — Claude drafts a short outreach opener per lead that
   references one specific real signal, not generic flattery
5. **Stream live** — every lead appears in a live terminal-style log as it's
   processed, instead of waiting for the whole batch
6. **Export** — a clean CSV with HubSpot-friendly column names, ready to import

## Setup

```
pip install -r requirements.txt
```

Get a free Anthropic API key at https://console.anthropic.com/settings/keys,
then copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and
fill in your key:

```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

`secrets.toml` is git-ignored — it never gets committed. You can also turn
off AI personalization entirely in the sidebar and use the tool for scoring
only, with no API key needed.

## Running it

```
streamlit run app.py
```

## How it's organized

- **[robots.py](robots.py)** — checks a site's `robots.txt` before fetching it
- **[enrichment.py](enrichment.py)** — fetches a company's homepage and
  detects tech stack, careers page, and marketing copy
- **[scoring.py](scoring.py)** — the configurable ICP rules engine
- **[personalize.py](personalize.py)** — the Claude call that drafts each opener
- **[pipeline.py](pipeline.py)** — the streaming generator tying it all together
- **[app.py](app.py)** — the live dashboard

## Cost

Personalization costs a small fraction of a cent per lead (Claude is only
given a few sentences of context and asked for a two-sentence reply).
Scoring and enrichment are completely free — no API calls involved.

## A note on scraping

This only ever fetches a company's own public homepage — the same page
anyone gets by typing the URL into a browser — and always checks
`robots.txt` first. It never accesses anything private or authenticated.
