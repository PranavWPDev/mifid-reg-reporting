

# from __future__ import annotations

# import json
# from typing import Any, Dict, List

# from db.relational import SessionLocal, TradeValidated, ExceptionRecord, AuditLog
# from rag.retriever import search_rules
# from utils.llm_json import call_llm_json


# # =========================
# # CONFIG
# # =========================
# RAG_WEIGHT = 0.7
# LLM_WEIGHT = 0.3
# RAG_TOP_K = 6


# # =========================
# # HELPERS
# # =========================

# def _clamp01(v: Any, default: float = 0.0) -> float:
#     try:
#         return max(0.0, min(1.0, float(v)))
#     except Exception:
#         return max(0.0, min(1.0, default))


# def _safe_str(v: Any) -> str:
#     return "" if v is None else str(v).strip()


# def _rules_to_text(docs: List[dict]) -> str:
#     if not docs:
#         return ""
#     return "\n\n".join(
#         f"[score={r.get('score', 0):.3f}] {r.get('text', '')}"
#         for r in docs if isinstance(r, dict)
#     )


# # =========================
# # RAG CONFIDENCE
# # =========================

# def compute_rag_confidence(rule_docs: List[dict]) -> float:
#     if not rule_docs:
#         return 0.3

#     scores = [_clamp01(d.get("score", 0.3), 0.3) for d in rule_docs]
#     return round(sum(scores) / len(scores), 4)


# # =========================
# # LLM VALIDATION PROMPT
# # =========================

# VALIDATION_PROMPT = """
# You are a MiFID II Validation Agent.

# Your job is to validate a financial trade using ONLY:
# - Retrieved regulatory rules
# - Trade data

# DO NOT assume anything not present in rules.
# DO NOT hallucinate.

# For each issue:
# - Assign severity: LOW | MEDIUM | HIGH | CRITICAL

# Return JSON only:

# {
#   "trade_id": "",
#   "passed": true/false,
#   "confidence": 0.0,
#   "issues": [
#     {
#       "field": "",
#       "error": "",
#       "severity": ""
#     }
#   ],
#   "field_assessments": [
#     {
#       "field": "",
#       "status": "PASS | HITL | FAIL",
#       "confidence": 0.0,
#       "reason": "",
#       "evidence": []
#     }
#   ],
#   "summary": "",
#   "recommended_next_action": "PASS | HITL | FAIL"
# }
# """


# # =========================
# # TIER DERIVATION (AGENTIC)
# # =========================

# def derive_tier_from_llm(result: dict) -> str:
#     """
#     NO hardcoded MiFID rules.
#     Only interpret LLM output.
#     """
#     if result.get("passed") is True:
#         return "PASS"

#     issues = result.get("issues", [])
#     if not issues:
#         return "HITL"

#     severities = [i.get("severity", "").upper() for i in issues]

#     if "CRITICAL" in severities:
#         return "FAIL"

#     if "HIGH" in severities:
#         return "HITL"

#     return "HITL"


# # =========================
# # FINAL CONFIDENCE
# # =========================

# def blend_confidence(tier: str, rag_conf: float, llm_conf: float) -> float:
#     base = (RAG_WEIGHT * rag_conf) + (LLM_WEIGHT * llm_conf)

#     if tier == "PASS":
#         return round(min(max(base, 0.80), 0.97), 4)

#     if tier == "HITL":
#         return round(min(max(base, 0.50), 0.79), 4)

#     return round(min(max(base, 0.10), 0.49), 4)


# # =========================
# # MAIN AGENT
# # =========================

# def validation_agent(state: dict) -> dict:
#     run_id = state["run_id"]
#     trades = state.get("enriched_trades", [])

#     db = SessionLocal()

#     results = []
#     logs = []
#     raw_outputs = []

#     try:
#         for trade in trades:
#             if not isinstance(trade, dict):
#                 continue

#             trade_id = trade.get("trade_id", "UNKNOWN")

#             # =========================
#             # RAG Retrieval
#             # =========================
#             query = f"""
#             Validate MiFID II trade:
#             {json.dumps(trade, indent=2)}
#             """

#             rule_docs = search_rules(query=query, n_results=RAG_TOP_K)
#             rules_text = _rules_to_text(rule_docs)
#             rag_conf = compute_rag_confidence(rule_docs)

#             # =========================
#             # LLM Call
#             # =========================
#             prompt = f"""
# {VALIDATION_PROMPT}

# Trade:
# {json.dumps(trade, indent=2)}

# Rules:
# {rules_text}
# """

#             fallback = {
#                 "trade_id": trade_id,
#                 "passed": False,
#                 "confidence": 0.3,
#                 "issues": [{
#                     "field": "system",
#                     "error": "LLM failed",
#                     "severity": "HIGH"
#                 }],
#                 "field_assessments": [],
#                 "summary": "Validation failed due to system error.",
#                 "recommended_next_action": "HITL"
#             }

#             result, raw = call_llm_json(prompt, fallback, retries=2)
#             raw_outputs.append({"trade_id": trade_id, "raw": raw})

