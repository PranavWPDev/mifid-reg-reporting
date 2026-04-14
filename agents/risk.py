# # import json
# # from typing import Any, Dict, List

# # from rag.retriever import search_rules
# # from llm import call_llm
# # from utils.json_tools import extract_json_object


# # def _safe_float(value: Any, default: float = 0.0) -> float:
# #     try:
# #         return float(value)
# #     except Exception:
# #         return default


# # def _clamp01(value: Any, default: float = 0.0) -> float:
# #     try:
# #         return max(0.0, min(1.0, float(value)))
# #     except Exception:
# #         return max(0.0, min(1.0, default))


# # def _rules_to_text(rule_docs: List[dict]) -> str:
# #     if not rule_docs:
# #         return ""
# #     return "\n\n".join(
# #         f"[score={r.get('score', 0)}] {r.get('text', '')}"
# #         for r in rule_docs
# #         if isinstance(r, dict)
# #     )


# # def _compute_rag_conf(rule_docs: List[dict]) -> float:
# #     if not rule_docs:
# #         return 0.3
# #     scores = []
# #     for r in rule_docs:
# #         if isinstance(r, dict):
# #             scores.append(_clamp01(r.get("score", 0.5), 0.5))
# #     if not scores:
# #         return 0.3
# #     return round(sum(scores) / len(scores), 2)


# # def _normalize_conf(conf: Any, rag_conf: float) -> float:
# #     base = _clamp01(conf, 0.0)
# #     rag_conf = _clamp01(rag_conf, 0.3)
# #     return round((base * 0.7) + (rag_conf * 0.3), 2)


# # def _deterministic_risk_assessment(trade: dict) -> dict:
# #     """
# #     Safe baseline when LLM/rules are weak or unavailable.
# #     This does not replace the LLM; it prevents nonsense outputs.
# #     """
# #     drivers = []
# #     risk_score = 0

# #     price = _safe_float(trade.get("price"), 0.0)
# #     qty = _safe_float(trade.get("quantity"), 0.0)
# #     notional = _safe_float(trade.get("notional_amount"), 0.0)
# #     currency = str(trade.get("currency", "")).upper().strip()
# #     venue = str(trade.get("venue", "")).upper().strip()
# #     isin = str(trade.get("isin", "")).strip()
# #     executing_lei = str(trade.get("executing_entity_lei", "")).strip()
# #     buyer_lei = str(trade.get("buyer_lei", "")).strip()
# #     seller_lei = str(trade.get("seller_lei", "")).strip()
# #     report_status = str(trade.get("report_status", "")).upper().strip()

# #     if price <= 0:
# #         risk_score += 3
# #         drivers.append("Non-positive price")
# #     if qty <= 0:
# #         risk_score += 3
# #         drivers.append("Non-positive quantity")
# #     if notional and abs((price * qty) - notional) > 0.01:
# #         risk_score += 2
# #         drivers.append("Notional mismatch")
# #     if buyer_lei and seller_lei and buyer_lei == seller_lei:
# #         risk_score += 3
# #         drivers.append("Potential wash trade")
# #     if not isin or len(isin) != 12:
# #         risk_score += 3
# #         drivers.append("Invalid ISIN")
# #     if not executing_lei or len(executing_lei) != 20:
# #         risk_score += 3
# #         drivers.append("Invalid executing LEI")
# #     if currency not in {"USD", "EUR", "GBP", "JPY", "CHF", "INR"}:
# #         risk_score += 1
# #         drivers.append("Unknown currency")
# #     if not venue.startswith("X") or len(venue) < 4:
# #         risk_score += 1
# #         drivers.append("Unknown venue")
# #     if report_status not in {"NEWT", "AMND", "CANC"}:
# #         risk_score += 2
# #         drivers.append("Invalid report status")

# #     if risk_score >= 6:
# #         level = "HIGH"
# #     elif risk_score >= 3:
# #         level = "MEDIUM"
# #     else:
# #         level = "LOW"

