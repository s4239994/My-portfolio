AUTHOR = "s4239994"
SITENAME = "My Portfolio"
SITESUBTITLE = "> get set go"
SITEURL = ""

PATH = "content"
TIMEZONE = "UTC"
DEFAULT_LANG = "en"

THEME = "theme"

ARTICLE_PATHS = ["articles"]
ARTICLE_URL = "projects/{slug}/"
ARTICLE_SAVE_AS = "projects/{slug}/index.html"

PAGE_PATHS = ["pages"]
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"

DEFAULT_PAGINATION = 10
RELATIVE_URLS = True

# This is a portfolio, not a blog -- no feeds needed.
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_DATE_FORMAT = "%B %Y"
