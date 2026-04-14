
# import json
# from typing import Any

# from db.relational import SessionLocal, AuditLog
# from utils.llm_json import call_llm_json


# def _safe_float(v: Any) -> float:
#     try:
#         return max(0.0, min(1.0, float(v)))
#     except Exception:
#         return 0.0


# def _aggregate_confidence(v: dict, r: dict, c: dict) -> float:
#     return round(
#         (_safe_float(v.get("confidence")) * 0.4) +
#         (_safe_float(r.get("confidence")) * 0.3) +
#         (_safe_float(c.get("confidence")) * 0.3),
#         2
#     )


# def _trade_is_auto_fixed(trade: dict) -> bool:
#     if not isinstance(trade, dict):
#         return False
#     if trade.get("auto_fix_applied") is True:
#         return True
#     corrections = trade.get("corrections", [])
#     return isinstance(corrections, list) and len(corrections) > 0


# def _confidence_by_status(base_conf: float, status: str) -> float:
#     base_conf = _safe_float(base_conf)
#     status = (status or "").upper().strip()

#     if status == "PASS":
#         return round(0.85 + (base_conf * 0.14), 2)

#     if status == "HITL":
#         return round(0.50 + (base_conf * 0.34), 2)

#     if status == "FAIL":
#         return round(0.20 + (base_conf * 0.29), 2)

#     return round(0.50 + (base_conf * 0.34), 2)


# def _confidence_label(status: str, auto_fixed: bool) -> str:
#     status = (status or "").upper().strip()
#     if status == "PASS" and auto_fixed:
#         return "PASS (AUTO-FIXED)"
#     if status == "PASS":
#         return "PASS"
#     if status == "HITL":
#         return "HITL"
#     if status == "FAIL":
#         return "FAIL"
#     return "UNKNOWN"


# def decision_agent(state: dict) -> dict:
#     run_id = state["run_id"]

#     trades = state.get("enriched_trades", [])
#     validation_map = {v["trade_id"]: v for v in state.get("validation_results", [])}
#     risk_map = {r["trade_id"]: r for r in state.get("risk_results", [])}
#     compliance_map = {c["trade_id"]: c for c in state.get("compliance_results", [])}

#     db = SessionLocal()
#     final_trades = []
#     hitl_queue = []
#     logs = []

#     try:
#         for trade in trades:
#             if not isinstance(trade, dict):
#                 continue

#             trade_id = trade.get("trade_id")
#             val = validation_map.get(trade_id, {})
#             risk = risk_map.get(trade_id, {})
#             comp = compliance_map.get(trade_id, {})

#             auto_fixed = _trade_is_auto_fixed(trade)

#             # =========================
#             # 🔥 UPDATED DECISION LOGIC
#             # =========================

#             val_tier = (val.get("decision_tier") or "").upper()

#             decision = "PASS"
#             reason = "All checks passed"

#             # 1. VALIDATION FAIL → FINAL FAIL
#             if val_tier == "FAIL":
#                 decision = "FAIL"
#                 reason = "Validation failed with critical issues"

#             # 2. VALIDATION HITL → FINAL HITL
#             elif val_tier == "HITL":
#                 decision = "HITL"
#                 reason = "Validation requires review"

#             # 3. COMPLIANCE FAIL
#             elif not comp.get("compliant", True):
#                 decision = "HITL"
#                 reason = "Compliance failed"

#             # 4. HIGH RISK
#             elif (risk.get("risk_level") or "").upper() == "HIGH":
#                 decision = "HITL"
#                 reason = "High risk detected"

#             # else PASS

#             # =========================
#             # CONFIDENCE
#             # =========================

#             raw_base_conf = _aggregate_confidence(val, risk, comp)
#             confidence = _confidence_by_status(raw_base_conf, decision)

#             # =========================
#             # LLM EXPLANATION
#             # =========================

#             prompt = f"""
# Explain the final decision briefly in JSON only.

# Trade:
# {json.dumps(trade, ensure_ascii=False)}

# Validation:
# {json.dumps(val, ensure_ascii=False)}

# Risk:
# {json.dumps(risk, ensure_ascii=False)}

# Compliance:
# {json.dumps(comp, ensure_ascii=False)}

# Final Decision: {decision}

# Return JSON only:
# {{ "reason": "" }}
# """.strip()

#             fallback = {"reason": reason}

#             try:
#                 result, _ = call_llm_json(prompt, fallback, retries=2)
#                 if isinstance(result, dict):
#                     reason = result.get("reason") or reason
#             except Exception:
#                 pass