# #     return {
# #         "risk_level": level,
# #         "summary": "Deterministic risk baseline applied.",
# #         "drivers": drivers,
# #     }


# # def risk_agent(state: dict) -> dict:
# #     trades = state.get("enriched_trades", [])
# #     results, logs, raw_outputs = [], [], []

# #     if not isinstance(trades, list):
# #         trades = []

# #     for trade in trades:
# #         if not isinstance(trade, dict):
# #             continue

# #         trade_id = trade.get("trade_id", "UNKNOWN")

# #         query = (
# #             f"risk analysis for trade quantity {trade.get('quantity')} "
# #             f"price {trade.get('price')} isin {trade.get('isin')}"
# #         )
# #         rule_docs = search_rules(query=query, rule_type="risk", n_results=4)

# #         rules_text = _rules_to_text(rule_docs)
# #         rag_conf = _compute_rag_conf(rule_docs)

# #         fallback = {
# #             "trade_id": trade_id,
# #             "risk_level": "HIGH",
# #             "confidence": 0.0,
# #             "summary": "fallback",
# #             "drivers": [],
# #         }

# #         prompt = f"""
# # You are MiFID II Risk Agent.

# # STRICT:
# # - Use ONLY provided rules
# # - No hallucination
# # - Return valid JSON only

# # Trade:
# # {json.dumps(trade, indent=2, ensure_ascii=False)}

# # Rules:
# # {rules_text if rules_text else "No retrieved risk rules"}

# # Return JSON:
# # {{
# #   "trade_id": "{trade_id}",
# #   "risk_level": "LOW | MEDIUM | HIGH",
# #   "confidence": 0.0,
# #   "summary": "",
# #   "drivers": []
# # }}
# # """

# #         try:
# #             raw = call_llm(prompt, json_mode=True)
# #         except Exception as e:
# #             raw = ""
# #             logs.append(f"RiskAgent LLM failed for {trade_id}: {e}")

# #         raw_outputs.append({"trade_id": trade_id, "raw": raw})

# #         result = extract_json_object(raw, {})
# #         if not isinstance(result, dict):
# #             result = {}

# #         deterministic = _deterministic_risk_assessment(trade)

# #         risk_level = str(result.get("risk_level") or deterministic["risk_level"]).upper().strip()
# #         if risk_level not in {"LOW", "MEDIUM", "HIGH"}:
# #             risk_level = deterministic["risk_level"]

# #         summary = result.get("summary") or deterministic["summary"]

# #         drivers = result.get("drivers")
# #         if not isinstance(drivers, list) or not drivers:
# #             drivers = deterministic["drivers"]

# #         final_conf = _normalize_conf(result.get("confidence", 0.0), rag_conf)

# #         # Make obviously risky trades show a meaningful confidence floor
# #         if risk_level == "HIGH":
# #             final_conf = max(final_conf, 0.79)
# #         elif risk_level == "MEDIUM":
# #             final_conf = max(final_conf, 0.55)
# #         else:
# #             final_conf = max(final_conf, 0.09)

# #         results.append({
# #             "trade_id": trade_id,
# #             "risk_level": risk_level,
# #             "confidence": final_conf,
# #             "summary": summary,
# #             "drivers": drivers,
# #             "rag_confidence": rag_conf,
# #         })

# #         logs.append(f"RiskAgent done {trade_id}")

# #     return {
# #         "risk_results": results,
# #         "risk_raw_outputs": raw_outputs,
# #         "agent_log": logs,
# #     }





# import json
# from typing import Any, List

# from rag.retriever import search_rules
# from utils.llm_json import call_llm_json


# def _safe_float(value: Any, default: float = 0.0) -> float:
#     try:
#         return float(value)
#     except Exception:
#         return default


