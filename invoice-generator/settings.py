import json
from pathlib import Path

SETTINGS_FILE = Path(__file__).parent / "settings.json"


def load_settings() -> dict:
    with open(SETTINGS_FILE, encoding="utf-8") as f:
        return json.load(f)
