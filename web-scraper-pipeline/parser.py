from urllib.parse import urljoin

from bs4 import BeautifulSoup

RATING_WORDS = {"One", "Two", "Three", "Four", "Five"}


def parse_listing_page(html: str, page_url: str, category: str) -> tuple:
    """Pull raw book entries out of a books.toscrape.com listing page, plus
    the URL of the next page if there is one. Returns (items, next_page_url)."""
    soup = BeautifulSoup(html, "html.parser")
    items = []

    for article in soup.select("article.product_pod"):
        title_tag = article.select_one("h3 a")
        title = title_tag["title"].strip() if title_tag else "Unknown"
        detail_href = title_tag["href"] if title_tag else ""
        source_url = urljoin(page_url, detail_href)

        price_tag = article.select_one("p.price_color")
        raw_price = price_tag.get_text(strip=True) if price_tag else ""

        rating_tag = article.select_one("p.star-rating")
        rating_word = None
        if rating_tag:
            rating_word = next((c for c in rating_tag.get("class", []) if c in RATING_WORDS), None)

        availability_tag = article.select_one("p.instock.availability")
        raw_availability = availability_tag.get_text(strip=True) if availability_tag else ""

        items.append({
            "title": title,
            "raw_price": raw_price,
            "rating_word": rating_word,
            "raw_availability": raw_availability,
            "category": category,
            "source_url": source_url,
        })

    next_tag = soup.select_one("li.next a")
    next_url = urljoin(page_url, next_tag["href"]) if next_tag else None

    return items, next_url
