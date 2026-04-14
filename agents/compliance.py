# import json
# from typing import Any, Dict, List

# from rag.retriever import search_rules
# from utils.llm_json import call_llm_json


# def _trade_view(trade: dict) -> dict:
#     normalized = trade.get("normalized_trade")
#     if isinstance(normalized, dict):
#         return normalized
#     return trade


# def _clamp01(value: Any, default: float = 0.0) -> float:
#     try:
#         return max(0.0, min(1.0, float(value)))
#     except Exception:
#         return max(0.0, min(1.0, default))


# def _rules_to_text(rule_docs: List[dict]) -> str:
#     if not rule_docs:
#         return ""
#     return "\n\n".join(
#         f"[score={r.get('score', 0)}] {r.get('text', '')}"
#         for r in rule_docs
#         if isinstance(r, dict)
#     )


# def _compute_rag_conf(rule_docs: List[dict]) -> float:
#     if not rule_docs:
#         return 0.3
#     scores = [_clamp01(r.get("score", 0.5), 0.5) for r in rule_docs if isinstance(r, dict)]
#     return round(sum(scores) / len(scores), 2) if scores else 0.3


# def _normalize_conf(conf: Any, rag_conf: float) -> float:
#     base = _clamp01(conf, 0.0)
#     rag = _clamp01(rag_conf, 0.3)
#     return round((base * 0.7) + (rag * 0.3), 2)


# def _clean_violations(value: Any) -> List[dict]:
#     if not isinstance(value, list):
#         return []
#     return [i for i in value if isinstance(i, dict)]


# def compliance_agent(state: dict) -> dict:
#     trades = state.get("enriched_trades", [])
#     results, logs, raw_outputs = [], [], []

#     if not isinstance(trades, list):
#         trades = []

#     for trade in trades:
#         if not isinstance(trade, dict):
#             continue

#         trade_id = trade.get("trade_id", "UNKNOWN")
#         trade_view = _trade_view(trade)

#         query = f"""
# compliance check for trade
# isin {trade_view.get('isin', '')}
# report_status {trade_view.get('report_status', '')}
# instrument_type {trade_view.get('instrument_type', '')}
# """.strip()

#         rule_docs = search_rules(query=query, rule_type="compliance", n_results=4)
#         rules_text = _rules_to_text(rule_docs)
#         rag_conf = _compute_rag_conf(rule_docs)

#         prompt = f"""
# You are MiFID II Compliance Agent.

# Assess the trade using ONLY the normalized trade data and retrieved rules.
# Do not hallucinate.
# Return JSON only.

# Trade (normalized preferred):
# {json.dumps(trade_view, indent=2, ensure_ascii=False)}

# Original trade:
# {json.dumps(trade, indent=2, ensure_ascii=False)}

# Rules:
# {rules_text if rules_text else "No retrieved rules"}

# Return JSON only:
# {{
#   "trade_id": "{trade_id}",
#   "compliant": true,
#   "confidence": 0.0,
#   "summary": "",
#   "violations": []
# }}
# """.strip()

#         fallback = {
#             "trade_id": trade_id,
#             "compliant": False,
#             "confidence": 0.0,
#             "summary": "fallback",
#             "violations": [],
#         }

#         result, raw = call_llm_json(prompt, fallback, retries=2)
#         raw_outputs.append({"trade_id": trade_id, "raw": raw})

#         if not isinstance(result, dict):
#             result = fallback

#         violations = _clean_violations(result.get("violations", []))
#         final_conf = _normalize_conf(result.get("confidence"), rag_conf)

#         results.append(
#             {
#                 "trade_id": trade_id,
#                 "compliant": bool(result.get("compliant", False)),
#                 "confidence": final_conf,
#                 "summary": result.get("summary", ""),
#                 "violations": violations,
#                 "rag_confidence": rag_conf,
#             }
#         )

#         logs.append(f"ComplianceAgent done {trade_id}")

#     return {
#         "compliance_results": results,
#         "compliance_raw_outputs": raw_outputs,
#         "agent_log": logs,
#     }



#-----------------------------------------------------------------------------------------