#             if not isinstance(result, dict):
#                 result = fallback

#             # =========================
#             # LLM Confidence
#             # =========================
#             llm_conf = _clamp01(result.get("confidence", 0.5), 0.5)

#             # =========================
#             # Tier
#             # =========================
#             tier = derive_tier_from_llm(result)

#             # =========================
#             # Final Confidence
#             # =========================
#             final_conf = blend_confidence(tier, rag_conf, llm_conf)

#             # =========================
#             # Final Output
#             # =========================
#             normalized = {
#                 "trade_id": trade_id,
#                 "passed": tier == "PASS",
#                 "decision_tier": tier,
#                 "confidence": final_conf,
#                 "rag_confidence": rag_conf,
#                 "llm_confidence": llm_conf,
#                 "summary": result.get("summary", ""),
#                 "issues": result.get("issues", []),
#                 "field_assessments": result.get("field_assessments", []),
#                 "recommended_next_action": tier,
#             }

#             results.append(normalized)

#             # =========================
#             # DB Writes
#             # =========================
#             db.add(TradeValidated(
#                 run_id=run_id,
#                 trade_id=trade_id,
#                 validated_json=json.dumps(normalized),
#                 passed=normalized["passed"]
#             ))

#             for issue in normalized["issues"]:
#                 db.add(ExceptionRecord(
#                     run_id=run_id,
#                     trade_id=trade_id,
#                     field=issue.get("field", ""),
#                     category="VALIDATION",
#                     severity=issue.get("severity", "HIGH"),
#                     description=issue.get("error", ""),
#                     status="OPEN"
#                 ))

#             db.add(AuditLog(
#                 run_id=run_id,
#                 trade_id=trade_id,
#                 agent="ValidationAgent",
#                 action="VALIDATED",
#                 detail=json.dumps({
#                     "rag_conf": rag_conf,
#                     "llm_conf": llm_conf,
#                     "final_conf": final_conf
#                 })
#             ))

#             logs.append(f"ValidationAgent done: {trade_id}")

#         db.commit()

#         return {
#             "validation_results": results,
#             "validation_raw_outputs": raw_outputs,
#             "agent_log": logs
#         }

#     except Exception:
#         db.rollback()
#         raise
#     finally:
#         db.close()

#------------------------------------------------------------------------
from __future__ import annotations

import json
from typing import Any, Dict, List

from db.relational import SessionLocal, TradeValidated, ExceptionRecord, AuditLog
from rag.retriever import search_rules
from utils.llm_json import call_llm_json

RAG_TOP_K = 6


