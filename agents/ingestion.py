# import csv
# import io
# import json
# import uuid
# from typing import Any, Dict, List

# from llm import call_llm
# from db.relational import SessionLocal, TradeRaw, AuditLog


# def _safe_json_loads(text: str, fallback: Dict[str, Any]) -> Dict[str, Any]:
#     cleaned = (text or "").strip().replace("```json", "").replace("```", "").strip()
#     try:
#         return json.loads(cleaned)
#     except Exception:
#         return fallback


# def ingestion_agent(state: dict) -> dict:
#     run_id = state["run_id"]
#     raw_input = state.get("raw_input")
#     db = SessionLocal()

#     trades: List[dict] = []

#     try:
#         if isinstance(raw_input, list):
#             trades = [dict(t) for t in raw_input if isinstance(t, dict)]

#         elif isinstance(raw_input, dict):
#             trades = [dict(raw_input)]

#         elif isinstance(raw_input, str):
#             text = raw_input.strip().lstrip("\ufeff")

#             if text.startswith("{") or text.startswith("["):
#                 try:
#                     parsed = json.loads(text)
#                     if isinstance(parsed, list):
#                         trades = [dict(t) for t in parsed if isinstance(t, dict)]
#                     elif isinstance(parsed, dict):
#                         trades = [parsed]
#                 except Exception:
#                     trades = []

#             elif "\n" in text and "," in text:
#                 reader = csv.DictReader(io.StringIO(text))
#                 trades = [dict(row) for row in reader]

#         if not trades:
#             return {
#                 "raw_trades": [],
#                 "agent_log": ["IngestionAgent found no trades"],
#                 "status": "enriching",
#             }

#         # ✅ FIX: use sample instead of undefined 'trade'
#         sample = trades[:3]

#         prompt = f"""
# You are an Ingestion Agent for MiFID II trade reporting.

# Task:
# - Normalize input trade data into structured format
# - Ensure all required fields are present
# - If field missing, keep empty string
# - If report_status missing → set "NEW"
# Sample Trade Input:
# {json.dumps(sample, indent=2)}

# Return JSON:

# {{
#   "field_mapping": {{
#     "input_field_name": "standard_field_name"
#   }},
#   "notes": "optional notes"
# }}
# """

#         fallback = {"field_mapping": {}, "notes": "schema inference fallback"}

#         try:
#             schema = _safe_json_loads(call_llm(prompt, json_mode=True), fallback)
#         except Exception as e:
#             schema = fallback
#             schema["notes"] = f"schema inference failed: {e}"

#         field_map = schema.get("field_mapping", {}) or {}

#         normalized_trades = []
#         logs = [f"IngestionAgent parsed {len(trades)} raw trades"]

#         for row in trades:
#             normalized = {}
#             for k, v in row.items():
#                 key = field_map.get(k, k)
#                 normalized[key] = "" if v is None else str(v).strip()

#             original_trade_id = normalized.get("trade_id") or f"TRD-{uuid.uuid4().hex[:6].upper()}"
#             trade_id = f"{run_id}-{original_trade_id}"
#             normalized["trade_id"] = trade_id
#             normalized["_original_trade_id"] = original_trade_id

#             normalized_trades.append(normalized)

#             db.add(TradeRaw(
#                 run_id=run_id,
#                 trade_id=trade_id,
#                 raw_json=json.dumps(normalized),
#             ))
#             db.add(AuditLog(
#                 run_id=run_id,
#                 trade_id=trade_id,
#                 agent="IngestionAgent",
#                 action="INGESTED",
#                 detail="LLM schema understanding completed",
#             ))

#         db.commit()

#         return {
#             "raw_trades": normalized_trades,
#             "ingestion_metadata": schema,
#             "agent_log": logs + [f"IngestionAgent completed with {len(normalized_trades)} trades"],
#             "status": "enriching",
#         }

#     except Exception:
#         db.rollback()
#         raise
#     finally:
#         db.close()

# agents/ingestion.py

import csv
import io
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List

from llm import call_llm
from db.relational import SessionLocal, TradeRaw, AuditLog


# ─── INTERNAL FIELDS that must never be treated as MiFID trade fields ─────────
_META_KEYS = {
    "_source", "_source_label", "_source_ref",
    "source_channel", "source_system", "source_ref",
    "batch_id", "received_at", "trace_id",
    "_original_trade_id",
}


def _safe_json_loads(text: str, fallback: Dict[str, Any]) -> Dict[str, Any]:
    cleaned = (text or "").strip().replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(cleaned)
    except Exception:
        return fallback


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_raw_input(raw_input: Any) -> List[dict]:
    """
    Accepts:
    - list of trade dicts              ← primary path (from data_sources.py)
    - dict with trade_data / trades    ← API envelope path
    - single trade dict                ← single trade path
    - JSON string                      ← raw paste from UI
    - CSV string                       ← CSV paste from UI
    """
    trades: List[dict] = []

    if isinstance(raw_input, list):
        trades = [dict(t) for t in raw_input if isinstance(t, dict)]

    elif isinstance(raw_input, dict):
        if isinstance(raw_input.get("trade_data"), list):
            trades = [dict(t) for t in raw_input["trade_data"] if isinstance(t, dict)]
        elif isinstance(raw_input.get("trades"), list):
            trades = [dict(t) for t in raw_input["trades"] if isinstance(t, dict)]
        else:
            trades = [dict(raw_input)]

    elif isinstance(raw_input, str):
        text = raw_input.strip().lstrip("\ufeff")

        if text.startswith("{") or text.startswith("["):
            try:
                parsed = json.loads(text)
                if isinstance(parsed, list):
                    trades = [dict(t) for t in parsed if isinstance(t, dict)]
                elif isinstance(parsed, dict):
                    trades = [parsed]
            except Exception:
                trades = []

        elif "\n" in text and "," in text:
            reader = csv.DictReader(io.StringIO(text))
            trades = [dict(row) for row in reader]

    return trades