# def _clamp01(value: Any, default: float = 0.0) -> float:
#     try:
#         return max(0.0, min(1.0, float(value)))
#     except Exception:
#         return max(0.0, min(1.0, default))


# def _rules_to_text(rule_docs: List[dict]) -> str:
#     return "\n\n".join(
#         f"[score={r.get('score', 0)}] {r.get('text', '')}"
#         for r in rule_docs
#         if isinstance(r, dict)
#     ) if rule_docs else ""


# def _compute_rag_conf(rule_docs: List[dict]) -> float:
#     if not rule_docs:
#         return 0.3
#     scores = [r.get("score", 0.5) for r in rule_docs if isinstance(r, dict)]
#     return round(sum(scores) / len(scores), 2) if scores else 0.3


# def _normalize_conf(conf: Any, rag_conf: float) -> float:
#     base = _clamp01(conf, 0.0)
#     rag_conf = _clamp01(rag_conf, 0.3)
#     return round((base * 0.7) + (rag_conf * 0.3), 2)


# def risk_agent(state: dict) -> dict:
#     trades = state.get("enriched_trades", [])
#     results, logs, raw_outputs = [], [], []

#     if not isinstance(trades, list):
#         trades = []

#     for trade in trades:
#         if not isinstance(trade, dict):
#             continue

#         trade_id = trade.get("trade_id", "UNKNOWN")

#         query = (
#             f"risk analysis for trade quantity {trade.get('quantity')} "
#             f"price {trade.get('price')} isin {trade.get('isin')}"
#         )
#         rule_docs = search_rules(query=query, rule_type="risk", n_results=4)

#         rules_text = _rules_to_text(rule_docs)
#         rag_conf = _compute_rag_conf(rule_docs)

#         prompt = f"""
# You are MiFID II Risk Agent.

# STRICT:
# - Use ONLY provided rules
# - No hallucination
# - Return JSON only
# - Do not add markdown
# - Do not truncate

# Trade:
# {json.dumps(trade, indent=2, ensure_ascii=False)}

# Rules:
# {rules_text if rules_text else "No retrieved risk rules"}

# Return JSON:
# {{
#   "trade_id": "{trade_id}",
#   "risk_level": "LOW | MEDIUM | HIGH",
#   "confidence": 0.0,
#   "summary": "",
#   "drivers": []
# }}
# """.strip()

#         fallback = {
#             "trade_id": trade_id,
#             "risk_level": "HIGH",
#             "confidence": 0.0,
#             "summary": "fallback",
#             "drivers": []
#         }

#         result, raw = call_llm_json(prompt, fallback, retries=2)
#         raw_outputs.append({"trade_id": trade_id, "raw": raw})

#         if not isinstance(result, dict):
#             result = fallback

#         risk_level = str(result.get("risk_level") or "HIGH").upper().strip()
#         if risk_level not in {"LOW", "MEDIUM", "HIGH"}:
#             risk_level = "HIGH"

#         drivers = result.get("drivers", [])
#         if not isinstance(drivers, list):
#             drivers = []

#         final_conf = _normalize_conf(result.get("confidence", 0.0), rag_conf)

#         if risk_level == "HIGH":
#             final_conf = max(final_conf, 0.79)
#         elif risk_level == "MEDIUM":
#             final_conf = max(final_conf, 0.55)
#         else:
#             final_conf = max(final_conf, 0.09)

#         results.append({
#             "trade_id": trade_id,
#             "risk_level": risk_level,
#             "confidence": final_conf,
#             "summary": result.get("summary", ""),
#             "drivers": drivers,
#             "rag_confidence": rag_conf,
#         })

#         logs.append(f"RiskAgent done {trade_id}")

#     return {
#         "risk_results": results,
#         "risk_raw_outputs": raw_outputs,
#         "agent_log": logs,
#     }

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


# def _clean_drivers(value: Any) -> List[dict]:
#     if not isinstance(value, list):
#         return []
#     return [i for i in value if isinstance(i, dict)]