import json
from typing import Any, Dict, List

from rag.retriever import search_rules
from utils.llm_json import call_llm_json


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def _trade_view(trade: dict) -> dict:
    normalized = trade.get("normalized_trade")
    return normalized if isinstance(normalized, dict) else trade


def _clamp01(value: Any, default: float = 0.0) -> float:
    try:
        return max(0.0, min(1.0, float(value)))
    except Exception:
        return max(0.0, min(1.0, default))


def _rules_to_text(rule_docs: List[dict]) -> str:
    if not rule_docs:
        return ""
    return "\n\n".join(
        f"[score={r.get('score', 0)}] {r.get('text', '')}"
        for r in rule_docs if isinstance(r, dict)
    )


def _compute_rag_conf(rule_docs: List[dict]) -> float:
    if not rule_docs:
        return 0.3
    scores = [_clamp01(r.get("score", 0.5), 0.5) for r in rule_docs if isinstance(r, dict)]
    return round(sum(scores) / len(scores), 2)


def _normalize_conf(conf: Any, rag_conf: float) -> float:
    base = _clamp01(conf, 0.0)
    rag = _clamp01(rag_conf, 0.3)
    return round((base * 0.7) + (rag * 0.3), 2)


def _clean_violations(value: Any) -> List[dict]:
    if not isinstance(value, list):
        return []
    return [i for i in value if isinstance(i, dict)]


# ─────────────────────────────────────────────
# MAIN AGENT (RAG BASED)
# ─────────────────────────────────────────────

def compliance_agent(state: dict) -> dict:
    trades = state.get("enriched_trades", [])

    results, logs, raw_outputs = [], [], []

    if not isinstance(trades, list):
        trades = []

    for trade in trades:
        if not isinstance(trade, dict):
            continue

        trade_id = trade.get("trade_id", "UNKNOWN")
        trade_view = _trade_view(trade)

        # 🔍 RAG SEARCH
        query = f"""
MiFID II compliance check
isin {trade_view.get('isin', '')}
report_status {trade_view.get('report_status', '')}
instrument_type {trade_view.get('instrument_type', '')}
""".strip()

        rule_docs = search_rules(query=query, rule_type="compliance", n_results=5)
        rules_text = _rules_to_text(rule_docs)
        rag_conf = _compute_rag_conf(rule_docs)

        # 🧠 LLM DECISION
        prompt = f"""
You are MiFID II Compliance Agent.

Your job:
- Evaluate trade compliance
- Return PASS / HITL / FAIL
- Generate confidence aligned with decision

Rules:
PASS  = compliant → confidence 0.75–0.95
HITL  = uncertain → 0.40–0.74
FAIL  = non-compliant → 0.10–0.39

Trade:
{json.dumps(trade_view, indent=2)}

Rules:
{rules_text if rules_text else "No rules found"}

Return JSON only:
{{
  "trade_id": "{trade_id}",
  "compliance_status": "PASS | HITL | FAIL",
  "confidence": 0.0,
  "summary": "",
  "violations": []
}}
"""

        fallback = {
            "trade_id": trade_id,
            "compliance_status": "HITL",
            "confidence": 0.5,
            "summary": "Fallback compliance decision",
            "violations": [],
        }

        result, raw = call_llm_json(prompt, fallback, retries=2)
        raw_outputs.append({"trade_id": trade_id, "raw": raw})

        if not isinstance(result, dict):
            result = fallback

        final_conf = _normalize_conf(result.get("confidence"), rag_conf)

        results.append({
            "trade_id": trade_id,
            "compliance_status": result.get("compliance_status", "HITL"),
            "confidence": final_conf,
            "summary": result.get("summary", ""),
            "violations": _clean_violations(result.get("violations")),
            "rag_confidence": rag_conf,

            # ✅ NEW 
            "source_channel": trade.get("source_channel"), 
            "trace_id": trade.get("trace_id"),
        })

        logs.append(f"ComplianceAgent done {trade_id}")

    return {
        "compliance_results": results,
        "compliance_raw_outputs": raw_outputs,
        "agent_log": logs,
    }