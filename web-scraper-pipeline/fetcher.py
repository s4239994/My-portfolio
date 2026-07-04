import time

import requests

import robots
import sound

USER_AGENT = "PortfolioScraperBot/1.0 (educational project)"
REQUEST_DELAY_SECONDS = 1.0
MAX_RETRIES = 3


class RobotsDisallowed(Exception):
    pass


def fetch(url: str) -> str:
    """Fetch a URL politely: checks robots.txt first, retries with backoff on
    failure, and waits between requests so the pipeline never hammers the site."""
    if not robots.is_allowed(url):
        raise RobotsDisallowed(f"robots.txt disallows fetching {url}")

    sound.play_page_hum()

    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=10)
            response.raise_for_status()
            time.sleep(REQUEST_DELAY_SECONDS)
            # requests falls back to Latin-1 when a server doesn't declare a
            # charset, which mangles non-ASCII characters (curly quotes, etc).
            # apparent_encoding sniffs the real encoding from the content itself.
            response.encoding = response.apparent_encoding
            return response.text
        except requests.RequestException as exc:
            last_error = exc
            time.sleep(attempt * 1.5)

    raise ConnectionError(f"Failed to fetch {url} after {MAX_RETRIES} attempts: {last_error}")