# def risk_agent(state: dict) -> dict:
#     trades = state.get("enriched_trades", [])
#     results, logs, raw_outputs = [], [], []

#     if not isinstance(trades, list):
#         trades = []

#     for trade in trades:
#         if not isinstance(trade, dict):
#             continue

#         trade_id = trade.get("trade_id", "UNKNOWN")
#         trade_view = _trade_view(trade)

#         query = (
#             f"risk assessment for trade "
#             f"isin {trade_view.get('isin', '')} "
#             f"price {trade_view.get('price', '')} "
#             f"quantity {trade_view.get('quantity', '')} "
#             f"notional {trade_view.get('notional_amount', '')}"
#         )
#         rule_docs = search_rules(query=query, rule_type="risk", n_results=4)

#         rules_text = _rules_to_text(rule_docs)
#         rag_conf = _compute_rag_conf(rule_docs)

#         prompt = f"""
# You are MiFID II Risk Agent.

# Assess the trade using ONLY the normalized trade data and retrieved rules.
# Do not invent drivers.
# Do not hallucinate.
# Return JSON only.

# Trade (normalized preferred):
# {json.dumps(trade_view, indent=2, ensure_ascii=False)}

# Original trade:
# {json.dumps(trade, indent=2, ensure_ascii=False)}

# Rules:
# {rules_text if rules_text else "No retrieved risk rules"}

# Return JSON only:
# {{
#   "trade_id": "{trade_id}",
#   "risk_level": "LOW | MEDIUM | HIGH",
#   "confidence": 0.0,
#   "summary": "",
#   "drivers": []
# }}
# """.strip()

#         fallback = {
#             "trade_id": trade_id,
#             "risk_level": "HIGH",
#             "confidence": 0.0,
#             "summary": "fallback",
#             "drivers": [],
#         }

#         result, raw = call_llm_json(prompt, fallback, retries=2)
#         raw_outputs.append({"trade_id": trade_id, "raw": raw})

#         if not isinstance(result, dict):
#             result = fallback

#         risk_level = str(result.get("risk_level", "HIGH")).upper().strip()
#         if risk_level not in {"LOW", "MEDIUM", "HIGH"}:
#             risk_level = "HIGH"

#         drivers = _clean_drivers(result.get("drivers", []))
#         final_conf = _normalize_conf(result.get("confidence"), rag_conf)

#         results.append(
#             {
#                 "trade_id": trade_id,
#                 "risk_level": risk_level,
#                 "confidence": final_conf,
#                 "summary": result.get("summary", ""),
#                 "drivers": drivers,
#                 "rag_confidence": rag_conf,
#             }
#         )

#         logs.append(f"RiskAgent done {trade_id}")

#     return {
#         "risk_results": results,
#         "risk_raw_outputs": raw_outputs,
#         "agent_log": logs,
#     }
# ----------------------------------------------------------------------------------------------

# import json
# from typing import Any, Dict, List

# from rag.retriever import search_rules
# from utils.llm_json import call_llm_json


# def _safe_float(value: Any, default: float = 0.0) -> float:
#     try:
#         return float(value)
#     except Exception:
#         return default


# def _clamp01(value: Any, default: float = 0.0) -> float:
#     try:
#         return max(0.0, min(1.0, float(value)))
#     except Exception:
#         return max(0.0, min(1.0, default))


# def _trade_view(trade: dict) -> dict:
#     normalized = trade.get("normalized_trade")
#     if isinstance(normalized, dict):
#         return normalized
#     return trade


# def _pick_first(view: dict, keys: List[str]) -> str:
#     for k in keys:
#         v = view.get(k)
#         if v not in (None, ""):
#             return str(v).strip()
#     return ""


# def _standardize_trade_fields(trade: dict) -> dict:
#     view = _trade_view(trade)

