# Magic Trends

A 5-page concept website for a feature Canva could plausibly ship next:
an AI tool that turns currently-circulating aesthetic trends into
ready-to-edit color palettes, font pairings, and layout packs inside
Canva's editor. Not an official Canva product -- a self-directed design
and build exercise, aimed at Melbourne's biggest design-tech company.

**[View it locally](index.html)** -- open `index.html` in a browser, or run a
local server (see below).

## Why this project exists

Canva's current push is "Magic Studio" -- a family of AI tools (Magic
Design, Dream Lab, Magic Write, Canva Sheets, Magic Charts) that all follow
the same pattern: take something that used to require manual design work
and make it one click inside the editor. Magic Trends applies that same
pattern to a real, unsolved gap: aesthetic trends (fashion, interiors,
content culture) move in weeks, but template libraries move in quarters.
Small creators and brand accounts end up manually reverse-engineering a
trend's palette from a screenshot every single time.

This project is also a deliberate shift in format from the rest of this
portfolio: instead of a Streamlit tool, it's a real 5-page static website,
built to match the visual craft of an actual product launch page (like
Canva's own newsroom), not a data app.

## Pages

1. **[index.html](index.html)** -- home, the pitch and a live-feeling moodboard teaser
2. **[how-it-works.html](how-it-works.html)** -- the real 4-step pipeline, including an honest note on why this never scrapes TikTok/Instagram/Pinterest (their terms of service prohibit it)
3. **[trends.html](trends.html)** -- the gallery: 6 real, currently-circulating aesthetic trends, each decomposed into an actual color palette
4. **[for-you.html](for-you.html)** -- split messaging for individual creators vs. brand accounts, with different real use cases for each
5. **[early-access.html](early-access.html)** -- a waitlist form and the "why this exists" note

## Design approach

Built around the actual subject instead of a generic SaaS template: the
product is about curating aesthetic trends into moodboards, so the site
itself *is* a moodboard -- rotated pinned cards, real color swatches with
hex values, an asymmetric collage layout instead of a centered hero.

- **Color:** near-black eggplant canvas (`#17131c`), dusty parchment paper (`#f3ece6`), hot magenta accent (`#ff4d8d`), amber secondary (`#ffb703`)
- **Type:** Fraunces (an expressive editorial serif) for display, Work Sans for body, IBM Plex Mono for swatch labels and hex codes
- **Layout:** an asymmetric pinboard collage with rotated cards, deliberately not centered or uniform

## Running it

No build step -- it's plain HTML/CSS/JS. Either open `index.html` directly,
or serve it locally:

```
python -m http.server 8000
```

Then visit `http://localhost:8000`.

## A note on the waitlist form

The email form on the early-access page is a front-end-only demo -- no
email is actually collected or sent anywhere. It exists to show the
interaction, not to run a real mailing list.
