import requests
from bs4 import BeautifulSoup

import robots

USER_AGENT = "SignalEngineBot/1.0 (lead research demo project)"
TIMEOUT = 10

CAREER_PATH_HINTS = ["/careers", "/jobs", "/join-us", "/work-with-us", "/hiring", "/join"]

TECH_SIGNATURES = {
    "WordPress": ["wp-content", "wp-includes"],
    "Shopify": ["cdn.shopify.com", "shopify.theme"],
    "Webflow": ["webflow.com", "data-wf-site", "data-wf-page"],
    "HubSpot": ["hubspot.com", "hs-scripts.com", "_hsq"],
    "Squarespace": ["squarespace.com", "static1.squarespace.com"],
    "Salesforce": ["force.com", "salesforce.com/embeddedservice"],
    "Marketo": ["marketo.com", "munchkin.js"],
    "Next.js": ["__next", "/_next/static"],
}


def enrich_company(name: str, url: str) -> dict:
    """Fetch a company's public homepage (politely) and pull out signals a
    sales team would actually care about: their tech stack, whether they're
    hiring, and what their own marketing copy says about them."""
    if not robots.is_allowed(url):
        return _empty_result(name, url, note="robots.txt disallows fetching this site")

    try:
        response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        html_text = response.text
    except requests.RequestException as exc:
        return _empty_result(name, url, note=f"Could not reach site ({exc.__class__.__name__})")

    soup = BeautifulSoup(html_text, "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else ""

    meta_tag = soup.find("meta", attrs={"name": "description"})
    meta_description = (meta_tag.get("content") or "").strip() if meta_tag else ""

    lowered_html = html_text.lower()
    detected_tech = [
        tech for tech, signatures in TECH_SIGNATURES.items()
        if any(sig.lower() in lowered_html for sig in signatures)
    ]

    has_careers_page = any(
        link.get("href") and any(hint in link["href"].lower() for hint in CAREER_PATH_HINTS)
        for link in soup.find_all("a", href=True)
    )

    return {
        "name": name,
        "url": url,
        "title": title,
        "meta_description": meta_description,
        "detected_tech": detected_tech,
        "has_careers_page": has_careers_page,
        "note": None,
    }


def _empty_result(name: str, url: str, note: str) -> dict:
    return {
        "name": name,
        "url": url,
        "title": "",
        "meta_description": "",
        "detected_tech": [],
        "has_careers_page": False,
        "note": note,
    }
