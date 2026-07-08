# Vibe Check

A blunt, AI-powered "vibe check" for a company's careers page -- scans it for
real corporate-speak red flags (buzzwords, vague pay, missing flexibility)
and hands back a verdict quoting the company's own words, no sugarcoating.

## Why this project exists

Built with Melbourne's AI/software scene in mind (Culture Amp, Employment
Hero, and every other workplace-tech company selling "great culture" to
candidates) -- but pointed the tool at the industry itself instead of at
job-seekers. It's the honest version of an "employee experience" product:
instead of scoring how a company *says* it treats people, it checks what
their own careers page actually says, word for word.

## What it does

1. **Fetch** -- pulls a company's own public careers/about page (checking
   `robots.txt` first, same as a browser would)
2. **Scan for free** -- a configurable, no-API-needed rules engine flags
   buzzwords ("rockstar", "wear many hats", "unlimited PTO") and rewards
   real signals (an actual salary number, flexible hours, mental health
   mentions) into a 0-100 vibe score
3. **Roast (optional)** -- Claude reads the page plus anything you paste in
   (a job posting, review snippets you copied yourself) and writes a blunt
   verdict, quoting exact phrases for every red or green flag -- it's told
   never to invent a quote that isn't actually there
4. **Stamp it** -- APPROVED / MID / RED FLAG, rendered like an actual rubber
   stamp

## On Glassdoor/LinkedIn

This tool never scrapes Glassdoor or LinkedIn -- both explicitly prohibit
automated scraping in their terms of service, unlike a company's own public
careers page. If you want a review-based verdict, copy-paste the review text
yourself into the "extra material" box. Same information, no ToS violation.

## Setup

```
pip install -r requirements.txt
```

Get a free Anthropic API key at https://console.anthropic.com/settings/keys,
then copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and
fill in your key. You can also turn off the AI step entirely in the sidebar
and just use the free deterministic scan.

## Running it

```
streamlit run app.py
```

## How it's organized

- **[robots.py](robots.py)** -- checks a site's `robots.txt` before fetching it
- **[enrichment.py](enrichment.py)** -- fetches a company's careers page text
- **[scoring.py](scoring.py)** -- the free, configurable buzzword rules engine
- **[vibe_ai.py](vibe_ai.py)** -- the Claude call that drafts quoted flags + verdict
- **[app.py](app.py)** -- the dashboard

## Cost

The AI step costs a small fraction of a cent per check. The scan itself is
completely free -- no API calls involved.
