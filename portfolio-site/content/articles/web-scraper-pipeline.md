Title: Automated Web Scraper & Data Pipeline
Date: 2026-07-05
Tags: python, data, automation
Summary: A streaming fetch-parse-clean-store pipeline with ethical scraping practices built in, not bolted on.

Streams book listings from a public scraping-practice site through a real
fetch -> parse -> clean -> store pipeline, one item at a time -- with a live
dashboard, audio feedback, and a local database.

## How it works

- Checks `robots.txt` before every request and refuses to fetch disallowed
  pages, rather than only claiming to be polite
- Rate-limited on purpose -- one request at a time, with a pause between
  pages, favoring politeness over raw speed
- The pipeline is a Python generator: items are fetched, parsed, cleaned,
  and stored one at a time, never loading the whole site into memory
- Automatic retries with backoff on network failures
- Stores into a local SQLite database, with a live Streamlit dashboard and
  a terminal channel sharing the exact same pipeline

## Stack

Python, requests, BeautifulSoup, SQLite, Streamlit.
