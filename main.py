

# from __future__ import annotations

# import os
# os.environ["ANONYMIZED_TELEMETRY"] = "False"
# os.environ["CHROMA_TELEMETRY"] = "False"

# import json
# import logging
# import datetime
# from pathlib import Path
# from typing import Any, Optional, List

# from fastapi import FastAPI, HTTPException, Body
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from dotenv import load_dotenv

# from config import get_settings
# from db.relational import init_db, SessionLocal, AuditLog, HitlQueue
# from rag import init_rag
# from agents.orchestrator import run_pipeline
# from intelligence.orchestrator import handle_auditor_query

# # ✅ tools
# from tools.bq_tool import fetch_trades as fetch_bigquery_trades
# from tools.inmemory_tool import fetch_trades as fetch_inmemory_trades

# load_dotenv()
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# settings = get_settings()

# app = FastAPI(title="MiFID II Agentic System")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ─────────────────────────────────────────────
# # STARTUP
# # ─────────────────────────────────────────────
# @app.on_event("startup")
# def startup():
#     logger.info("🚀 Starting System...")

#     init_db()
#     init_rag()

#     Path(settings.reports_dir).mkdir(parents=True, exist_ok=True)
#     Path(settings.inmemory_csv_path).parent.mkdir(parents=True, exist_ok=True)
#     Path(settings.sqlite_path).parent.mkdir(parents=True, exist_ok=True)
#     Path(settings.chroma_path).mkdir(parents=True, exist_ok=True)

#     logger.info("✅ System Ready")


# # ─────────────────────────────────────────────
# # MODELS
# # ─────────────────────────────────────────────
# class AuditQueryRequest(BaseModel):
#     query: str


# # ─────────────────────────────────────────────
# # HELPERS
# # ─────────────────────────────────────────────
# def _build_pipeline_response(result: dict) -> dict:
#     final_trades = result.get("final_trades", []) or []

#     return {
#         "run_id": result.get("run_id"),
#         "stats": result.get("stats", {}),
#         "final_trades": final_trades,
#         "hitl_queue": result.get("hitl_queue", []),
#         "corrections": result.get("corrections", []),
#         "validation_results": result.get("validation_results", []),
#         "risk_results": result.get("risk_results", []),
#         "compliance_results": result.get("compliance_results", []),
#     }


# # ─────────────────────────────────────────────
# # 🚀 CORE: CHAT → PIPELINE FLOW
# # ─────────────────────────────────────────────
# @app.post("/api/audit-query")
# async def audit_query(body: AuditQueryRequest):
#     try:
#         logger.info(f"📩 Query: {body.query}")

#         # 1️⃣ Intent + Planning
#         result = await handle_auditor_query(body.query)

#         intent = result.get("intent", {})
#         plan   = result.get("plan", {})
#         steps  = plan.get("steps", [])

#         logger.info(f"🧠 Intent: {intent.get('report_type')}")
#         logger.info(f"📌 Steps: {len(steps)}")

#         all_rows: List[dict] = []

#         # 2️⃣ Execute each step
#         for step in steps:
#             tool = step.get("tool")
#             params = step.get("params", {})

#             logger.info(f"⚙️ Executing tool: {tool}")

#             try:
#                 if tool == "inmemory":
#                     rows = fetch_inmemory_trades(
#                         filters=params.get("filters"),
#                         limit=params.get("limit", 500),
#                     )

#                 elif tool == "bigquery":
#                     rows = fetch_bigquery_trades(
#                         sql=params.get("sql"),
#                         params=params.get("params"),
#                         limit=params.get("limit", 500),
#                     )

#                 else:
#                     logger.warning(f"⚠️ Unknown tool: {tool}")
#                     continue

#                 # tag source
#                 for r in rows:
#                     r["source_channel"] = tool

#                 logger.info(f"📊 {tool} returned {len(rows)} rows")

#                 all_rows.extend(rows)

