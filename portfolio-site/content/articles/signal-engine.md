Title: Signal Engine
Date: 2026-07-07
Tags: python, ai, automation
Summary: An AI-powered lead enrichment and outreach pipeline -- a self-built version of what GTM automation studios sell as a service.

An AI-powered lead enrichment and outreach automation pipeline -- upload a
list of companies, get each one scored against an ideal customer profile
using real public signals, plus a genuinely personalized outreach opener,
streamed live one lead at a time.

## How it works

- Fetches each company's real public homepage (respecting `robots.txt`) and
  detects actual signals: tech stack in use, whether they have a careers
  page, and what their own marketing copy says
- A fully configurable rules engine blends those signals into a 0-100 fit
  score -- editable live in the sidebar, not hardcoded
- Claude drafts a short outreach opener per lead that references one
  specific real signal, never generic flattery
- Every lead streams into a live terminal-style log as it's processed
- Exports a clean, HubSpot-ready CSV

This is a self-built version of the exact category of tool a modern GTM/RevOps
studio sells as a service -- connecting prospecting, enrichment, scoring, and
outreach into one live system.

## Stack

Python, Streamlit, Claude API, BeautifulSoup.
