# My Portfolio

A collection of small, real, working Python tools — each one built end to
end: a working app, tested against real input, and documented well enough
for someone else to run it. No project here is a mockup.

**Live showcase site:** https://s4239994.github.io/My-portfolio/

## Projects

| Project | What it does | Stack | Run it |
|---|---|---|---|
| [voice-meeting-summarizer](voice-meeting-summarizer/) | Upload a meeting recording, get a transcript, summary, and action items — fully offline | Python, Streamlit, Whisper | `streamlit run app.py` |
| [health-monitor](health-monitor/) | Live terminal dashboard for CPU, memory, disk, and local open ports | Python, psutil, Rich | `python monitor.py` |
| [invoice-generator](invoice-generator/) | Turns billable work into PDF invoices with automatic tax, discounts, and late fees | Python, fpdf2 | `python main.py` |
| [portfolio-site](portfolio-site/) | This showcase site itself — a static site generator with optional headless CMS support | Python, Pelican | `pelican content -s pelicanconf.py -o output -listen` |
| [support-bot](support-bot/) | AI customer support chatbot with sentiment detection and human hand-off, on a free local model | Python, Ollama, Streamlit | `streamlit run app.py` |
| [resume-screener](resume-screener/) | Scores a resume against a job description with exact + semantic skill matching and a concept graph | Python, spaCy, sentence-transformers | `streamlit run app.py` |
| [web-scraper-pipeline](web-scraper-pipeline/) | A streaming scrape → clean → store pipeline with robots.txt compliance built in | Python, requests, BeautifulSoup | `streamlit run app.py` |
| [signal-engine](signal-engine/) | AI lead enrichment & outreach pipeline — scores real company signals and drafts personalized openers | Python, Streamlit, Claude API | **[Live demo](https://my-portfolio-beazp4fzwcfb2jmyh9wypx.streamlit.app/)** |
| [vibe-check](vibe-check/) | Blunt AI "vibe check" for a company's careers page — scans for corporate-speak red flags and hands back a verdict quoting their own words | Python, Streamlit, Claude API | `streamlit run app.py` |
| [pulse-check](pulse-check/) | A 5-second emoji team check-in (instead of a long survey) with a live mood trend and an AI-written weekly manager briefing | Python, Streamlit, SQLite, Claude API | `streamlit run app.py` |
| [uvos](uvos/) | A Linux-desktop-styled sun exposure monitor using real live government UV data and real dermatological burn-time math | Python, Streamlit, SQLite, Claude API | `streamlit run app.py` |
| [magic-trends](magic-trends/) | A 5-page concept product site for Canva — turns real, currently-circulating aesthetic trends into ready-to-edit palettes and layout packs | HTML, CSS, JS | Open `index.html` |
| [shipped](shipped/) | A Rovo Agent concept for Atlassian — turns your Jira ticket history into a shareable, Spotify-Wrapped-style sprint recap | Python, Streamlit, Claude API | `streamlit run app.py` |
| [flow](flow/) | A 3D live venue capacity map concept for ROLLER — explore a whole theme park's wait times as an interactive 3D scene | Three.js, HTML, CSS, JS | Open `index.html` |
| [mixtape](mixtape/) | A genre hub of original mini-games — each genre inverts one core mechanic instead of cloning an existing game (Action is playable now; more genres in progress) | Java, Swing | `java -cp out Main` |

Each project is self-contained — its own `requirements.txt` (or, for
`magic-trends` and `flow`, no build step at all) and its own `README.md`
with full setup instructions. Most need no paid account or API key to run;
`signal-engine`, `vibe-check`, `pulse-check`, `uvos`, and `shipped` use the
Claude API for their AI writing step (a fraction of a cent per use), and
all five fall back to API-free functionality if you skip it.

## Design

Early projects share a dark terminal motif with a neon-green accent
(`#39FF88`). Later projects each get their own distinct visual identity
instead — `signal-engine` runs a charcoal-and-electric-blue theme,
`vibe-check` runs a Y2K brutalist "rubber stamp" look, `pulse-check` runs a
warm coral-and-navy look, `uvos` runs a Linux-desktop window aesthetic with
a boot sequence, `magic-trends` runs an editorial moodboard look (a
near-black canvas, a dusty-parchment card color, and a serif display face)
built specifically around what that product does, `shipped` runs a bold
indigo-and-orange "Wrapped card" look, and `flow` is a bright daytime 3D
scene instead of a flat page at all. Deliberate choice: every project
should look like its own thing, not a reskin of the last one.

## License

MIT — see [LICENSE](LICENSE).
