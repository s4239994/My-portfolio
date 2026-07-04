import re

RATING_VALUES = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def clean_item(raw_item: dict) -> dict:
    """Turn a raw scraped dict into clean, normalized, ready-for-storage values."""
    price_match = re.search(r"[\d.]+", raw_item.get("raw_price", ""))
    price = float(price_match.group()) if price_match else None

    rating = RATING_VALUES.get(raw_item.get("rating_word"))

    raw_availability = raw_item.get("raw_availability", "")
    availability = "In stock" if "in stock" in raw_availability.lower() else "Out of stock"

    return {
        "title": raw_item["title"].strip(),
        "price": price,
        "rating": rating,
        "availability": availability,
        "category": raw_item.get("category"),
        "source_url": raw_item.get("source_url"),
    }