#     return {
#         "trade_id": _pick_first(view, ["trade_id"]),
#         "trade_datetime": _pick_first(view, ["trade_datetime", "Execution_Timestamp"]),
#         "isin": _pick_first(view, ["isin", "instrument_id", "Instrument_Identification_Code"]),
#         "executing_entity_lei": _pick_first(view, ["executing_entity_lei", "executing_entity", "Executing_Entity_Identification_Code"]),
#         "buyer_lei": _pick_first(view, ["buyer_lei", "buyer", "Buyer_Identification_Code"]),
#         "seller_lei": _pick_first(view, ["seller_lei", "seller", "Seller_Identification_Code"]),
#         "price": _pick_first(view, ["price", "Price"]),
#         "currency": _pick_first(view, ["currency", "Price_Currency"]),
#         "quantity": _pick_first(view, ["quantity", "Quantity"]),
#         "venue": _pick_first(view, ["venue", "Venue"]),
#         "notional_amount": _pick_first(view, ["notional_amount", "notional", "Notional_Amount"]),
#         "report_status": _pick_first(view, ["report_status", "Report_Status"]),
#         "instrument_type": _pick_first(view, ["instrument_type", "Instrument_Type", "instrument_classification"]),
#     }


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


# def _is_iso8601_utc(value: str) -> bool:
#     if not value:
#         return False
#     try:
#         from datetime import datetime
#         dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
#         return dt.tzinfo is not None and dt.utcoffset().total_seconds() == 0
#     except Exception:
#         return False


# def _is_valid_isin(value: str) -> bool:
#     return bool(value) and len(value) == 12 and value.isalnum()


# def _is_valid_lei(value: str) -> bool:
#     return bool(value) and len(value) == 20 and value.isalnum()


# def _is_valid_currency(value: str) -> bool:
#     return value.upper() in {"USD", "EUR", "GBP", "JPY", "CHF", "INR"}


# def _is_valid_venue(value: str) -> bool:
#     v = value.upper().strip()
#     return len(v) >= 4 and v.startswith("X")


# def _severity_counts(drivers: List[dict]) -> Dict[str, int]:
#     counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
#     for d in drivers:
#         if not isinstance(d, dict):
#             continue
#         sev = str(d.get("severity", "")).upper()
#         if sev in counts:
#             counts[sev] += 1
#     return counts


# def _risk_tier_from_drivers(drivers: List[dict]) -> str:
#     """
#     Simple enterprise-style risk tiering:
#     - LOW    = clean trade
#     - MEDIUM = some issues, but not catastrophic
#     - HIGH   = clearly risky / non-compliant
#     """
#     if not drivers:
#         return "LOW"

#     counts = _severity_counts(drivers)
#     total = len(drivers)

#     if counts["CRITICAL"] >= 2:
#         return "HIGH"
#     if counts["CRITICAL"] >= 1 and counts["HIGH"] >= 1:
#         return "HIGH"
#     if counts["HIGH"] >= 3:
#         return "HIGH"
#     if counts["HIGH"] >= 2 and total >= 3:
#         return "HIGH"

#     if counts["CRITICAL"] >= 1:
#         return "HIGH"
#     if counts["HIGH"] >= 1 or counts["MEDIUM"] >= 1:
#         return "MEDIUM"

#     return "LOW"


# def _risk_confidence_from_tier(tier: str, drivers: List[dict], rag_conf: float) -> float:
#     """
#     Confidence is aligned to the risk outcome:
#     LOW risk    -> high confidence
#     MEDIUM risk -> middle confidence
#     HIGH risk   -> low confidence

#     This makes the UI easy to explain to business users.
#     """
#     counts = _severity_counts(drivers)
#     total = len(drivers)
#     rag = _clamp01(rag_conf, 0.3)

#     if tier == "LOW":
#         conf = 0.88 + (rag * 0.07)
#         return round(min(max(conf, 0.85), 0.95), 2)