#             except Exception as tool_err:
#                 logger.exception(f"❌ Tool failed: {tool}")
#                 continue

#         # 3️⃣ Merge (simple merge for now)
#         merged_rows = {}
#         for row in all_rows:
#             key = row.get("trade_id") or row.get("execution_id")
#             if not key:
#                 continue

#             if key not in merged_rows:
#                 merged_rows[key] = row
#             else:
#                 merged_rows[key].update({k: v for k, v in row.items() if v})

#         final_rows = list(merged_rows.values())

#         logger.info(f"🔗 Merged rows: {len(final_rows)}")

#         # 4️⃣ 🚀 RUN PIPELINE
#         if final_rows:
#             pipeline_result = run_pipeline(
#                 final_rows,
#                 source_channel="agentic_query",
#             )

#             response = _build_pipeline_response(pipeline_result)

#             # attach intelligence info
#             response["intent"] = intent
#             response["plan"] = plan
#             response["llm_response"] = result.get("response", "")

#             return response

#         # fallback if no data
#         return {
#             "message": "No data found for query",
#             "intent": intent,
#             "plan": plan,
#         }

#     except Exception as e:
#         logger.exception("❌ Audit query failed")
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/api/sources/all")
# def fetch_all_trades():
#     from data_sources import get_db_trades, get_csv_trades
#     from tools.bq_tool import fetch_trades

#     db_trades = get_db_trades()
#     csv_trades = get_csv_trades()

#     # 🔥 ADD BIGQUERY FETCH
#     sql = """
#     SELECT *
#     FROM `deutschebank-aipocs.mifid_reporting.trade_execution_facts`
#     ORDER BY created_at DESC
#     LIMIT 100
#     """

#     bq_trades = fetch_trades(sql=sql)

#     merged = []

#     for t in db_trades:
#         merged.append({**t, "source_channel": "inmemory"})

#     for t in csv_trades:
#         merged.append({**t, "source_channel": "csv"})

#     for t in bq_trades:
#         merged.append({**t, "source_channel": "bigquery"})

#     return {
#         "source": "merged",
#         "count": len(merged),
#         "trades": merged,
#     }

# @app.post("/api/run-pipeline")
# def run_pipeline_endpoint(body: dict = Body(...)):
#     trades = body.get("trades") or body.get("data") or []

#     if not trades:
#         raise HTTPException(status_code=400, detail="No trades provided")

#     # ensure source_channel
#     for t in trades:
#         if "source_channel" not in t:
#             t["source_channel"] = t.get("_source") or "ui"

#     try:
#         result = run_pipeline(trades, source_channel="ui")

#         print(f"🚀 PIPELINE TRIGGERED: {len(trades)} trades")

#         # 🔥 FULL RESPONSE (UI FIX)
#         return {
#             "success": True,
#             "run_id": result.get("run_id"),
#             "stats": result.get("stats", {}),

#             # ✅ CORE
#             "final_trades": result.get("final_trades", []),
#             "hitl_queue": result.get("hitl_queue", []),
#             "corrections": result.get("corrections", []),

#             # ✅ IMPORTANT FOR UI TABS
#             "validation_results": result.get("validation_results", []),
#             "risk_results": result.get("risk_results", []),
#             "compliance_results": result.get("compliance_results", []),

#             # ✅ REPORTS TAB FIX
#             "report_json": result.get("report_json", {}),
#             "report_path": result.get("report_path", ""),
#             "exception_report_path": result.get("exception_report_path", ""),
#             "mifid_report_csv": result.get("mifid_report_csv", ""),
#         }

#     except Exception as e:
#         print("❌ PIPELINE ERROR:", str(e))
#         raise HTTPException(status_code=500, detail=str(e))
#     trades = body.get("trades") or body.get("data") or []

#     if not trades:
#         raise HTTPException(status_code=400, detail="No trades provided")

#     # 🔥 FIX: ensure source_channel exists
#     for t in trades:
#         if "source_channel" not in t:
#             t["source_channel"] = t.get("_source") or "ui"

