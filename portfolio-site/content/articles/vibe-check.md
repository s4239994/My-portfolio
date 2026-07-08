Title: Vibe Check
Date: 2026-07-08
Tags: python, ai, culture
Summary: A blunt AI "vibe check" for a company's careers page -- scans for corporate-speak red flags and hands back a verdict quoting the company's own words.

Paste a company's careers page URL and it gets scanned for real: buzzword
red flags, missing pay transparency, generic corporate-speak -- plus an
AI-written verdict that quotes the company's own words back at them,
no sugarcoating.

## How it works

- Fetches a company's own public careers page (respecting `robots.txt`,
  same as a browser would)
- A free, configurable rules engine scores it 0-100 based on buzzwords
  ("rockstar", "wear many hats", "unlimited PTO") versus real signals (an
  actual salary number, flexible hours, mental health mentions)
- Claude reads the page (plus anything you paste in yourself -- a job
  posting, review snippets) and writes a blunt verdict, quoting an exact
  phrase for every red or green flag -- it's told never to invent a quote
- Stamped APPROVED / MID / RED FLAG, styled like an actual rubber stamp

## Why this project exists

Built with Melbourne's workplace-tech scene in mind (Culture Amp, Employment
Hero, and the rest of the industry selling "great culture" to candidates)
-- but pointed at the industry itself instead of at job-seekers. It's the
honest version of an "employee experience" product: instead of scoring how
a company *says* it treats people, it checks what their own careers page
actually says.

Deliberately never scrapes Glassdoor or LinkedIn -- both prohibit automated
scraping in their terms of service. If you want a review-based verdict,
you paste the text in yourself.

## Stack

Python, Streamlit, Claude API, BeautifulSoup.
