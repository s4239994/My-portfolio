import json
from pathlib import Path

CONFIG_FILE = Path(__file__).parent / "data" / "icp_config.json"


def load_icp_config() -> dict:
    with open(CONFIG_FILE, encoding="utf-8") as f:
        return json.load(f)


def score_lead(enriched: dict, config: dict) -> dict:
    """Blend detected signals into a 0-100 fit score using configurable
    weights -- an editable rules engine, not a hardcoded guess."""
    weights = config["weights"]

    matched_tech = [t for t in enriched["detected_tech"] if t in config["target_tech"]]
    text = f"{enriched['title']} {enriched['meta_description']}".lower()
    matched_keywords = [k for k in config["target_keywords"] if k.lower() in text]

    score = 0
    reasons = []

    if enriched["has_careers_page"]:
        score += weights["has_careers_page"]
        reasons.append("actively hiring (careers page found)")

    if matched_tech:
        score += weights["tech_match"] * len(matched_tech)
        reasons.append(f"uses {', '.join(matched_tech)}")

    if matched_keywords:
        score += weights["keyword_match"] * len(matched_keywords)
        reasons.append(f"matches target keywords: {', '.join(matched_keywords)}")

    if enriched.get("note"):
        reasons.append(enriched["note"])

    return {
        **enriched,
        "score": min(score, 100),
        "matched_tech": matched_tech,
        "matched_keywords": matched_keywords,
        "reasons": reasons,
    }
