from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

USER_AGENT = "PortfolioScraperBot/1.0 (educational project)"

_cache: dict = {}


def is_allowed(url: str) -> bool:
    """Check robots.txt before fetching anything -- this is what makes the
    scraper 'non-intrusive' in practice, not just in intent."""
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"

    if base not in _cache:
        parser = RobotFileParser()
        parser.set_url(f"{base}/robots.txt")
        try:
            parser.read()
        except Exception:
            # No readable robots.txt -- most sites without one don't restrict crawling.
            parser = None
        _cache[base] = parser

    parser = _cache[base]
    if parser is None:
        return True
    return parser.can_fetch(USER_AGENT, url)