def _json_safe(value):
    from datetime import date, datetime
    from decimal import Decimal

    if value is None:
        return None
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, dict):
        return {k: _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    return value


def validation_agent(state: dict) -> dict:
    run_id = state["run_id"]
    trades = state.get("enriched_trades", [])

    db = SessionLocal()
    results = []

    try:
        for trade in trades:
            trade_id = trade.get("trade_id", "UNKNOWN")

            safe_trade = _json_safe(trade)

            rule_docs = search_rules(
                query=json.dumps(safe_trade, indent=2),
                n_results=RAG_TOP_K,
            )

            prompt = f"""
Return STRICT VALID JSON only.
No markdown. No explanation.

Trade:
{json.dumps(safe_trade, indent=2)}

Return:
{{
  "trade_id": "{trade_id}",
  "passed": true,
  "confidence": 0.5,
  "issues": [],
  "summary": "",
  "recommended_next_action": "PASS"
}}
"""

            fallback = {
                "trade_id": trade_id,
                "passed": False,
                "confidence": 0.4,
                "issues": [{
                    "field": "system",
                    "error": "LLM failed — fallback used",
                    "severity": "MEDIUM"
                }],
                "summary": "Fallback validation applied",
                "recommended_next_action": "HITL",
            }

            result, _ = call_llm_json(prompt, fallback)

            results.append(result)

            db.add(TradeValidated(
                run_id=run_id,
                trade_id=trade_id,
                validated_json=json.dumps(result),
                passed=result.get("passed", False),
            ))

        db.commit()

        return {
            "validation_results": results,
        }

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

# from __future__ import annotations

# import json
# from typing import Any, Dict, List

# from db.relational import SessionLocal, TradeValidated, ExceptionRecord, AuditLog
# from rag.retriever import search_rules
# from utils.llm_json import call_llm_json


# RAG_TOP_K = 6


# # =========================
# # HELPERS
# # =========================
# def _clamp01(v: Any, default: float = 0.0) -> float:
#     try:
#         return max(0.0, min(1.0, float(v)))
#     except Exception:
#         return default


# def _safe_str(v: Any) -> str:
#     return "" if v is None else str(v)


# def _rules_to_text(docs: List[dict]) -> str:
#     if not docs:
#         return ""
#     return "\n\n".join(
#         f"[score={float(r.get('score', 0)):.3f}] {r.get('text', '')}"
#         for r in docs if isinstance(r, dict)
#     )


# def _clean_issues(value: Any) -> List[dict]:
#     if not isinstance(value, list):
#         return []
#     return [i for i in value if isinstance(i, dict)]


# def _severity_counts(issues: List[dict]) -> Dict[str, int]:
#     counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
#     for issue in issues:
#         sev = _safe_str(issue.get("severity", "")).upper()
#         if sev in counts:
#             counts[sev] += 1
#     return counts


# def compute_rag_confidence(rule_docs: List[dict]) -> float:
#     if not rule_docs:
#         return 0.3
#     scores = [_clamp01(d.get("score", 0.3), 0.3) for d in rule_docs if isinstance(d, dict)]
#     return round(sum(scores) / len(scores), 4) if scores else 0.3


# def _derive_tier(passed: bool, issues: List[dict]) -> str:
#     if passed and not issues:
#         return "PASS"

#     if not issues:
#         return "HITL"

#     counts = _severity_counts(issues)

#     if counts["CRITICAL"] >= 1:
#         return "FAIL"

#     if counts["HIGH"] >= 2:
#         return "FAIL"

#     if counts["HIGH"] >= 1 or counts["MEDIUM"] >= 1:
#         return "HITL"

#     return "PASS"


# def _confidence_from_tier(tier: str, rag_conf: float, llm_conf: float) -> float:
#     base = (rag_conf * 0.7) + (llm_conf * 0.3)

#     if tier == "PASS":
#         return round(min(max(0.75 + base * 0.2, 0.70), 0.95), 4)

#     if tier == "HITL":
#         return round(min(max(0.55 + base * 0.1, 0.40), 0.69), 4)

#     return round(min(max(0.25 + base * 0.05, 0.10), 0.39), 4)


# # =========================
# # MAIN AGENT
# # =========================
# def validation_agent(state: dict) -> dict:
#     run_id = state["run_id"]
#     trades = state.get("enriched_trades", [])

#     db = SessionLocal()
#     results = []
#     logs = []

#     try:
#         for trade in trades:
#             trade_id = trade.get("trade_id", "UNKNOWN")

#             # 🔍 RAG
#             rule_docs = search_rules(
#                 query=f"Validate trade {json.dumps(trade)}",
#                 n_results=RAG_TOP_K
#             )

#             rag_conf = compute_rag_confidence(rule_docs)

#             # 🧠 LLM
#             prompt = f"""
# Validate this MiFID II trade.

# Return JSON:
# {{
#   "passed": true,
#   "confidence": 0.0,
#   "issues": []
# }}
# Trade:
# {json.dumps(trade)}
# """

#             fallback = {
#                 "passed": False,
#                 "confidence": 0.3,
#                 "issues": [{
#                     "field": "system",
#                     "error": "Fallback triggered",
#                     "severity": "HIGH"
#                 }]
#             }

#             try:
#                 result, _ = call_llm_json(prompt, fallback, retries=2)
#             except Exception:
#                 result = fallback

#             if not isinstance(result, dict):
#                 result = fallback

#             issues = _clean_issues(result.get("issues", []))
#             passed = bool(result.get("passed", False))

#             llm_conf = _clamp01(result.get("confidence", 0.5), 0.5)

#             tier = _derive_tier(passed, issues)
#             final_conf = _confidence_from_tier(tier, rag_conf, llm_conf)

#             normalized = {
#                 "trade_id": trade_id,
#                 "passed": tier == "PASS",
#                 "decision_tier": tier,
#                 "confidence": final_conf,
#                 "rag_confidence": rag_conf,
#                 "llm_confidence": llm_conf,
#                 "issues": issues,
#                 "summary": _safe_str(result.get("summary", "")),

#                 # ✅ SAFE METADATA
#                 "source_channel": trade.get("source_channel", ""),
#                 "trace_id": trade.get("trace_id", ""),
#             }

#             results.append(normalized)

#             # ✅ DB SAFE INSERT
#             db.add(TradeValidated(
#                 run_id=run_id,
#                 trade_id=trade_id,
#                 validated_json=json.dumps(normalized, ensure_ascii=False),
#                 passed=normalized["passed"],
#             ))

#             for issue in issues:
#                 db.add(ExceptionRecord(
#                     run_id=run_id,
#                     trade_id=trade_id,
#                     field=_safe_str(issue.get("field")),
#                     category="VALIDATION",
#                     severity=_safe_str(issue.get("severity", "HIGH")),
#                     description=_safe_str(issue.get("error")),
#                     status="OPEN",
#                 ))

#             db.add(AuditLog(
#                 run_id=run_id,
#                 trade_id=trade_id,
#                 agent="ValidationAgent",
#                 action="VALIDATED",
#                 detail=json.dumps(normalized, ensure_ascii=False),
#             ))

#             logs.append(f"ValidationAgent done: {trade_id}")

#         db.commit()

#         return {
#             "validation_results": results,
#             "agent_log": logs,
#         }

#     except Exception:
#         db.rollback()
#         raise
#     finally:
#         db.close()