#     try:
#         result = run_pipeline(trades, source_channel="ui")

#         print(f"🚀 PIPELINE TRIGGERED: {len(trades)} trades")

#         return {
#             "success": True,
#             "run_id": result.get("run_id"),
#             "stats": result.get("stats"),
#             "final_trades": result.get("final_trades"),
#             "hitl_queue": result.get("hitl_queue"),
#         }

#     except Exception as e:
#         print("❌ PIPELINE ERROR:", str(e))
#         raise HTTPException(status_code=500, detail=str(e))


# # ─────────────────────────────────────────────
# # AUDIT TRAIL API
# # ─────────────────────────────────────────────
# @app.get("/api/audit-log/{run_id}")
# def get_audit_log(run_id: str):
#     try:
#         db = SessionLocal()

#         logs = (
#             db.query(AuditLog)
#             .filter(AuditLog.run_id == run_id)
#             .order_by(AuditLog.created_at.asc())
#             .all()
#         )

#         return {
#             "run_id": run_id,
#             "count": len(logs),
#             "logs": [
#                 {
#                     "id": log.id,
#                     "step": log.step,
#                     "action": log.action,
#                     "details": log.details,
#                     "created_at": log.created_at.isoformat(),
#                 }
#                 for log in logs
#             ],
#         }

#     except Exception as e:
#         logger.exception("❌ Audit log fetch failed")
#         raise HTTPException(status_code=500, detail=str(e))

#     finally:
#         db.close()


# # ─────────────────────────────────────────────
# # HEALTH
# # ─────────────────────────────────────────────
# @app.get("/api/health")
# def health():
#     return {"status": "ok"}



# from __future__ import annotations

# import logging
# from typing import List

# from fastapi import FastAPI, HTTPException, Body
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel

# from agents.orchestrator import run_pipeline
# from intelligence.orchestrator import handle_auditor_query
# from tools.bq_tool import fetch_trades as fetch_bigquery_trades
# from tools.inmemory_tool import fetch_trades as fetch_inmemory_trades
# from db.relational import SessionLocal, AuditLog

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# class AuditQueryRequest(BaseModel):
#     query: str


# # 🚀 CHAT FLOW
# @app.post("/api/audit-query")
# async def audit_query(body: AuditQueryRequest):
#     result = await handle_auditor_query(body.query)

#     intent = result.get("intent", {})
#     plan = result.get("plan", {})
#     steps = plan.get("steps", [])

#     all_rows: List[dict] = []

#     for step in steps:
#         tool = step["tool"]
#         params = step.get("params", {})

#         if tool == "bigquery":
#             rows = fetch_bigquery_trades(**params)

#             # 🔥 PRIORITY FIX
#             if rows:
#                 all_rows = rows
#                 break

#         elif tool == "inmemory":
#             rows = fetch_inmemory_trades(**params)
#             all_rows.extend(rows)

#     if not all_rows:
#         return {
#             "response": "No real data found in BigQuery or sources.",
#             "intent": intent,
#             "plan": plan
#         }

#     pipeline_result = run_pipeline(all_rows)

#     return {
#         "response": result.get("response"),
#         "intent": intent,
#         "plan": plan,

#         "run_id": pipeline_result.get("run_id"),
#         "stats": pipeline_result.get("stats"),
#         "final_trades": pipeline_result.get("final_trades"),
#         "hitl_queue": pipeline_result.get("hitl_queue"),

#         "validation_results": pipeline_result.get("validation_results"),
#         "risk_results": pipeline_result.get("risk_results"),
#         "compliance_results": pipeline_result.get("compliance_results"),

#         "report_json": pipeline_result.get("report_json"),
#         "report_path": pipeline_result.get("report_path"),
#         "exception_report_path": pipeline_result.get("exception_report_path"),
#     }


