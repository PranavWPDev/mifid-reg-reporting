# import json
# from db.relational import SessionLocal, TradeEnriched, AuditLog
# from rag.retriever import search_isin, search_lei, search_rules
# from llm import call_llm


# def _safe_json_loads(text: str, fallback: dict) -> dict:
#     cleaned = (text or "").strip().replace("```json", "").replace("```", "").strip()
#     try:
#         return json.loads(cleaned)
#     except Exception:
#         return fallback


# def enrichment_agent(state: dict) -> dict:
#     run_id = state["run_id"]

#     # ✅ IMPORTANT FIX:
#     # If a trade was modified in HITL, reprocess the modified version first.
#     raw_trades = state.get("modified_trades") or state.get("raw_trades", [])

#     db = SessionLocal()
#     enriched_trades = []
#     logs = []

#     try:
#         for trade in raw_trades:
#             trade_id = trade.get("trade_id", "UNKNOWN")

#             isin = (trade.get("isin") or "").strip()
#             lei = (trade.get("executing_entity_lei") or "").strip()

#             isin_docs = search_isin(f"ISIN {isin}", n_results=2) if isin else []
#             lei_docs = search_lei(f"LEI {lei}", n_results=2) if lei else []
#             rule_docs = search_rules("MiFID II enrichment and reference data guidance", n_results=2)

#             print(f"\n🔍 DEBUG RAG for {trade_id}")
#             print("ISIN:", isin)
#             print("ISIN DOCS:", isin_docs)
#             print("LEI:", lei)
#             print("LEI DOCS:", lei_docs)

#             prompt = f"""
# You are the MiFID II Enrichment Agent.

# Goal:
# Enrich trade using ONLY provided RAG evidence.
# DO NOT hallucinate or invent any regulated data.

# Trade:
# {json.dumps(trade, indent=2)}

# ISIN Evidence:
# {json.dumps(isin_docs, indent=2)}

# LEI Evidence:
# {json.dumps(lei_docs, indent=2)}

# Rules:
# {json.dumps(rule_docs, indent=2)}

# Instructions:
# - Map ISIN → company name if found
# - Map LEI → legal entity name if found
# - If no evidence → return empty string
# - Always return valid JSON

# Return JSON:

# {{
#   "trade_id": "{trade_id}",
#   "enriched_fields": {{
#     "isin_reference": "",
#     "executing_entity_reference": "",
#     "notes": ""
#   }}
# }}
# """

#             fallback = {
#                 "trade_id": trade_id,
#                 "enriched_fields": {
#                     "isin_reference": isin_docs[0] if isin_docs else "",
#                     "executing_entity_reference": lei_docs[0] if lei_docs else "",
#                     "notes": "evidence-backed fallback enrichment",
#                 }
#             }

#             try:
#                 result = _safe_json_loads(call_llm(prompt, json_mode=True), fallback)
#             except Exception:
#                 result = fallback

#             enriched = dict(trade)
#             enriched_fields = result.get("enriched_fields", {}) or {}

#             for k, v in enriched_fields.items():
#                 if v not in ("", None):
#                     enriched[k] = v

#             enriched["enriched"] = True
#             enriched_trades.append(enriched)

#             db.add(TradeEnriched(
#                 run_id=run_id,
#                 trade_id=trade_id,
#                 enriched_json=json.dumps(enriched),
#             ))
#             db.add(AuditLog(
#                 run_id=run_id,
#                 trade_id=trade_id,
#                 agent="EnrichmentAgent",
#                 action="ENRICHED",
#                 detail=json.dumps(enriched_fields),
#             ))

#             logs.append(f"EnrichmentAgent completed for {trade_id}")

#         db.commit()

#         return {
#             "enriched_trades": enriched_trades,
#             "agent_log": logs,
#             "status": "reasoning",
#         }

#     except Exception:
#         db.rollback()
#         raise
#     finally:
#         db.close()


import json
from typing import Any, Dict, List

from db.relational import SessionLocal, TradeEnriched, AuditLog
from rag.retriever import search_isin, search_lei, search_rules
from utils.llm_json import call_llm_json


CANONICAL_KEYS = [
    "trade_id",
    "trade_datetime",
    "isin",
    "executing_entity_lei",
    "buyer_lei",
    "seller_lei",
    "price",
    "currency",
    "quantity",
    "venue",
    "notional_amount",
    "report_status",
    "instrument_type",
]


def _safe_dict(value: Any) -> Dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


def _build_canonical_template() -> Dict[str, str]:
    return {k: "" for k in CANONICAL_KEYS}


