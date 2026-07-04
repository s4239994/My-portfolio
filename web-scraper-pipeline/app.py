import html
import time

import pandas as pd
import streamlit as st

import database
import pipeline
import sound

st.set_page_config(page_title="Web Scraper Pipeline", page_icon="🕸️", layout="wide")

ACCENT_TEAL = "#2dd4bf"

st.markdown(
    """
    <style>
    .terminal-tag {
        font-family: "Consolas", "SFMono-Regular", Menlo, monospace;
        color: #39FF88;
        opacity: 0.85;
        letter-spacing: 2px;
        font-size: 0.8rem;
    }
    .hero-card {
        background: linear-gradient(135deg, rgba(45,212,191,0.10), rgba(57,255,136,0.02));
        border: 1px solid #2a2b2f;
        border-left: 4px solid #2dd4bf;
        border-radius: 12px;
        padding: 1.5rem 1.75rem;
        margin-bottom: 1.5rem;
    }
    .hero-title { margin: 0.3rem 0 0.4rem; font-size: 1.9rem; }
    .hero-caption { color: #9a9a9a; margin: 0; font-size: 0.95rem; }
    .pipeline-steps { display: flex; gap: 0.6rem; margin-bottom: 1.5rem; }
    .pipeline-step {
        flex: 1; text-align: center; padding: 0.7rem 0.5rem; border-radius: 8px;
        background: #17181b; border: 1px solid #2a2b2f;
        font-family: "Consolas", "SFMono-Regular", Menlo, monospace;
        font-size: 0.8rem; color: #9a9a9a;
    }
    .pipeline-step b { display: block; color: #f5f5f5; font-size: 0.95rem; margin-bottom: 2px; }
    .pipeline-arrow { align-self: center; color: #2dd4bf; font-size: 1.1rem; }
    .stat-card {
        background: #17181b; border: 1px solid #2a2b2f; border-radius: 10px;
        padding: 0.9rem; text-align: center;
    }
    .stat-card .value { font-size: 1.6rem; font-weight: 700; color: #2dd4bf; }
    .stat-card .label { font-size: 0.8rem; color: #9a9a9a; margin-top: 2px; }
    .terminal-log {
        background: #0a0a0b; border: 1px solid #2a2b2f; border-radius: 8px;
        padding: 0.85rem 1.1rem; font-family: "Consolas", "SFMono-Regular", Menlo, monospace;
        font-size: 0.8rem; color: #39FF88; max-height: 340px; overflow-y: auto;
        white-space: pre-wrap; line-height: 1.5;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def stat_card(value, label: str) -> str:
    return f'<div class="stat-card"><div class="value">{value}</div><div class="label">{label}</div></div>'


st.markdown(
    """
    <div class="hero-card">
        <p class="terminal-tag">&gt; VIBE STATE: PIPELINE ENGAGED</p>
        <p class="hero-title">🕸️ Automated Web Scraper &amp; Data Pipeline</p>
        <p class="hero-caption">Streams book listings from books.toscrape.com (a public
        scraping sandbox site) through a fetch -> parse -> clean -> store pipeline,
        one item at a time.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="pipeline-steps">
        <div class="pipeline-step"><b>1. Fetch</b>robots.txt + rate limit</div>
        <div class="pipeline-arrow">→</div>
        <div class="pipeline-step"><b>2. Parse</b>HTML structure</div>
        <div class="pipeline-arrow">→</div>
        <div class="pipeline-step"><b>3. Clean</b>normalize types</div>
        <div class="pipeline-arrow">→</div>
        <div class="pipeline-step"><b>4. Store</b>SQLite</div>
    </div>
    """,
    unsafe_allow_html=True,
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

            safe_title = html.escape(item["title"])
            log_lines.append(
                f"[{count:03d}] {safe_title} -- £{item['price']} -- "
                f"{item['rating']}* -- {item['availability']}"
            )
            log_html = "\n".join(log_lines[-15:])
            log_placeholder.markdown(f'<div class="terminal-log">{log_html}</div>', unsafe_allow_html=True)

            elapsed = time.time() - start_time
            rate = count / elapsed if elapsed > 0 else 0
            stats_placeholder.markdown(
                f'<div style="max-width:260px;">{stat_card(count, f"items streamed -- {rate:.1f}/sec")}</div>',
                unsafe_allow_html=True,
            )

        st.success(f"Done -- {count} items streamed into the database.")
    except Exception as exc:
        st.error(f"Pipeline stopped early after {count} items: {exc}")

st.divider()
st.subheader("Stored data")

conn = database.get_connection()
stats = database.get_stats(conn)
col1, col2, col3, col4 = st.columns(4)
col1.markdown(stat_card(stats["count"], "Total items"), unsafe_allow_html=True)
col2.markdown(stat_card(f"£{stats['avg_price']}", "Avg price"), unsafe_allow_html=True)
col3.markdown(stat_card(f"£{stats['min_price']}", "Min price"), unsafe_allow_html=True)
col4.markdown(stat_card(f"£{stats['max_price']}", "Max price"), unsafe_allow_html=True)

st.write("")
rows = database.fetch_all(conn)
if rows:
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)
    st.download_button("Download as CSV", df.to_csv(index=False), file_name="scraped_books.csv")
else:
    st.info("No data yet -- click 'Start Pipeline' to begin.")
