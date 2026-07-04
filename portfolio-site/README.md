# Portfolio Site (Static Site Generator + Headless CMS)

A fast, static portfolio website. Content is decoupled from design: pages are
written in Markdown (or pulled from a headless CMS), a Python static site
generator turns them into plain HTML/CSS, and GitHub Actions automatically
rebuilds and republishes the live site every time something changes.

## Stack

- **[Pelican](https://getpelican.com/)** — a static site generator written in
  Python (Markdown in, HTML out — no JavaScript build tooling required)
- **Contentful** (optional) — a free headless CMS; if configured, content is
  pulled from there instead of the local Markdown files
- **GitHub Pages + GitHub Actions** — free hosting with automatic build and
  deploy on every push (no separate hosting account needed)

## Running it locally

```
pip install -r requirements.txt
pelican content -s pelicanconf.py -o output -listen
```

Then open http://localhost:8000. `-listen` serves the `output/` folder; add
`-r` (`pelican content -r -listen`) to auto-rebuild whenever you edit a file.

## Adding a project

Drop a new Markdown file in `content/articles/`:

```
Title: My New Project
Date: 2026-08-01
Tags: python, cli
Summary: One sentence describing it.

Full writeup goes here in Markdown.
```

It'll appear automatically on the homepage the next time the site builds.

## Adding a static page

Same idea, but in `content/pages/` (see `about.md` for an example). Set a
`Slug:` field to control its URL.

## Connecting the headless CMS (optional)

By default the site builds from the local Markdown files above — you don't
need Contentful at all to use this. To pull content from Contentful instead:

1. Create a free account at https://www.contentful.com/ and a new Space
2. Create a content type called `project` with fields: `title` (short text),
   `slug` (short text), `date` (date), `tags` (short text, list),
   `summary` (short text), `body` (long text, written in Markdown)
3. Go to Settings → API keys → add an API key, and note the **Space ID** and
   **Content Delivery API access token**
4. Copy `contentful_config.example.json` to `contentful_config.json` and fill
   in those two values (this file is git-ignored, it never gets committed)
5. Run `python content_fetch.py` before building — it overwrites
   `content/articles/` with whatever's published in Contentful

## Auto-deploy on every push

`.github/workflows/deploy-portfolio.yml` (at the repo root) rebuilds and
republishes the site automatically whenever anything under `portfolio-site/`
changes on the `main` branch. The very first time, you need to turn on GitHub
Pages for the repo:

1. On GitHub, go to the repo's **Settings → Pages**
2. Under **Build and deployment → Source**, choose **GitHub Actions**

After that, every `git push` rebuilds and republishes the live site within a
minute or two — no manual deploy step, ever.

### Making Contentful trigger a deploy too (optional)

If you're using Contentful, you can make *publishing content* also trigger a
rebuild, without touching any code:

1. In GitHub, create a Personal Access Token with `repo` scope (Settings →
   Developer settings → Personal access tokens)
2. In Contentful, go to Settings → Webhooks → Add webhook
   - URL: `https://api.github.com/repos/s4239994/My-portfolio/dispatches`
   - Method: POST
   - Headers: `Authorization: Bearer <your GitHub token>`,
     `Accept: application/vnd.github+json`
   - Content: custom payload `{"event_type": "contentful-publish"}`
   - Trigger: on Entry publish

Now editing content in Contentful and hitting "Publish" rebuilds the live
site automatically, with zero code changes.