#     if tier == "MEDIUM":
#         penalty = (counts["CRITICAL"] * 0.04) + (counts["HIGH"] * 0.03) + (counts["MEDIUM"] * 0.02)
#         conf = 0.68 + (rag * 0.07) - penalty - (max(0, total - 1) * 0.01)
#         return round(min(max(conf, 0.55), 0.84), 2)

#     # HIGH
#     penalty = (counts["CRITICAL"] * 0.05) + (counts["HIGH"] * 0.03) + (counts["MEDIUM"] * 0.01)
#     conf = 0.36 + (rag * 0.04) - penalty - (max(0, total - 2) * 0.01)
#     return round(min(max(conf, 0.20), 0.49), 2)


# def _build_deterministic_drivers(trade: dict) -> List[dict]:
#     drivers = []

#     trade_datetime = _pick_first(trade, ["trade_datetime"])
#     isin = _pick_first(trade, ["isin"])
#     executing_lei = _pick_first(trade, ["executing_entity_lei"])
#     buyer_lei = _pick_first(trade, ["buyer_lei"])
#     seller_lei = _pick_first(trade, ["seller_lei"])
#     currency = _pick_first(trade, ["currency"]).upper()
#     venue = _pick_first(trade, ["venue"]).upper()
#     report_status = _pick_first(trade, ["report_status"]).upper()
#     instrument_type = _pick_first(trade, ["instrument_type"]).upper()

#     price = _safe_float(trade.get("price"), 0.0)
#     quantity = _safe_float(trade.get("quantity"), 0.0)
#     notional = _safe_float(trade.get("notional_amount"), 0.0)

#     if not trade_datetime:
#         drivers.append({
#             "rule_id": "BR-006",
#             "severity": "CRITICAL",
#             "field": "trade_datetime",
#             "description": "trade_datetime is missing.",
#         })
#     elif not _is_iso8601_utc(trade_datetime):
#         drivers.append({
#             "rule_id": "BR-006",
#             "severity": "CRITICAL",
#             "field": "trade_datetime",
#             "description": f"trade_datetime '{trade_datetime}' is not valid ISO 8601 UTC format.",
#         })

#     if not isin:
#         drivers.append({
#             "rule_id": "BR-007",
#             "severity": "CRITICAL",
#             "field": "isin",
#             "description": "ISIN is missing.",
#         })
#     elif not _is_valid_isin(isin):
#         drivers.append({
#             "rule_id": "BR-007",
#             "severity": "CRITICAL",
#             "field": "isin",
#             "description": f"ISIN '{isin}' is not a valid 12-character ISO 6166 code.",
#         })

#     if not executing_lei:
#         drivers.append({
#             "rule_id": "BR-002",
#             "severity": "CRITICAL",
#             "field": "executing_entity_lei",
#             "description": "Executing entity LEI is missing.",
#         })
#     elif not _is_valid_lei(executing_lei):
#         drivers.append({
#             "rule_id": "BR-002",
#             "severity": "CRITICAL",
#             "field": "executing_entity_lei",
#             "description": f"Executing entity LEI '{executing_lei}' is not a valid 20-character ISO 17442 LEI.",
#         })

#     if buyer_lei and seller_lei and buyer_lei == seller_lei:
#         drivers.append({
#             "rule_id": "BR-003",
#             "severity": "HIGH",
#             "fields": ["buyer_lei", "seller_lei"],
#             "description": "Buyer and seller LEIs are identical (possible wash trade).",
#             "values": [buyer_lei, seller_lei],
#         })

#     if price <= 0:
#         drivers.append({
#             "rule_id": "BR-004",
#             "severity": "HIGH",
#             "field": "price",
#             "description": f"Price '{trade.get('price')}' must be strictly positive.",
#         })

#     if quantity <= 0:
#         drivers.append({
#             "rule_id": "BR-005",
#             "severity": "HIGH",
#             "field": "quantity",
#             "description": f"Quantity '{trade.get('quantity')}' must be strictly positive.",
#         })