#             final_trade = {
#                 **trade,
#                 "final_status": decision,
#                 "decision_confidence": confidence,
#                 "decision_reason": reason,
#                 "confidence_label": _confidence_label(decision, auto_fixed),
#                 "confidence_band": (
#                     "PASS" if decision == "PASS"
#                     else "FAIL" if decision == "FAIL"
#                     else "REVIEW"
#                 ),
#                 "auto_fix_applied": auto_fixed,
#                 "auto_fix_status": "APPLIED" if auto_fixed else "NONE",
#                 "decision_path": (
#                     "AUTO_FIXED_PASS" if auto_fixed and decision == "PASS"
#                     else decision
#                 ),
#                 "raw_decision_confidence": raw_base_conf,
#             }

#             final_trades.append(final_trade)

#             if decision in ["HITL", "FAIL"]:
#                 hitl_queue.append({
#                     "trade_id": trade_id,
#                     "reason": reason,
#                     "trade": trade,
#                     "validation": val,
#                     "risk": risk,
#                     "compliance": comp,
#                     "confidence": confidence,
#                     "confidence_label": _confidence_label(decision, auto_fixed),
#                     "auto_fix_applied": auto_fixed,
#                     "decision_path": decision,
#                 })

#             db.add(AuditLog(
#                 run_id=run_id,
#                 trade_id=trade_id,
#                 agent="DecisionAgent",
#                 action=decision,
#                 detail=json.dumps({
#                     "decision_confidence": confidence,
#                     "raw_decision_confidence": raw_base_conf,
#                     "reason": reason,
#                     "validation": val,
#                     "risk": risk,
#                     "compliance": comp,
#                     "auto_fix_applied": auto_fixed,
#                     "decision_path": final_trade["decision_path"],
#                 }, ensure_ascii=False),
#             ))

#             logs.append(f"DecisionAgent {decision} {trade_id}")

#         db.commit()

#         return {
#             "final_trades": final_trades,
#             "hitl_queue": hitl_queue,
#             "agent_log": logs
#         }

#     except Exception:
#         db.rollback()
#         raise
#     finally:
#         db.close()

import json
from typing import Any

from db.relational import SessionLocal, AuditLog
from utils.llm_json import call_llm_json


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def _safe_float(v: Any) -> float:
    try:
        return max(0.0, min(1.0, float(v)))
    except Exception:
        return 0.0


def _trade_is_auto_fixed(trade: dict) -> bool:
    if not isinstance(trade, dict):
        return False
    if trade.get("auto_fix_applied") is True:
        return True
    corrections = trade.get("corrections", [])
    return isinstance(corrections, list) and len(corrections) > 0


def _tier_from_confidence(conf: float) -> str:
    if conf >= 0.70:
        return "PASS"
    if conf >= 0.40:
        return "HITL"
    return "FAIL"


def _confidence_label(status: str, auto_fixed: bool) -> str:
    status = (status or "").upper().strip()

    if status == "PASS" and auto_fixed:
        return "PASS (AUTO-FIXED)"
    if status == "PASS":
        return "PASS"
    if status == "HITL":
        return "HITL"
    if status == "FAIL":
        return "FAIL"

    return "UNKNOWN"


# ─────────────────────────────────────────────
# MAIN AGENT
# ─────────────────────────────────────────────

