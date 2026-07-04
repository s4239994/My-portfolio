import time

import pandas as pd
import streamlit as st

import database
import pipeline
import sound

st.set_page_config(page_title="Web Scraper Pipeline", page_icon="🕸️", layout="wide")

st.title("🕸️ Automated Web Scraper & Data Pipeline")
st.caption(
    "Streams book listings from books.toscrape.com (a public scraping sandbox site) "
    "through a fetch -> parse -> clean -> store pipeline, one item at a time."
)

with st.sidebar:
    st.header("Settings")
    max_pages = st.slider("Pages to scrape", 1, 20, 3)
    st.caption(
        "Checks robots.txt before every request and waits ~1s between pages -- "
        "built to be non-intrusive, not fast."
    )
    if st.button("Clear stored data"):
        conn = database.get_connection()
        database.clear_all(conn)
        st.success("Cleared.")

start_clicked = st.button("Start Pipeline", type="primary")

log_placeholder = st.empty()
stats_placeholder = st.empty()

if start_clicked:
    conn = database.get_connection()
    log_lines = []
    start_time = time.time()
    count = 0

    try:
        for item in pipeline.run_pipeline(max_pages=max_pages):
            database.insert_item(conn, item)
            sound.play_item_click()
            count += 1

            log_lines.append(
                f"[{count}] {item['title']} -- £{item['price']} -- "
                f"{item['rating']}* -- {item['availability']}"
            )
            log_placeholder.code("\n".join(log_lines[-15:]), language=None)

            elapsed = time.time() - start_time
            rate = count / elapsed if elapsed > 0 else 0
            stats_placeholder.metric("Items streamed", count, f"{rate:.1f} items/sec")

        st.success(f"Done -- {count} items streamed into the database.")
    except Exception as exc:
        st.error(f"Pipeline stopped early after {count} items: {exc}")

st.divider()
st.subheader("Stored data")

conn = database.get_connection()
stats = database.get_stats(conn)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total items", stats["count"])
col2.metric("Avg price", f"£{stats['avg_price']}")
col3.metric("Min price", f"£{stats['min_price']}")
col4.metric("Max price", f"£{stats['max_price']}")

rows = database.fetch_all(conn)
if rows:
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)
    st.download_button("Download as CSV", df.to_csv(index=False), file_name="scraped_books.csv")
else:
    st.info("No data yet -- click 'Start Pipeline' to begin.")