def _extract_source_meta(trade: dict, state: dict) -> dict:
    """
    Pull source metadata from the trade itself first (set by data_sources.py),
    then fall back to state-level metadata, then to sensible defaults.
    This means a trade tagged source_channel='in_memory_db' by data_sources.py
    keeps that tag even if state says 'ui'.
    """
    return {
        "source_channel": (
            trade.get("source_channel") or
            trade.get("_source") or
            state.get("source_channel") or
            "ui"
        ),
        "source_system": (
            trade.get("source_system") or
            state.get("source_system") or
            "react-ui"
        ),
        "source_ref": (
            trade.get("source_ref") or
            trade.get("_source_ref") or
            state.get("source_ref") or
            "manual"
        ),
        "source_label": (
            trade.get("_source_label") or
            trade.get("source_channel") or
            state.get("source_channel") or
            "UI"
        ),
        "batch_id": (
            trade.get("batch_id") or
            state.get("batch_id") or
            ""
        ),
        "received_at": (
            trade.get("received_at") or
            state.get("received_at") or
            _utc_now_iso()
        ),
    }


def ingestion_agent(state: dict) -> dict:
    run_id    = state["run_id"]
    raw_input = state.get("raw_input")
    db        = SessionLocal()

    try:
        trades = _parse_raw_input(raw_input)

        if not trades:
            return {
                "raw_trades": [],
                "agent_log": ["IngestionAgent: no trades found in input"],
                "status": "enriching",
            }

        # ── LLM schema inference on a small sample ─────────────────────────
        # Only pass MiFID-relevant fields to the LLM — strip meta keys so the
        # LLM does not try to "map" source_channel → some canonical field.
        sample_for_llm = []
        for t in trades[:3]:
            clean = {k: v for k, v in t.items() if k not in _META_KEYS}
            sample_for_llm.append(clean)

        prompt = f"""
You are an Ingestion Agent for MiFID II trade reporting.

Task: Normalize input trade data into the standard MiFID II schema.
- Map non-standard field names to canonical names (e.g. instrument_id → isin).
- If a field is already canonical, map it to itself.
- Only return the field_mapping dict.

Sample trades (3 records):
{json.dumps(sample_for_llm, indent=2)}

Return JSON only:
{{
  "field_mapping": {{
    "input_field_name": "canonical_field_name"
  }}
}}
"""
        schema    = _safe_json_loads(call_llm(prompt, json_mode=True), {"field_mapping": {}})
        field_map = schema.get("field_mapping") or {}

        normalized_trades: List[dict] = []
        logs: List[str] = []

        # Track unique source channels across this batch for the log
        seen_sources: set = set()

        for row in trades:
            # ── Extract source metadata BEFORE field mapping ────────────────
            meta = _extract_source_meta(row, state)
            seen_sources.add(meta["source_channel"])

            # ── Separate MiFID fields from internal meta fields ─────────────
            trade_fields = {k: v for k, v in row.items() if k not in _META_KEYS}

            # ── Apply LLM field mapping ─────────────────────────────────────
            normalized: Dict[str, Any] = {}
            for k, v in trade_fields.items():
                canonical_key = field_map.get(k, k)
                normalized[canonical_key] = "" if v in (None, "null", "None", "") else str(v).strip()

            # ── Assign trade ID ─────────────────────────────────────────────
            original_id = (
                normalized.get("trade_id") or
                row.get("trade_id") or
                f"T-{uuid.uuid4().hex[:6].upper()}"
            )
            trade_id = f"{run_id}-{original_id}"

            normalized["trade_id"]          = trade_id
            normalized["_original_trade_id"] = original_id

            # ── Re-attach source metadata (preserved, not mapped by LLM) ───
            normalized["source_channel"] = meta["source_channel"]
            normalized["source_system"]  = meta["source_system"]
            normalized["source_ref"]     = meta["source_ref"]
            normalized["source_label"]   = meta["source_label"]
            normalized["batch_id"]       = meta["batch_id"]
            normalized["received_at"]    = meta["received_at"]
            normalized["trace_id"]       = f"{meta['batch_id']}-{original_id}" if meta["batch_id"] else original_id

            normalized_trades.append(normalized)

            # ── Persist to DB ───────────────────────────────────────────────
            db.add(TradeRaw(
                run_id=run_id,
                trade_id=trade_id,
                raw_json=json.dumps(normalized, ensure_ascii=False),
            ))

            db.add(AuditLog(
                run_id=run_id,
                trade_id=trade_id,
                agent="IngestionAgent",
                action="INGESTED",
                detail=json.dumps({
                    "source_channel": meta["source_channel"],
                    "source_system":  meta["source_system"],
                    "source_label":   meta["source_label"],
                    "source_ref":     meta["source_ref"],
                    "batch_id":       meta["batch_id"],
                    "trace_id":       normalized["trace_id"],
                    "original_trade_id": original_id,
                }, ensure_ascii=False),
            ))

        db.commit()

        # ── Build human-readable log entries ────────────────────────────────
        logs.append(f"IngestionAgent: parsed {len(normalized_trades)} trade(s)")
        for src in sorted(seen_sources):
            count = sum(1 for t in normalized_trades if t.get("source_channel") == src)
            logs.append(f"  Source [{src.upper()}]: {count} trade(s) received")

        return {
            "raw_trades": normalized_trades,
            "agent_log":  logs,
            "status":     "enriching",
        }

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()