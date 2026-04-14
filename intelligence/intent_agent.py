from __future__ import annotations

import re
from typing import Any, Dict, List

from utils.llm_json import call_llm_json


_ALLOWED_REPORT_TYPES = {
    "trade_lookup",
    "exception_report",
    "t1_sweep",
    "compliance_summary",
    "hitl_review",
    "execution_report",
}


def _keyword_intent(query: str) -> Dict[str, Any]:
    q = (query or "").lower()

    report_type = "trade_lookup"
    sources: List[str] = ["inmemory", "bigquery"]

    if any(k in q for k in ["exception", "failed", "failures", "breach", "violations"]):
        report_type = "exception_report"
        sources = ["bigquery"]

    elif "t+1" in q or "t1" in q or "overdue" in q:
        report_type = "t1_sweep"
        sources = ["bigquery"]

    elif any(k in q for k in ["summary", "trend", "count", "how many"]):
        report_type = "compliance_summary"
        sources = ["bigquery"]

    elif any(k in q for k in ["hitl", "review", "approve", "reject", "modify"]):
        report_type = "hitl_review"
        sources = ["bigquery"]

    elif any(k in q for k in ["execution", "executed", "fill", "matched"]):
        report_type = "execution_report"
        sources = ["bigquery"]

    def _extract(pattern: str) -> str | None:
        m = re.search(pattern, query or "", flags=re.IGNORECASE)
        return m.group(1) if m else None

    trade_id = _extract(r"\b(T\d{3,8})\b")
    isin = _extract(r"\b([A-Z]{2}[A-Z0-9]{9}\d)\b")
    venue = _extract(r"\b(XNAS|XETR|XLON|XAMS|XMIL|BATS)\b")
    status = _extract(r"\b(NEWT|AMND|CANC|PASS|FAIL|HITL)\b")
    execution_id = _extract(r"\b(EXE-\d+)\b")

    date_window = ""
    if "today" in q:
        date_window = "today"
    elif "yesterday" in q:
        date_window = "yesterday"
    elif "last 7 days" in q or "past 7 days" in q:
        date_window = "last_7_days"
    elif "this month" in q:
        date_window = "this_month"
    elif "last month" in q:
        date_window = "last_month"

    return {
        "report_type": report_type,
        "filters": {
            "trade_id": trade_id,
            "isin": isin,
            "venue": venue,
            "status": status,
            "execution_id": execution_id,
            "date_window": date_window,
        },
        "data_sources_needed": sources,
        "reasoning": "Heuristic intent classification based on keywords and extracted identifiers.",
        "confidence": 0.72,
    }


def intent_agent(query: str) -> Dict[str, Any]:
    """
    Classify the auditor query into a structured intent object.

    This function is conservative:
    - it uses heuristics first
    - then lets the LLM refine
    - then applies hard safety normalization
    """
    fallback = _keyword_intent(query)

    prompt = f"""
You are a MiFID II regulatory reporting assistant.

Classify the auditor query and return JSON only.

Auditor query:
{query}

Return JSON with:
{{
  "report_type": "trade_lookup | exception_report | t1_sweep | compliance_summary | hitl_review | execution_report",
  "filters": {{
    "trade_id": null,
    "isin": null,
    "venue": null,
    "status": null,
    "execution_id": null,
    "date_window": "today | yesterday | last_7_days | this_month | last_month | empty"
  }},
  "data_sources_needed": ["inmemory", "bigquery"],
  "reasoning": "",
  "confidence": 0.0
}}
""".strip()

    try:
        result, _ = call_llm_json(prompt, fallback, retries=2)

        if not isinstance(result, dict):
            return fallback

        report_type = str(result.get("report_type") or fallback["report_type"]).strip()
        if report_type not in _ALLOWED_REPORT_TYPES:
            report_type = fallback["report_type"]

        filters = result.get("filters") or fallback["filters"]
        if not isinstance(filters, dict):
            filters = fallback["filters"]

        sources = result.get("data_sources_needed") or fallback["data_sources_needed"]
        if not isinstance(sources, list):
            sources = fallback["data_sources_needed"]

        sources = [s for s in sources if s in {"inmemory", "bigquery"}]
        if not sources:
            sources = fallback["data_sources_needed"]

        confidence = result.get("confidence", fallback["confidence"])
        try:
            confidence = max(0.0, min(1.0, float(confidence)))
        except Exception:
            confidence = fallback["confidence"]

        return {
            "report_type": report_type,
            "filters": filters,
            "data_sources_needed": sources,
            "reasoning": result.get("reasoning") or fallback["reasoning"],
            "confidence": confidence,
        }

    except Exception:
        return fallback