def _merge_non_empty(base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(base)
    for k, v in update.items():
        if v not in ("", None):
            merged[k] = v
    return merged


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def _derive_corrections(original_trade: dict, normalized_trade: dict) -> List[dict]:
    """
    Track any field that the enrichment model changed.
    This is the audit trail for auto-fixes.
    """
    corrections = []

    for key in CANONICAL_KEYS:
        if key == "trade_id":
            continue

        original_value = _stringify(original_trade.get(key, ""))
        normalized_value = _stringify(normalized_trade.get(key, ""))

        if original_value != normalized_value and normalized_value != "":
            corrections.append({
                "field": key,
                "old_value": original_value,
                "new_value": normalized_value,
                "source": "enrichment",
            })

    return corrections


def enrichment_agent(state: dict) -> dict:
    run_id = state["run_id"]

    # If HITL modified trades exist, process them first.
    raw_trades = state.get("modified_trades") or state.get("raw_trades", [])
    if not isinstance(raw_trades, list):
        raw_trades = []

    db = SessionLocal()
    enriched_trades = []
    all_corrections = []
    logs = []

    try:
        for trade in raw_trades:
            if not isinstance(trade, dict):
                continue

            trade_id = trade.get("trade_id", "UNKNOWN")

            isin_hint = (trade.get("isin") or trade.get("Instrument_Identification_Code") or "").strip()
            lei_hint = (trade.get("executing_entity_lei") or trade.get("Executing_Entity_Identification_Code") or "").strip()

            isin_docs = search_isin(f"ISIN {isin_hint}", n_results=2) if isin_hint else []
            lei_docs = search_lei(f"LEI {lei_hint}", n_results=2) if lei_hint else []
            rule_docs = search_rules("MiFID II enrichment and reference data guidance", n_results=2)

            prompt = f"""
You are the MiFID II Enrichment and Normalization Agent.

Goal:
1) Normalize the incoming trade into a canonical schema.
2) Enrich the trade using only provided evidence.

IMPORTANT:
- Do NOT invent data.
- If a canonical field cannot be mapped confidently, keep it as "".
- Preserve the original trade conceptually, but return a clean normalized_trade object.
- Treat notional_amount carefully: if you can infer a corrected value from the trade context, reflect that in normalized_trade and explain it in notes.
- Use ONLY the trade data and RAG evidence below.

Canonical schema for normalized_trade:
{json.dumps(_build_canonical_template(), indent=2, ensure_ascii=False)}

Input trade:
{json.dumps(trade, indent=2, ensure_ascii=False)}

ISIN evidence:
{json.dumps(isin_docs, indent=2, ensure_ascii=False)}

LEI evidence:
{json.dumps(lei_docs, indent=2, ensure_ascii=False)}

Rules:
{json.dumps(rule_docs, indent=2, ensure_ascii=False)}

Return JSON only:
{{
  "trade_id": "{trade_id}",
  "normalized_trade": {json.dumps(_build_canonical_template(), ensure_ascii=False)},
  "enriched_fields": {{
    "isin_reference": "",
    "executing_entity_reference": "",
    "notes": ""
  }},
  "notes": ""
}}
""".strip()

            fallback = {
                "trade_id": trade_id,
                "normalized_trade": _merge_non_empty(_build_canonical_template(), trade),
                "enriched_fields": {
                    "isin_reference": isin_docs[0] if isin_docs else "",
                    "executing_entity_reference": lei_docs[0] if lei_docs else "",
                    "notes": "fallback enrichment",
                },
                "notes": "fallback used",
            }

            result, raw = call_llm_json(prompt, fallback, retries=2)

            if not isinstance(result, dict):
                result = fallback

            normalized_trade = _safe_dict(result.get("normalized_trade"))
            if not normalized_trade:
                normalized_trade = _merge_non_empty(_build_canonical_template(), trade)

            normalized_trade = _merge_non_empty(_build_canonical_template(), normalized_trade)
            normalized_trade["trade_id"] = trade_id

            corrections = _derive_corrections(trade, normalized_trade)
            enriched_fields = _safe_dict(result.get("enriched_fields"))
            notes = _stringify(result.get("notes") or enriched_fields.get("notes") or "")

            enriched = dict(trade)

            # 🔥 ADD THIS AFTER: enriched = dict(trade) # ✅ PRESERVE SOURCE METADATA (CRITICAL) 
            for key in ["source_channel", "source_system", "source_ref", "batch_id", "received_at", "trace_id"]: 
                if key in trade: 
                    enriched[key] = trade[key]
            enriched["original_trade"] = trade
            enriched["normalized_trade"] = normalized_trade
            enriched = _merge_non_empty(enriched, normalized_trade)

            enriched["enriched"] = True
            enriched["auto_fix_applied"] = bool(corrections)
            enriched["auto_fix_status"] = "APPLIED" if corrections else "NONE"
            enriched["corrections"] = corrections
            enriched["enrichment_notes"] = notes

            enriched_trades.append(enriched)
            all_corrections.extend(
                [{"trade_id": trade_id, **c} for c in corrections]
            )

            db.add(
                TradeEnriched(
                    run_id=run_id,
                    trade_id=trade_id,
                    enriched_json=json.dumps(enriched, ensure_ascii=False),
                )
            )
            db.add(
                AuditLog(
                    run_id=run_id,
                    trade_id=trade_id,
                    agent="EnrichmentAgent",
                    action="ENRICHED",
                    detail=json.dumps(
                        {
                            "normalized_trade": normalized_trade,
                            "enriched_fields": enriched_fields,
                            "corrections": corrections,
                            "notes": notes,
                        },
                        ensure_ascii=False,
                    ),
                )
            )

            logs.append(f"EnrichmentAgent completed for {trade_id}")

        db.commit()

        return {
            "enriched_trades": enriched_trades,
            "corrections": all_corrections,
            "agent_log": logs,
            "status": "reasoning",
        }

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()