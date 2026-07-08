from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

USER_AGENT = "VibeCheckBot/1.0 (workplace culture research demo project)"

_cache: dict = {}


def is_allowed(url: str) -> bool:
    """Check robots.txt before fetching -- this only ever visits a company's
    own public careers/about page, the same way a browser would, and backs
    off if the site's own rules say not to."""
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"

    if base not in _cache:
        parser = RobotFileParser()
        parser.set_url(f"{base}/robots.txt")
        try:
            parser.read()
        except Exception:
            parser = None
        _cache[base] = parser

    parser = _cache[base]
    if parser is None:
        return True
    return parser.can_fetch(USER_AGENT, url)