#     if currency and not _is_valid_currency(currency):
#         drivers.append({
#             "rule_id": "BR-008",
#             "severity": "HIGH",
#             "field": "currency",
#             "description": f"Currency '{currency}' is not a valid ISO 4217 code.",
#         })

#     if venue and not _is_valid_venue(venue):
#         drivers.append({
#             "rule_id": "BR-009",
#             "severity": "HIGH",
#             "field": "venue",
#             "description": f"Venue '{venue}' is not a valid ISO 10383 MIC code.",
#         })

#     if report_status not in {"NEWT", "AMND", "CANC"}:
#         drivers.append({
#             "rule_id": "BR-010",
#             "severity": "CRITICAL",
#             "field": "report_status",
#             "description": f"Report status '{report_status}' is invalid. Must be NEWT, AMND, or CANC.",
#         })

#     if price > 0 and quantity > 0 and notional > 0:
#         expected_notional = round(price * quantity, 2)
#         if abs(expected_notional - notional) > 0.01:
#             drivers.append({
#                 "rule_id": "BR-001",
#                 "severity": "CRITICAL",
#                 "field": "notional_amount",
#                 "description": f"Notional amount '{notional}' does not equal price × quantity ({expected_notional}).",
#             })

#     if instrument_type == "EQUITY":
#         if not buyer_lei:
#             drivers.append({
#                 "rule_id": "BR-011",
#                 "severity": "HIGH",
#                 "field": "buyer_lei",
#                 "description": "Buyer LEI is mandatory for equity trades.",
#             })
#         if not seller_lei:
#             drivers.append({
#                 "rule_id": "BR-011",
#                 "severity": "HIGH",
#                 "field": "seller_lei",
#                 "description": "Seller LEI is mandatory for equity trades.",
#             })

#     return drivers


# def _deterministic_risk(trade: dict) -> dict:
#     drivers = _build_deterministic_drivers(trade)
#     tier = _risk_tier_from_drivers(drivers)
#     confidence = _risk_confidence_from_tier(tier, drivers, rag_conf=0.3)

#     if tier == "LOW":
#         return {
#             "risk_level": "LOW",
#             "decision_tier": "LOW",
#             "confidence": confidence,
#             "summary": "Trade is low risk and no material risk drivers were detected.",
#             "drivers": [],
#         }

#     if tier == "MEDIUM":
#         return {
#             "risk_level": "MEDIUM",
#             "decision_tier": "MEDIUM",
#             "confidence": confidence,
#             "summary": "Trade has moderate risk and should be reviewed.",
#             "drivers": drivers,
#         }

#     return {
#         "risk_level": "HIGH",
#         "decision_tier": "HIGH",
#         "confidence": confidence,
#         "summary": "Trade is high risk due to one or more severe rule breaches.",
#         "drivers": drivers,
#     }


# def risk_agent(state: dict) -> dict:
#     trades = state.get("enriched_trades", [])
#     results, logs, raw_outputs = [], [], []

#     if not isinstance(trades, list):
#         trades = []

#     for trade in trades:
#         if not isinstance(trade, dict):
#             continue

#         trade_id = trade.get("trade_id", "UNKNOWN")
#         trade_view = _standardize_trade_fields(trade)

#         query = (
#             f"risk assessment for trade "
#             f"isin {trade_view.get('isin', '')} "
#             f"price {trade_view.get('price', '')} "
#             f"quantity {trade_view.get('quantity', '')} "
#             f"notional {trade_view.get('notional_amount', '')}"
#         )

#         rule_docs = search_rules(query=query, rule_type="risk", n_results=4)
#         rules_text = _rules_to_text(rule_docs)
#         rag_conf = _compute_rag_conf(rule_docs)

#         deterministic = _deterministic_risk(trade_view)