# # 🚀 MERGE SOURCES
# @app.get("/api/sources/all")
# def fetch_all():
#     sql = """
#     SELECT *
#     FROM `deutschebank-aipocs.mifid_reporting.trade_execution_facts`
#     ORDER BY created_at DESC
#     LIMIT 100
#     """

#     rows = fetch_bigquery_trades(sql=sql)

#     return {
#         "count": len(rows),
#         "trades": rows
#     }


# # 🚀 PIPELINE
# @app.post("/api/run-pipeline")
# def run_pipeline_endpoint(body: dict = Body(...)):
#     trades = body.get("trades") or []

#     if not trades:
#         raise HTTPException(status_code=400, detail="No trades")

#     result = run_pipeline(trades)

#     return {
#         "run_id": result.get("run_id"),
#         "stats": result.get("stats"),

#         "final_trades": result.get("final_trades"),
#         "hitl_queue": result.get("hitl_queue"),
#         "corrections": result.get("corrections"),

#         "validation_results": result.get("validation_results"),
#         "risk_results": result.get("risk_results"),
#         "compliance_results": result.get("compliance_results"),

#         "report_json": result.get("report_json"),
#         "report_path": result.get("report_path"),
#         "exception_report_path": result.get("exception_report_path"),
#     }


# # 🚀 AUDIT LOG
# @app.get("/api/audit-log/{run_id}")
# def get_audit_log(run_id: str):
#     db = SessionLocal()

#     logs = db.query(AuditLog).filter(
#         AuditLog.run_id == run_id
#     ).all()

#     return {
#         "run_id": run_id,
#         "logs": [
#             {
#                 "step": l.step,
#                 "action": l.action,
#                 "details": l.details,
#                 "time": str(l.created_at)
#             }
#             for l in logs
#         ]
#     }

from __future__ import annotations

import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False"

import logging
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from config import get_settings
from db.relational import init_db
from rag import init_rag
from agents.orchestrator import run_pipeline
from intelligence.orchestrator import handle_auditor_query

# tools
from tools.bq_tool import fetch_trades as fetch_bigquery_trades
from tools.inmemory_tool import fetch_trades as fetch_inmemory_trades

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

app = FastAPI(title="MiFID II Agentic System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────
# STARTUP
# ─────────────────────────────────────────────
@app.on_event("startup")
def startup():
    logger.info("🚀 Starting System...")

    init_db()
    init_rag()

    Path(settings.reports_dir).mkdir(parents=True, exist_ok=True)

    logger.info("✅ System Ready")


# ─────────────────────────────────────────────
# MODELS
# ─────────────────────────────────────────────
class AuditQueryRequest(BaseModel):
    query: str
from datetime import date, datetime
from decimal import Decimal

def _json_safe(value):
    if value is None:
        return None
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, dict):
        return {k: _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_safe(v) for v in value]
    if isinstance(value, bytes):
        try:
            return value.decode("utf-8")
        except Exception:
            return str(value)
    return value

def _sanitize_row(row: dict) -> dict:
    return {k: _json_safe(v) for k, v in row.items()}

