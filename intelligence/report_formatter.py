from __future__ import annotations

import json
from typing import Any, Dict, List

from utils.llm_json import call_llm_json


def _safe_str(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        try:
            return json.dumps(value, ensure_ascii=False)
        except Exception:
            return str(value)
    return str(value)


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def _summarize_issues(final_trades: List[dict], hitl_queue: List[dict], limit: int = 8) -> List[str]:
    issues: List[str] = []

    for trade in final_trades[:5]:
        if not isinstance(trade, dict):
            continue
        trade_id = _safe_str(trade.get("trade_id") or "UNKNOWN")
        status = _safe_str(trade.get("final_status") or "UNKNOWN")
        reason = _safe_str(trade.get("decision_reason") or trade.get("summary") or "")
        if reason:
            issues.append(f"{trade_id}: {status} — {reason}")
        else:
            issues.append(f"{trade_id}: {status}")

    for item in hitl_queue[:3]:
        if not isinstance(item, dict):
            continue
        trade_id = _safe_str(item.get("trade_id") or "UNKNOWN")
        reason = _safe_str(item.get("reason") or item.get("decision_reason") or "")
        if reason:
            issues.append(f"HITL {trade_id}: {reason}")
        else:
            issues.append(f"HITL {trade_id}")

    # Deduplicate while preserving order
    deduped: List[str] = []
    seen = set()
    for issue in issues:
        if issue not in seen:
            seen.add(issue)
            deduped.append(issue)

    return deduped[:limit]


def _build_fallback_narrative(
    original_query: str,
    stats: Dict[str, Any],
    final_trades: List[dict],
    hitl_queue: List[dict],
    corrections: List[dict],
) -> str:
    total = _safe_int(stats.get("total"), len(final_trades))
    passed = _safe_int(stats.get("passed"), 0)
    hitl = _safe_int(stats.get("hitl"), len(hitl_queue))
    failed = _safe_int(stats.get("fail"), stats.get("failed", 0))
    auto_fixed = _safe_int(stats.get("auto_fixed"), len(corrections))

    parts = [
        f"Query processed successfully: {original_query}",
        f"Total trades analyzed: {total}",
        f"Passed: {passed}",
        f"Requires human review: {hitl}",
        f"Failed: {failed}",
        f"Auto-corrected: {auto_fixed}",
    ]

    if hitl:
        parts.append("Review the HITL queue for borderline or ambiguous cases.")
    if failed:
        parts.append("Review failed trades for rule breaches before submission.")
    if auto_fixed:
        parts.append("Auto-fixes were applied during enrichment and should be audited.")

    return " ".join(parts)


def report_formatter(original_query: str, pipeline_result: Dict[str, Any]) -> str:
    """
    Convert pipeline output into a concise auditor-friendly narrative.

    This is intentionally LLM-assisted for readability, but it remains bounded by:
    - pipeline stats
    - final trade outcomes
    - HITL queue
    - correction records
    """
    stats = pipeline_result.get("stats", {}) or {}
    final_trades = pipeline_result.get("final_trades", []) or []
    hitl_queue = pipeline_result.get("hitl_queue", []) or []
    corrections = pipeline_result.get("corrections", []) or []
    source_breakdown = pipeline_result.get("source_breakdown", {}) or {}
    intent = pipeline_result.get("intent", {}) or {}
    plan = pipeline_result.get("plan", {}) or {}

    top_issues = _summarize_issues(final_trades, hitl_queue, limit=8)

    total = _safe_int(stats.get("total"), len(final_trades))
    passed = _safe_int(stats.get("passed"), 0)
    hitl = _safe_int(stats.get("hitl"), len(hitl_queue))
    failed = _safe_int(stats.get("fail"), stats.get("failed", 0))
    auto_fixed = _safe_int(stats.get("auto_fixed"), len(corrections))

    prompt = f"""
You are writing to a senior MiFID II auditor.

Original auditor question:
{original_query}

Intent:
{_safe_str(intent)}

Execution plan:
{_safe_str(plan)}

Pipeline statistics:
- Total trades analyzed: {total}
- Passed: {passed}
- HITL required: {hitl}
- Failed: {failed}
- Auto-fixed: {auto_fixed}

Source breakdown:
{_safe_str(source_breakdown)}

Top issues:
{json.dumps(top_issues, indent=2, ensure_ascii=False)}

Corrections:
{json.dumps(corrections[:10], indent=2, ensure_ascii=False)}

Write a professional answer in plain English.
Requirements:
1. Directly answer the auditor's question.
2. Mention the outcome clearly.
3. Highlight any critical exceptions or HITL items.
4. Mention whether auto-corrections were applied.
5. State what action is needed next.
6. Keep it under 220 words.
7. Do not return JSON.
8. Do not mention internal code or technical implementation details.
""".strip()

    fallback_narrative = _build_fallback_narrative(
        original_query=original_query,
        stats=stats,
        final_trades=final_trades,
        hitl_queue=hitl_queue,
        corrections=corrections,
    )

    fallback = {"narrative": fallback_narrative}

    try:
        result, _ = call_llm_json(prompt, fallback, retries=2)

        if isinstance(result, dict):
            narrative = _safe_str(result.get("narrative")).strip()
            if narrative:
                return narrative

        return fallback_narrative

    except Exception:
        return fallback_narrative