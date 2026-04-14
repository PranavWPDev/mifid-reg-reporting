# from __future__ import annotations

# import asyncio
# from collections import Counter
# from typing import Dict, List

# from agents.orchestrator import run_pipeline
# from intelligence.intent_agent import intent_agent
# from intelligence.planning_agent import planning_agent
# from intelligence.report_formatter import report_formatter
# from routers.channel_router import ChannelRouter
# from tools.tool_registry import TOOL_REGISTRY


# def _merge_trade_rows(rows: List[dict]) -> List[dict]:
#     """
#     Merge records by trade_id. Later sources enrich earlier sources.
#     """
#     merged: Dict[str, dict] = {}

#     for row in rows:
#         if not isinstance(row, dict):
#             continue

#         trade_id = str(row.get("trade_id") or row.get("execution_id") or "").strip()
#         if not trade_id:
#             continue

#         existing = merged.get(trade_id, {})
#         combined = dict(existing)

#         for k, v in row.items():
#             if v not in (None, "", [], {}):
#                 combined[k] = v

#         merged[trade_id] = combined

#     return list(merged.values())


# def _source_breakdown(trades: List[dict]) -> Dict[str, int]:
#     counter = Counter()
#     for t in trades:
#         counter[str(t.get("source_channel") or "unknown")] += 1
#     return dict(counter)


# async def handle_auditor_query(query: str) -> dict:
#     """
#     Main entry point for the auditor chat workflow.

#     Flow:
#     1) classify intent
#     2) create execution plan
#     3) fetch data from sources
#     4) normalize into pipeline envelope
#     5) run existing MiFID pipeline unchanged
#     6) format narrative response
#     """
#     intent = intent_agent(query)
#     plan = planning_agent(intent)

#     fetched_rows: List[dict] = []

#     for step in plan["steps"]:
#         tool_name = step["tool"]
#         tool_fn = TOOL_REGISTRY[tool_name]
#         params = step.get("params", {})

#         rows = await asyncio.to_thread(tool_fn, **params)

#         for row in rows:
#             row.setdefault("source_channel", tool_name)
#             row.setdefault("source_system", params.get("source_system", tool_name))
#             row.setdefault("source_ref", params.get("source_ref", tool_name))

#         fetched_rows.extend(rows)

#     merged_rows = _merge_trade_rows(fetched_rows)

#     if not merged_rows:
#         return {
#             "response": "No matching trades or execution records were found for that query.",
#             "run_id": None,
#             "stats": {},
#             "source_breakdown": {},
#             "report_path": None,
#             "csv_path": None,
#             "exception_report_path": None,
#             "final_trades": [],
#             "hitl_queue": [],
#             "corrections": [],
#             "intent": intent,
#             "plan": plan,
#         }

#     router = ChannelRouter()
#     envelope = router.build_envelope(
#         merged_rows,
#         source_channel="agentic_query",
#         source_system="audit-intelligence",
#         source_ref=intent.get("report_type", "manual"),
#     )

#     pipeline_result = await asyncio.to_thread(
#         run_pipeline,
#         envelope,
#         source_channel="agentic_query",
#         source_system="audit-intelligence",
#         source_ref=intent.get("report_type", "manual"),
#     )

#     narrative = await asyncio.to_thread(report_formatter, query, pipeline_result)
#     final_trades = pipeline_result.get("final_trades", []) or []

#     return {
#         "response": narrative,
#         "run_id": pipeline_result.get("run_id"),
#         "stats": pipeline_result.get("stats", {}),
#         "source_breakdown": _source_breakdown(merged_rows),
#         "report_path": pipeline_result.get("report_path"),
#         "csv_path": pipeline_result.get("csv_path"),
#         "exception_report_path": pipeline_result.get("exception_report_path"),
#         "final_trades": final_trades,
#         "hitl_queue": pipeline_result.get("hitl_queue", []),
#         "corrections": pipeline_result.get("corrections", []),
#         "intent": intent,
#         "plan": plan,
#     }


from __future__ import annotations

import asyncio
from collections import Counter
from typing import Dict, List

from agents.orchestrator import run_pipeline
from intelligence.intent_agent import intent_agent
from intelligence.planning_agent import planning_agent
from intelligence.report_formatter import report_formatter
from routers.channel_router import ChannelRouter
from tools.tool_registry import TOOL_REGISTRY