#         prompt = f"""
# You are MiFID II Risk Agent.

# Write a short human-readable summary only.
# Do not change the risk decision.
# Do not invent risk drivers.
# Return JSON only.

# Trade:
# {json.dumps(trade_view, indent=2, ensure_ascii=False)}

# Deterministic risk result:
# {json.dumps(deterministic, indent=2, ensure_ascii=False)}

# Retrieved rules:
# {rules_text if rules_text else "No retrieved risk rules"}

# Return JSON only:
# {{
#   "summary": ""
# }}
# """.strip()

#         fallback = {
#             "summary": deterministic["summary"],
#         }

#         result, raw = call_llm_json(prompt, fallback, retries=2)
#         raw_outputs.append({"trade_id": trade_id, "raw": raw})

#         if not isinstance(result, dict):
#             result = fallback

#         final_confidence = _risk_confidence_from_tier(
#             deterministic["risk_level"],
#             deterministic["drivers"],
#             rag_conf
#         )

#         results.append({
#             "trade_id": trade_id,
#             "risk_level": deterministic["risk_level"],
#             "confidence": final_confidence,
#             "summary": result.get("summary") or deterministic["summary"],
#             "drivers": deterministic["drivers"],
#             "rag_confidence": rag_conf,
#         })

#         logs.append(f"RiskAgent done {trade_id}")

#     return {
#         "risk_results": results,
#         "risk_raw_outputs": raw_outputs,
#         "agent_log": logs,
#     }



# ------------------------------------------------------
#

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


# ─────────────────────────────────────────────
# MAIN AGENT (RAG BASED)
# ─────────────────────────────────────────────

def risk_agent(state: dict) -> dict:
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
risk assessment for trade
isin {trade_view.get('isin', '')}
price {trade_view.get('price', '')}
quantity {trade_view.get('quantity', '')}
notional {trade_view.get('notional_amount', '')}
""".strip()

        rule_docs = search_rules(query=query, rule_type="risk", n_results=5)
        rules_text = _rules_to_text(rule_docs)
        rag_conf = _compute_rag_conf(rule_docs)

        # 🧠 LLM DECISION (NO DETERMINISTIC)
        prompt = f"""
You are MiFID II Risk Agent.

Your job:
- Analyze trade risk using rules + trade data
- Assign ONLY one of: PASS / HITL / FAIL
- Generate confidence aligned to decision

Rules:
PASS  = safe trade → confidence 0.75–0.95
HITL  = uncertain → confidence 0.40–0.74
FAIL  = risky trade → confidence 0.10–0.39

Trade:
{json.dumps(trade_view, indent=2)}

Rules:
{rules_text if rules_text else "No rules found"}

Return JSON only:
{{
  "trade_id": "{trade_id}",
  "risk_level": "PASS | HITL | FAIL",
  "confidence": 0.0,
  "summary": "",
  "drivers": []
}}
"""

        fallback = {
            "trade_id": trade_id,
            "risk_level": "HITL",
            "confidence": 0.5,
            "summary": "Fallback risk decision",
            "drivers": [],
        }

        result, raw = call_llm_json(prompt, fallback, retries=2)
        raw_outputs.append({"trade_id": trade_id, "raw": raw})

        if not isinstance(result, dict):
            result = fallback

        final_conf = _normalize_conf(result.get("confidence"), rag_conf)

        results.append({
    "trade_id": trade_id,
    "risk_level": result.get("risk_level", "HITL"),
    "confidence": final_conf,
    "summary": result.get("summary", ""),
    "drivers": result.get("drivers", []),
    "rag_confidence": rag_conf,

    # ✅ NEW
    "source_channel": trade.get("source_channel"),
    "trace_id": trade.get("trace_id"),
    })

        logs.append(f"RiskAgent done {trade_id}")

    return {
        "risk_results": results,
        "risk_raw_outputs": raw_outputs,
        "agent_log": logs,
    }