def decision_agent(state: dict) -> dict:
    run_id = state["run_id"]

    trades = state.get("enriched_trades", [])
    validation_map = {v["trade_id"]: v for v in state.get("validation_results", [])}
    risk_map = {r["trade_id"]: r for r in state.get("risk_results", [])}
    compliance_map = {c["trade_id"]: c for c in state.get("compliance_results", [])}

    db = SessionLocal()
    final_trades = []
    hitl_queue = []
    logs = []

    try:
        for trade in trades:
            if not isinstance(trade, dict):
                continue

            trade_id = trade.get("trade_id")

            val = validation_map.get(trade_id, {})
            risk = risk_map.get(trade_id, {})
            comp = compliance_map.get(trade_id, {})

            auto_fixed = _trade_is_auto_fixed(trade)

            # ─────────────────────────────────────────────
            # GET TIERS FROM ALL AGENTS
            # ─────────────────────────────────────────────

            val_tier = (val.get("decision_tier") or "").upper().strip()
            risk_tier = (risk.get("risk_level") or "").upper().strip()
            comp_tier = (comp.get("compliance_status") or "").upper().strip()

            val_conf = _safe_float(val.get("confidence"))
            risk_conf = _safe_float(risk.get("confidence"))
            comp_conf = _safe_float(comp.get("confidence"))

            # fallback if LLM didn't return tier
            if val_tier not in {"PASS", "HITL", "FAIL"}:
                val_tier = _tier_from_confidence(val_conf)

            if risk_tier not in {"PASS", "HITL", "FAIL"}:
                risk_tier = _tier_from_confidence(risk_conf)

            if comp_tier not in {"PASS", "HITL", "FAIL"}:
                comp_tier = _tier_from_confidence(comp_conf)

            # ─────────────────────────────────────────────
            # FINAL DECISION LOGIC (CRITICAL FIX)
            # ─────────────────────────────────────────────

            tiers = [val_tier, risk_tier, comp_tier]

            if "FAIL" in tiers:
                decision = "FAIL"
            elif "HITL" in tiers:
                decision = "HITL"
            else:
                decision = "PASS"

            # ─────────────────────────────────────────────
            # CONFIDENCE (ALIGNED WITH DECISION)
            # ─────────────────────────────────────────────

            available_conf = [c for c in [val_conf, risk_conf, comp_conf] if c > 0]

            if available_conf:
                confidence = min(available_conf)  # conservative approach
            else:
                confidence = (
                    0.88 if decision == "PASS" else
                    0.55 if decision == "HITL" else
                    0.25
                )

            # ─────────────────────────────────────────────
            # REASON (LLM SUMMARY)
            # ─────────────────────────────────────────────

            prompt = f"""
Explain the final decision briefly.

Trade:
{json.dumps(trade, ensure_ascii=False)}

Validation:
{json.dumps(val, ensure_ascii=False)}

Risk:
{json.dumps(risk, ensure_ascii=False)}

Compliance:
{json.dumps(comp, ensure_ascii=False)}

Final Decision: {decision}

Return JSON:
{{ "reason": "" }}
"""

            fallback = {
                "reason": f"Decision derived from Validation ({val_tier}), Risk ({risk_tier}), Compliance ({comp_tier})"
            }

            try:
                result, _ = call_llm_json(prompt, fallback, retries=2)
                if isinstance(result, dict):
                    reason = result.get("reason") or fallback["reason"]
                else:
                    reason = fallback["reason"]
            except Exception:
                reason = fallback["reason"]

            # ─────────────────────────────────────────────
            # FINAL TRADE OBJECT
            # ─────────────────────────────────────────────

            final_trade = {
                **trade,
                "final_status": decision,
                "decision_confidence": round(_safe_float(confidence), 4),
                "decision_reason": reason,
                "confidence_label": _confidence_label(decision, auto_fixed),
                "confidence_band": decision,
                "auto_fix_applied": auto_fixed,
                "auto_fix_status": "APPLIED" if auto_fixed else "NONE",
                "decision_path": f"{val_tier}|{risk_tier}|{comp_tier}",
                "raw_decision_confidence": val_conf,
                # ✅ NEW (CRITICAL) 
                "source_channel": trade.get("source_channel"), 
                "trace_id": trade.get("trace_id"),
            }

            final_trades.append(final_trade)

            # ─────────────────────────────────────────────
            # HITL QUEUE (STRICT FIX)
            # ─────────────────────────────────────────────

            if decision == "HITL":
                hitl_queue.append({
                    "trade_id": trade_id,
                    "reason": reason,
                    "trade": trade,
                    "validation": val,
                    "risk": risk,
                    "compliance": comp,
                    "confidence": round(_safe_float(confidence), 4),
                    "confidence_label": _confidence_label(decision, auto_fixed),
                    "auto_fix_applied": auto_fixed,
                    "auto_fix_status": "APPLIED" if auto_fixed else "NONE",
                    "decision_path": final_trade["decision_path"],
                })

            # ─────────────────────────────────────────────
            # AUDIT LOG
            # ─────────────────────────────────────────────

            db.add(
                AuditLog(
                    run_id=run_id,
                    trade_id=trade_id,
                    agent="DecisionAgent",
                    action=decision,
                    detail=json.dumps({
                        "decision_confidence": round(_safe_float(confidence), 4),
                        "reason": reason,
                        "validation": val,
                        "risk": risk,
                        "compliance": comp,
                        "decision_path": final_trade["decision_path"],
                        "final_status": decision,
                    }, ensure_ascii=False),
                )
            )

            logs.append(f"DecisionAgent {decision} {trade_id}")

        db.commit()

        return {
            "final_trades": final_trades,
            "hitl_queue": hitl_queue,
            "agent_log": logs,
        }

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()