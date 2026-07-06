from typing import Iterator, Optional

import enrichment
import personalize
import scoring


def run_pipeline(leads: list, config: dict, client: Optional[object] = None) -> Iterator[dict]:
    """Stream one scored (and optionally personalized) lead at a time --
    fetch, score, and draft as it goes, instead of batching everything
    before showing any results."""
    for lead in leads:
        enriched = enrichment.enrich_company(lead["name"], lead["url"])
        result = scoring.score_lead(enriched, config)

        if client is not None:
            try:
                draft = personalize.draft_opener(client, result)
                result["opener"] = draft.opener
                result["signal_referenced"] = draft.signal_referenced
            except Exception as exc:
                result["opener"] = None
                result["signal_referenced"] = None
                result["reasons"].append(f"AI drafting failed: {exc}")
        else:
            result["opener"] = None
            result["signal_referenced"] = None

        yield result