# ─────────────────────────────────────────────
# MERGE LOGIC
# ─────────────────────────────────────────────
def _merge_trade_rows(rows: List[dict]) -> List[dict]:
    merged: Dict[str, dict] = {}

    for row in rows:
        if not isinstance(row, dict):
            continue

        trade_id = str(row.get("trade_id") or row.get("execution_id") or "").strip()
        if not trade_id:
            continue

        existing = merged.get(trade_id, {})
        combined = dict(existing)

        for k, v in row.items():
            if v not in (None, "", [], {}):
                combined[k] = v

        merged[trade_id] = combined

    return list(merged.values())


def _source_breakdown(trades: List[dict]) -> Dict[str, int]:
    counter = Counter()
    for t in trades:
        counter[str(t.get("source_channel") or "unknown")] += 1
    return dict(counter)


# ─────────────────────────────────────────────
# MAIN HANDLER
# ─────────────────────────────────────────────
async def handle_auditor_query(query: str) -> dict:
    print("\n🧠 USER QUERY:", query)

    # 🔥 Step 1: Intent
    intent = intent_agent(query)

    # ✅ CRITICAL FIX (LLM SUPPORT)
    intent["query"] = query

    print("🧠 INTENT:", intent)

    # 🔥 Step 2: Planning
    plan = planning_agent(intent)

    print("🧠 PLAN:", plan)

    fetched_rows: List[dict] = []

    # 🔥 Step 3: Execute tools
    for step in plan.get("steps", []):
        tool_name = step.get("tool")
        tool_fn = TOOL_REGISTRY.get(tool_name)

        if not tool_fn:
            print(f"❌ Tool not found: {tool_name}")
            continue

        params = step.get("params", {}) or {}

        # ✅ FIX: Remove unsupported params
        safe_params = {
            k: v for k, v in params.items()
            if k not in ("source_channel", "source_system", "source_ref")
        }

        print(f"\n🔧 EXECUTING TOOL: {tool_name}")
        print("PARAMS:", safe_params)

        try:
            rows = await asyncio.to_thread(tool_fn, **safe_params)
        except Exception as e:
            print("❌ TOOL ERROR:", str(e))
            continue

        print(f"✅ Rows fetched: {len(rows)}")

        for row in rows:
            row.setdefault("source_channel", tool_name)
            row.setdefault("source_system", tool_name)
            row.setdefault("source_ref", "audit-query")

        fetched_rows.extend(rows)

    print(f"\n📊 TOTAL ROWS FETCHED: {len(fetched_rows)}")

    # 🔥 Step 4: Merge
    merged_rows = _merge_trade_rows(fetched_rows)

    print(f"📊 MERGED ROWS: {len(merged_rows)}")

    # ⚠️ IMPORTANT CHANGE: Do NOT stop pipeline early
    if not merged_rows:
        print("⚠️ No rows found — returning fallback response")

        return {
            "response": "No matching data found in sources. Try different filters.",
            "run_id": None,
            "stats": {},
            "source_breakdown": {},
            "report_path": None,
            "csv_path": None,
            "exception_report_path": None,
            "final_trades": [],
            "hitl_queue": [],
            "corrections": [],
            "intent": intent,
            "plan": plan,
        }

    # 🔥 Step 5: Build envelope
    router = ChannelRouter()

    envelope = router.build_envelope(
        merged_rows,
        source_channel="agentic_query",
        source_system="audit-intelligence",
        source_ref=intent.get("report_type", "manual"),
    )

    print("📦 ENVELOPE SIZE:", len(envelope))

    # 🔥 Step 6: Run pipeline
    pipeline_result = await asyncio.to_thread(
        run_pipeline,
        envelope,
        source_channel="agentic_query",
        source_system="audit-intelligence",
        source_ref=intent.get("report_type", "manual"),
    )

    print("🚀 PIPELINE COMPLETED")

    # 🔥 Step 7: Format response
    narrative = await asyncio.to_thread(report_formatter, query, pipeline_result)

    final_trades = pipeline_result.get("final_trades", []) or []

    return {
        "response": narrative,
        "run_id": pipeline_result.get("run_id"),
        "stats": pipeline_result.get("stats", {}),
        "source_breakdown": _source_breakdown(merged_rows),
        "report_path": pipeline_result.get("report_path"),
        "csv_path": pipeline_result.get("csv_path"),
        "exception_report_path": pipeline_result.get("exception_report_path"),
        "final_trades": final_trades,
        "hitl_queue": pipeline_result.get("hitl_queue", []),
        "corrections": pipeline_result.get("corrections", []),
        "intent": intent,
        "plan": plan,
    }