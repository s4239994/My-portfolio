from typing import Iterator

import fetcher
import parser
import transform

DEFAULT_START_URL = "https://books.toscrape.com/index.html"
DEFAULT_CATEGORY = "All books"


def run_pipeline(
    start_url: str = DEFAULT_START_URL,
    category: str = DEFAULT_CATEGORY,
    max_pages: int = 5,
) -> Iterator[dict]:
    """Stream cleaned items one at a time -- fetch, parse, clean, yield -- instead
    of collecting every page into memory before processing anything."""
    url = start_url
    pages_fetched = 0

    while url and pages_fetched < max_pages:
        html = fetcher.fetch(url)
        raw_items, next_url = parser.parse_listing_page(html, url, category)
        pages_fetched += 1

        for raw_item in raw_items:
            yield transform.clean_item(raw_item)

        url = next_url
