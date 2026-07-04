import json
import re
from pathlib import Path

import spacy
from spacy.matcher import PhraseMatcher

TAXONOMY_FILE = Path(__file__).parent / "data" / "skills_taxonomy.json"
EXPERIENCE_PATTERN = re.compile(r"(\d+)\+?\s*(?:years?|yrs?)\b", re.IGNORECASE)

_nlp = spacy.blank("en")


def load_taxonomy() -> dict:
    with open(TAXONOMY_FILE, encoding="utf-8") as f:
        return json.load(f)


def _all_skills(taxonomy: dict) -> list:
    skills = []
    for skill_list in taxonomy["categories"].values():
        skills.extend(skill_list)
    return skills


def extract_skills(text: str, taxonomy: dict) -> set:
    """Find every taxonomy skill mentioned in the text (case-insensitive, multi-word aware)."""
    skills = _all_skills(taxonomy)
    matcher = PhraseMatcher(_nlp.vocab, attr="LOWER")
    matcher.add("SKILLS", [_nlp.make_doc(skill) for skill in skills])

    doc = _nlp(text)
    matches = matcher(doc)

    lookup = {skill.lower(): skill for skill in skills}
    found = set()
    for _, start, end in matches:
        span_text = doc[start:end].text.lower()
        if span_text in lookup:
            found.add(lookup[span_text])
    return found


def extract_experience_years(text: str) -> int:
    """Return the largest 'N years' figure mentioned, or 0 if none found."""
    years = [int(m) for m in EXPERIENCE_PATTERN.findall(text)]
    return max(years) if years else 0


def skill_category(skill: str, taxonomy: dict) -> str:
    for category, skill_list in taxonomy["categories"].items():
        if skill in skill_list:
            return category
    return "Other"
