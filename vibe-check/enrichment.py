import requests
from bs4 import BeautifulSoup

import robots

USER_AGENT = "VibeCheckBot/1.0 (workplace culture research demo project)"
TIMEOUT = 8


def fetch_page_text(url: str) -> dict:
    """Fetches a company's own public careers/about page and returns its
    visible text. Only ever hits a page a browser could also load, and
    checks robots.txt first."""
    if not robots.is_allowed(url):
        return _empty_result(url, "Blocked by this site's robots.txt -- skipped.")

    try:
        response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
    except Exception as exc:
        return _empty_result(url, f"Couldn't fetch this page: {exc}")

    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "svg"]):
        tag.decompose()

    title = soup.title.get_text(strip=True) if soup.title else ""
    text = " ".join(soup.get_text(separator=" ").split())

    return {
        "url": url,
        "title": title,
        "text": text[:8000],
        "note": "",
    }


def _empty_result(url: str, note: str) -> dict:
    return {"url": url, "title": "", "text": "", "note": note}