# ─────────────────────────────────────────────
# MAIN AUDIT FLOW
# ─────────────────────────────────────────────
@app.post("/api/audit-query")
async def audit_query(body: AuditQueryRequest):
    try:
        logger.info(f"📩 Query: {body.query}")

        result = await handle_auditor_query(body.query)

        intent = result.get("intent", {})
        plan = result.get("plan", {})
        steps = plan.get("steps", [])

        all_rows: List[dict] = []

        # 🔥 Execute tools
        for step in steps:
            tool = step.get("tool")
            params = step.get("params", {})

            logger.info(f"⚙️ Executing tool: {tool}")

            try:
                if tool == "inmemory":
                    rows = fetch_inmemory_trades(
                        filters=params.get("filters"),
                        limit=params.get("limit", 500),
                    )

                elif tool == "bigquery":
                    # ✅ FIXED: clean params (NO source_channel)
                    rows = fetch_bigquery_trades(
                        sql=params.get("sql"),
                        params=params.get("params"),
                        limit=params.get("limit", 100),
                    )

                else:
                    logger.warning(f"Unknown tool: {tool}")
                    continue

                for r in rows:
                    r["source_channel"] = tool

                logger.info(f"📊 {tool} returned {len(rows)} rows")
                all_rows.extend(rows)

            except Exception:
                logger.exception(f"❌ Tool failed: {tool}")
                continue

        # ✅ SAFE FALLBACK
        if not all_rows:
            return {
                "response": "No trades found in BigQuery or other sources.",
                "intent": intent,
                "plan": plan,
                "final_trades": [],
                "stats": {},
            }

        # 🔗 Merge rows
        merged = {}
        for row in all_rows:
            key = row.get("trade_id") or row.get("execution_id")
            if not key:
                continue

            if key not in merged:
                merged[key] = row
            else:
                merged[key].update({k: v for k, v in row.items() if v})

        final_rows = list(merged.values())

        logger.info(f"🔗 Merged rows: {len(final_rows)}")

        # 🚀 Run pipeline
        pipeline_result = run_pipeline(
            final_rows,
            source_channel="agentic_query",
        )

        return {
            "run_id": pipeline_result.get("run_id"),
            "stats": pipeline_result.get("stats"),
            "final_trades": pipeline_result.get("final_trades"),
            "hitl_queue": pipeline_result.get("hitl_queue"),
            "validation_results": pipeline_result.get("validation_results"),
            "risk_results": pipeline_result.get("risk_results"),
            "compliance_results": pipeline_result.get("compliance_results"),
            "report_path": pipeline_result.get("report_path"),
            "intent": intent,
            "plan": plan,
            "llm_response": result.get("response"),
        }

    except Exception as e:
        logger.exception("❌ Audit query failed")
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────
# MERGE SOURCES (UI)
# ─────────────────────────────────────────────
@app.get("/api/sources/all")
def fetch_all_trades():
    sql = """
    SELECT *
    FROM `deutschebank-aipocs.mifid_reporting.trade_execution_facts`
    ORDER BY created_at DESC
    LIMIT 100
    """

    trades = fetch_bigquery_trades(sql=sql)

    return {
        "source": "bigquery",
        "count": len(trades),
        "trades": trades,
    }


# ─────────────────────────────────────────────
# RUN PIPELINE FROM UI
# ─────────────────────────────────────────────
@app.post("/api/run-pipeline")
def run_pipeline_endpoint(body: dict = Body(...)):
    trades = body.get("trades") or []

    if not trades:
        raise HTTPException(status_code=400, detail="No trades provided")

    for t in trades:
        if "source_channel" not in t:
            t["source_channel"] = "ui"

    result = run_pipeline(trades, source_channel="ui")

    return {
        "success": True,
        "run_id": result.get("run_id"),
        "stats": result.get("stats"),
        "final_trades": result.get("final_trades"),
        "hitl_queue": result.get("hitl_queue"),
        "validation_results": result.get("validation_results"),
        "risk_results": result.get("risk_results"),
        "compliance_results": result.get("compliance_results"),
        "report_path": result.get("report_path"),
        "csv_path": result.get("csv_path"),
    }



from fastapi.responses import FileResponse
from pathlib import Path


@app.get("/api/report/{run_id}")
def get_report(run_id: str):
    reports_dir = Path(settings.reports_dir)

    # 🔍 find report file
    files = list(reports_dir.glob(f"*{run_id}*"))

    if not files:
        raise HTTPException(status_code=404, detail="Report not found")

    report_file = files[0]

    return FileResponse(
        path=report_file,
        filename=report_file.name,
        media_type="application/octet-stream",
    )
# ─────────────────────────────────────────────
# HEALTH
# ─────────────────────────────────────────────
@app.get("/api/health")
def health():
    return {"status": "ok"}