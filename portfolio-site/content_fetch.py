import json
import os
from pathlib import Path

import requests

CONFIG_FILE = Path(__file__).parent / "contentful_config.json"
OUTPUT_DIR = Path(__file__).parent / "content" / "articles"


def _load_config():
    space_id = os.environ.get("CONTENTFUL_SPACE_ID")
    access_token = os.environ.get("CONTENTFUL_ACCESS_TOKEN")
    if space_id and access_token:
        return {"space_id": space_id, "access_token": access_token}

    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, encoding="utf-8") as f:
            return json.load(f)

    return None


def fetch_projects(config: dict) -> list:
    url = f"https://cdn.contentful.com/spaces/{config['space_id']}/environments/master/entries"
    params = {"access_token": config["access_token"], "content_type": "project"}
    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    return response.json()["items"]


def write_markdown(entry: dict) -> None:
    fields = entry["fields"]
    slug = fields["slug"]
    lines = [
        f"Title: {fields['title']}",
        f"Date: {fields.get('date', '')}",
        f"Slug: {slug}",
        f"Tags: {', '.join(fields.get('tags', []))}",
        f"Summary: {fields.get('summary', '')}",
        "",
        fields.get("body", ""),
    ]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / f"{slug}.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = _load_config()
    if not config:
        print("No Contentful credentials found -- using existing local content/ files as-is.")
        return

    try:
        projects = fetch_projects(config)
    except requests.RequestException as exc:
        print(f"Could not reach Contentful ({exc}) -- using existing local content/ files as-is.")
        return

    for entry in projects:
        write_markdown(entry)

    print(f"Fetched {len(projects)} project(s) from Contentful.")


if __name__ == "__main__":
    main()
