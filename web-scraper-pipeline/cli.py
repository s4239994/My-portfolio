import argparse

import database
import pipeline
import sound


def main() -> None:
    arg_parser = argparse.ArgumentParser(description="Stream book listings into a local SQLite database.")
    arg_parser.add_argument("--pages", type=int, default=3, help="Number of listing pages to scrape")
    args = arg_parser.parse_args()

    conn = database.get_connection()
    count = 0

    print(f"Streaming up to {args.pages} pages from books.toscrape.com...\n")
    for item in pipeline.run_pipeline(max_pages=args.pages):
        database.insert_item(conn, item)
        sound.play_item_click()
        count += 1
        print(f"[{count}] {item['title']} -- £{item['price']} -- {item['rating']}* -- {item['availability']}")

    print(f"\nDone. {count} items streamed into data/scraped_books.db")


if __name__ == "__main__":
    main()
