# Automated Web Scraper & Data Pipeline

Streams book listings from a public scraping-practice site through a real
fetch -> parse -> clean -> store pipeline, one item at a time -- with a live
dashboard, audio feedback, and a local database, no accounts or cost.

## Why books.toscrape.com

The target site is [books.toscrape.com](https://books.toscrape.com) -- a
site built specifically for people to practice web scraping on, with no
terms-of-service risk. Pointing a scraper at a real commercial site (Amazon,
LinkedIn, etc.) without permission is a real legal and ethical problem, so
this project deliberately targets a site that exists for exactly this
purpose instead.

## What it does

- **Checks `robots.txt` before every request** -- if a site's rules ever
  disallow a page, the scraper refuses to fetch it, instead of only
  pretending to be polite.
- **Rate-limited on purpose** -- one request at a time, with a pause between
  pages. This is a deliberate choice: real concurrency would fetch faster,
  but it conflicts with "non-intrusive," so this always chooses politeness
  over raw speed.
- **Streams instead of hoarding** -- the pipeline is a Python generator. Each
  item is fetched, parsed, cleaned, and stored one at a time; it never loads
  the whole site into memory before doing anything with it.
- **Cleans and normalizes on the fly** -- raw text like `"£51.77"` and
  `"star-rating Three"` get converted into a real float price and integer
  rating before they're stored.
- **Reliable against network hiccups** -- automatic retries with backoff if
  a request fails, instead of the whole pipeline crashing.
- **Stores into a local SQLite database** -- no server, no setup.
- **Audio feedback** -- a low tone each time a new page starts loading, a
  sharp click for every individual item parsed off that page.

## Setup

```
pip install -r requirements.txt
```

No accounts, no API keys.

## Running it

**Live dashboard:**
```
streamlit run app.py
```
Pick how many pages to scrape and click **Start Pipeline** -- watch items
stream in live, then browse or download the results as CSV.

**Terminal:**
```
python cli.py --pages 3
```

Both share the exact same pipeline (`pipeline.py`) -- proof the scraping
logic isn't tied to one interface.

## How it's organized

- **[robots.py](robots.py)** -- checks a site's `robots.txt` before any
  request goes out.
- **[fetcher.py](fetcher.py)** -- the actual HTTP layer: robots check, retry
  with backoff, rate limiting, a proper User-Agent string.
- **[parser.py](parser.py)** -- knows books.toscrape.com's specific HTML
  structure (this is the one file that would need rewriting for a different
  site -- every site's HTML is different, so this is normal for scrapers).
- **[transform.py](transform.py)** -- turns raw scraped text into clean,
  typed values.
- **[database.py](database.py)** -- the SQLite schema and read/write helpers.
- **[pipeline.py](pipeline.py)** -- the generator that ties fetch -> parse ->
  clean -> yield together, handling pagination automatically.
- **[sound.py](sound.py)** -- the audio cues.
- **[app.py](app.py)** -- the Streamlit live dashboard.
- **[cli.py](cli.py)** -- the terminal channel.

## Pointing it at a different site

Change `DEFAULT_START_URL` in `pipeline.py`, and write a new function in
`parser.py` that knows *that* site's HTML structure (open the page, look at
its HTML, find the CSS selectors for the fields you want). `robots.py` and
`fetcher.py` don't change -- they work for any site.
