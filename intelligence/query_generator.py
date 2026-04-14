# from __future__ import annotations

# from datetime import datetime, timedelta, timezone
# from typing import Any, Dict, List, Tuple

# from config import get_settings


# _ALLOWED_REPORT_TYPES = {
#     "trade_lookup",
#     "exception_report",
#     "t1_sweep",
#     "compliance_summary",
#     "hitl_review",
#     "execution_report",
# }


# def _resolve_date_window(preset: str) -> Tuple[str, str]:
#     today = datetime.now(timezone.utc).date()
#     preset = (preset or "").lower().strip()

#     if preset == "today":
#         return today.isoformat(), today.isoformat()

#     if preset == "yesterday":
#         d = today - timedelta(days=1)
#         return d.isoformat(), d.isoformat()

#     if preset == "last_7_days":
#         d = today - timedelta(days=7)
#         return d.isoformat(), today.isoformat()

#     if preset == "this_month":
#         start = today.replace(day=1)
#         return start.isoformat(), today.isoformat()

#     if preset == "last_month":
#         first_this_month = today.replace(day=1)
#         last_prev_month = first_this_month - timedelta(days=1)
#         start_prev_month = last_prev_month.replace(day=1)
#         return start_prev_month.isoformat(), last_prev_month.isoformat()

#     return "", ""


# def normalize_filters(filters: Dict[str, Any]) -> Dict[str, Any]:
#     out = dict(filters or {})

#     for key in ["trade_id", "isin", "venue", "status", "execution_id", "report_status", "final_status"]:
#         if out.get(key) in ("", None, "null", "None"):
#             out[key] = None

#     date_window = out.get("date_window") or ""
#     date_from, date_to = _resolve_date_window(date_window)
#     if date_from and date_to:
#         out["date_from"] = date_from
#         out["date_to"] = date_to

#     return out


# def build_inmemory_filters(intent: Dict[str, Any]) -> Dict[str, Any]:
#     return normalize_filters(intent.get("filters") or {})


# def should_use_inmemory(intent: Dict[str, Any]) -> bool:
#     report_type = (intent.get("report_type") or "trade_lookup").strip()

#     if report_type in {"trade_lookup", "hitl_review"}:
#         return True

#     filters = intent.get("filters") or {}
#     return bool(
#         filters.get("trade_id")
#         or filters.get("isin")
#         or filters.get("venue")
#     )


# def should_use_bigquery(intent: Dict[str, Any]) -> bool:
#     report_type = (intent.get("report_type") or "trade_lookup").strip()

#     if report_type in {
#         "exception_report",
#         "t1_sweep",
#         "compliance_summary",
#         "execution_report",
#     }:
#         return True

#     filters = intent.get("filters") or {}
#     if filters.get("date_window") in {"yesterday", "last_7_days", "this_month", "last_month"}:
#         return True

#     return False


# def _apply_common_filters(
#     where: List[str],
#     params: Dict[str, Any],
#     filters: Dict[str, Any],
#     *,
#     table_kind: str,
# ) -> None:
#     """
#     table_kind:
#       - execution
#       - exceptions
#       - runs
#       - outcomes
#     """
#     date_from = filters.get("date_from")
#     date_to = filters.get("date_to")

#     if date_from and date_to:
#         if table_kind == "execution":
#             where.append(
#                 "DATE(COALESCE(executed_at, trade_datetime, created_at)) BETWEEN DATE(@date_from) AND DATE(@date_to)"
#             )
#         else:
#             where.append("DATE(created_at) BETWEEN DATE(@date_from) AND DATE(@date_to)")
#         params["date_from"] = date_from
#         params["date_to"] = date_to

#     if filters.get("trade_id"):
#         where.append("trade_id = @trade_id")
#         params["trade_id"] = filters["trade_id"]

#     if filters.get("isin") and table_kind in {"execution"}:
#         where.append("isin = @isin")
#         params["isin"] = filters["isin"]

#     if filters.get("venue") and table_kind in {"execution"}:
#         where.append("venue = @venue")
#         params["venue"] = filters["venue"]

#     if filters.get("report_status") and table_kind in {"execution"}:
#         where.append("report_status = @report_status")
#         params["report_status"] = filters["report_status"]

#     if filters.get("execution_id") and table_kind in {"execution"}:
#         where.append("execution_id = @execution_id")
#         params["execution_id"] = filters["execution_id"]

#     if filters.get("status"):
#         if table_kind == "execution":
#             where.append("report_status = @status")
#         elif table_kind == "exceptions":
#             where.append("status = @status")
#         elif table_kind == "outcomes":
#             where.append("final_status = @status")
#         elif table_kind == "runs":
#             where.append("status = @status")
#         params["status"] = filters["status"]

#     if filters.get("final_status") and table_kind == "outcomes":
#         where.append("final_status = @final_status")
#         params["final_status"] = filters["final_status"]


# def build_bigquery_sql(intent: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
#     settings = get_settings()
#     dataset = settings.bq_dataset
#     report_type = (intent.get("report_type") or "trade_lookup").strip()
#     filters = normalize_filters(intent.get("filters") or {})

#     project_id = settings.gcp_project_id.strip()
#     if not project_id:
#         raise RuntimeError("GCP_PROJECT_ID is not configured.")

#     table_lookup = f"`{project_id}.{dataset}.trade_execution_facts`"
#     table_exceptions = f"`{project_id}.{dataset}.trade_exception_records`"
#     table_runs = f"`{project_id}.{dataset}.trade_pipeline_runs`"
#     table_outcomes = f"`{project_id}.{dataset}.trade_final_outcomes`"

#     params: Dict[str, Any] = {}
#     where: List[str] = ["1=1"]

#     if report_type == "exception_report":
#         _apply_common_filters(where, params, filters, table_kind="exceptions")
#         sql = f"""
#         SELECT
#           run_id, trade_id, field, category, severity, description,
#           status, source_channel, created_at
#         FROM {table_exceptions}
#         WHERE {" AND ".join(where)}
#         ORDER BY created_at DESC
#         """
#         return sql.strip(), params

#     if report_type == "compliance_summary":
#         _apply_common_filters(where, params, filters, table_kind="runs")
#         sql = f"""
#         SELECT
#           run_id,
#           COUNT(*) AS total_runs,
#           SUM(total_trades) AS total_trades,
#           SUM(passed) AS passed,
#           SUM(hitl) AS hitl,
#           SUM(failed) AS failed,
#           SUM(auto_fixed) AS auto_fixed
#         FROM {table_runs}
#         WHERE {" AND ".join(where)}
#         GROUP BY run_id
#         ORDER BY run_id DESC
#         """
#         return sql.strip(), params

#     if report_type == "t1_sweep":
#         _apply_common_filters(where, params, filters, table_kind="execution")
#         sql = f"""
#         SELECT
#           trade_id, run_id, trade_datetime, isin, executing_entity_lei,
#           buyer_lei, seller_lei, price, currency, quantity, venue,
#           report_status, instrument_type, execution_id, execution_status,
#           execution_price, executed_quantity, executed_at,
#           source_channel, source_system, source_ref, batch_id, created_at
#         FROM {table_lookup}
#         WHERE {" AND ".join(where)}
#         ORDER BY COALESCE(executed_at, created_at) DESC
#         """
#         return sql.strip(), params

#     if report_type == "execution_report":
#         _apply_common_filters(where, params, filters, table_kind="execution")
#         sql = f"""
#         SELECT
#           trade_id, run_id, trade_datetime, isin, execution_id, execution_status,
#           execution_price, executed_quantity, executed_at,
#           source_channel, source_system, source_ref, batch_id, created_at
#         FROM {table_lookup}
#         WHERE {" AND ".join(where)}
#         ORDER BY COALESCE(executed_at, created_at) DESC
#         """
#         return sql.strip(), params

#     if report_type == "hitl_review":
#         _apply_common_filters(where, params, filters, table_kind="outcomes")
#         sql = f"""
#         SELECT
#           run_id, trade_id, final_status, decision_confidence, decision_reason,
#           confidence_label, auto_fix_status, source_channel, source_system,
#           source_ref, batch_id, created_at
#         FROM {table_outcomes}
#         WHERE {" AND ".join(where)}
#         ORDER BY created_at DESC
#         """
#         return sql.strip(), params

#     # Default = trade lookup
#     _apply_common_filters(where, params, filters, table_kind="execution")
#     sql = f"""
#     SELECT
#       trade_id, run_id, trade_datetime, isin, executing_entity_lei, buyer_lei, seller_lei,
#       price, currency, quantity, venue, report_status, instrument_type,
#       execution_id, execution_status, execution_price, executed_quantity,
#       executed_at, source_channel, source_system, source_ref, batch_id, created_at
#     FROM {table_lookup}
#     WHERE {" AND ".join(where)}
#     ORDER BY COALESCE(executed_at, created_at) DESC
#     """
#     return sql.strip(), params


# def build_source_plan(intent: Dict[str, Any]) -> List[str]:
#     sources: List[str] = []

#     if should_use_inmemory(intent):
#         sources.append("inmemory")

#     if should_use_bigquery(intent):
#         sources.append("bigquery")

#     if not sources:
#         sources = ["inmemory", "bigquery"]

#     deduped: List[str] = []
#     for src in sources:
#         if src not in deduped:
#             deduped.append(src)

#     return deduped

#-------------------------------------------------------------------------------------------------------------------

# from __future__ import annotations

# from typing import Any, Dict, List, Tuple

# from config import get_settings
# from utils.llm_json import call_llm_json


# # ─────────────────────────────────────────────
# # RAG CONTEXT
# # ─────────────────────────────────────────────
# SCHEMA_CONTEXT = """
# Tables:

# 1. trade_execution_facts
#    - report_status

# 2. trade_exception_records
#    - status

# 3. trade_final_outcomes
#    - final_status   <-- IMPORTANT

# Rules:
# - trade_execution_facts → use report_status
# - trade_exception_records → use status
# - trade_final_outcomes → use final_status
# """

# # ─────────────────────────────────────────────
# # LLM SQL GENERATOR
# # ─────────────────────────────────────────────
# def generate_sql_with_llm(query: str) -> Tuple[str, Dict[str, Any]]:
#     settings = get_settings()

#     project = settings.gcp_project_id
#     dataset = settings.bq_dataset

#     prompt = f"""
# You are a BigQuery SQL expert.

# {SCHEMA_CONTEXT}

# User query:
# {query}

# Rules:
# - Use full table path: `{project}.{dataset}.table_name`
# - Always use LIMIT 100
# - Use correct status values: FAILED, HITL, PASS

# Return JSON:
# {{
#   "sql": "...",
#   "params": {{}}
# }}
# """

#     fallback = {
#         "sql": f"""
#         SELECT *
#         FROM `{project}.{dataset}.trade_execution_facts`
#         LIMIT 50
#         """,
#         "params": {}
#     }

#     result, _ = call_llm_json(prompt, fallback, retries=2)

#     return result.get("sql", ""), result.get("params", {})


# # ─────────────────────────────────────────────
# # MAIN SQL BUILDER
# # ─────────────────────────────────────────────
# def build_bigquery_sql(intent: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
#     query_text = intent.get("query") or ""

#     sql, params = generate_sql_with_llm(query_text)

#     # 🔥 FIX: column correction
#     if "trade_final_outcomes" in sql and " status " in sql:
#         sql = sql.replace(" status ", " final_status ")

#     if "trade_execution_facts" in sql and " status " in sql:
#         sql = sql.replace(" status ", " report_status ")

#     print("\n🤖 FINAL SQL (POST FIX):")
#     print(sql)

#     return sql, params

# # ─────────────────────────────────────────────
# # BIGQUERY STEP
# # ─────────────────────────────────────────────
# def build_bigquery_step(intent: Dict[str, Any]) -> Dict[str, Any]:
#     sql, params = build_bigquery_sql(intent)

#     return {
#         "tool": "bigquery",
#         "params": {
#             "sql": sql,
#             "params": params,
#             "limit": 100,
#             "source_channel": "bigquery",
#         },
#     }


# # ─────────────────────────────────────────────
# # ✅ REQUIRED COMPATIBILITY FUNCTIONS
# # ─────────────────────────────────────────────

# # 🔥 FIX 1 (your current error)
# def build_source_plan(intent: Dict[str, Any]) -> List[str]:
#     return ["inmemory", "bigquery"]


# # 🔥 FIX 2 (previous error)
# def build_inmemory_filters(intent: Dict[str, Any]) -> Dict[str, Any]:
#     return intent.get("filters", {}) or {}




from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Tuple

from config import get_settings

_ALLOWED_REPORT_TYPES = {
    "trade_lookup",
    "exception_report",
    "t1_sweep",
    "compliance_summary",
    "hitl_review",
    "execution_report",
}


def _resolve_date_window(preset: str) -> Tuple[str, str]:
    today = datetime.now(timezone.utc).date()
    preset = (preset or "").lower().strip()

    if preset == "today":
        return today.isoformat(), today.isoformat()

    if preset == "yesterday":
        d = today - timedelta(days=1)
        return d.isoformat(), d.isoformat()

    if preset == "last_7_days":
        d = today - timedelta(days=7)
        return d.isoformat(), today.isoformat()

    if preset == "this_month":
        start = today.replace(day=1)
        return start.isoformat(), today.isoformat()

    if preset == "last_month":
        first_this_month = today.replace(day=1)
        last_prev_month = first_this_month - timedelta(days=1)
        start_prev_month = last_prev_month.replace(day=1)
        return start_prev_month.isoformat(), last_prev_month.isoformat()

    return "", ""


def normalize_filters(filters: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(filters or {})

    for key in ["trade_id", "isin", "venue", "status", "execution_id", "report_status", "final_status"]:
        if out.get(key) in ("", None, "null", "None"):
            out[key] = None

    date_window = out.get("date_window") or ""
    date_from, date_to = _resolve_date_window(date_window)
    if date_from and date_to:
        out["date_from"] = date_from
        out["date_to"] = date_to

    return out


def build_inmemory_filters(intent: Dict[str, Any]) -> Dict[str, Any]:
    return normalize_filters(intent.get("filters") or {})


def should_use_inmemory(intent: Dict[str, Any]) -> bool:
    report_type = (intent.get("report_type") or "trade_lookup").strip()

    if report_type in {"trade_lookup", "hitl_review"}:
        return True

    filters = intent.get("filters") or {}
    return bool(filters.get("trade_id") or filters.get("isin") or filters.get("venue"))


def should_use_bigquery(intent: Dict[str, Any]) -> bool:
    report_type = (intent.get("report_type") or "trade_lookup").strip()

    if report_type in {
        "exception_report",
        "t1_sweep",
        "compliance_summary",
        "execution_report",
        "trade_lookup",
    }:
        return True

    filters = intent.get("filters") or {}
    if filters.get("date_window") in {"yesterday", "last_7_days", "this_month", "last_month"}:
        return True

    return False


def build_bigquery_sql(intent: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    settings = get_settings()
    dataset = settings.bq_dataset
    report_type = (intent.get("report_type") or "trade_lookup").strip()
    filters = normalize_filters(intent.get("filters") or {})

    project_id = settings.gcp_project_id.strip()
    if not project_id:
        raise RuntimeError("GCP_PROJECT_ID is not configured.")

    table_lookup = f"`{project_id}.{dataset}.trade_execution_facts`"
    table_exceptions = f"`{project_id}.{dataset}.trade_exception_records`"
    table_runs = f"`{project_id}.{dataset}.trade_pipeline_runs`"
    table_outcomes = f"`{project_id}.{dataset}.trade_final_outcomes`"

    params: Dict[str, Any] = {}
    where: List[str] = ["1=1"]

    if report_type == "trade_lookup":
        if filters.get("trade_id"):
            where.append("trade_id = @trade_id")
            params["trade_id"] = filters["trade_id"]

        if filters.get("isin"):
            where.append("isin = @isin")
            params["isin"] = filters["isin"]

        if filters.get("venue"):
            where.append("venue = @venue")
            params["venue"] = filters["venue"]

        sql = f"""
        SELECT
          trade_id, run_id, trade_datetime, isin,
          executing_entity_lei, buyer_lei, seller_lei,
          price, currency, quantity, venue,
          report_status, instrument_type,
          execution_id, execution_status,
          execution_price, executed_quantity, executed_at,
          source_channel, source_system, source_ref, batch_id, created_at
        FROM {table_lookup}
        WHERE {" AND ".join(where)}
        ORDER BY COALESCE(executed_at, trade_datetime, created_at) DESC
        """
        return sql.strip(), params

    if report_type == "exception_report":
        if filters.get("trade_id"):
            where.append("trade_id = @trade_id")
            params["trade_id"] = filters["trade_id"]

        if filters.get("status"):
            where.append("status = @status")
            params["status"] = filters["status"]

        sql = f"""
        SELECT
          run_id, trade_id, field, category, severity, description,
          status, source_channel, created_at
        FROM {table_exceptions}
        WHERE {" AND ".join(where)}
        ORDER BY created_at DESC
        """
        return sql.strip(), params

    if report_type == "compliance_summary":
        if filters.get("status"):
            where.append("status = @status")
            params["status"] = filters["status"]

        sql = f"""
        SELECT
          run_id,
          COUNT(*) AS total_runs,
          SUM(total_trades) AS total_trades,
          SUM(passed) AS passed,
          SUM(hitl) AS hitl,
          SUM(failed) AS failed,
          SUM(auto_fixed) AS auto_fixed
        FROM {table_runs}
        WHERE {" AND ".join(where)}
        GROUP BY run_id
        ORDER BY run_id DESC
        """
        return sql.strip(), params

    if report_type == "t1_sweep":
        if filters.get("trade_id"):
            where.append("trade_id = @trade_id")
            params["trade_id"] = filters["trade_id"]

        if filters.get("venue"):
            where.append("venue = @venue")
            params["venue"] = filters["venue"]

        if filters.get("date_from") and filters.get("date_to"):
            where.append(
                "DATE(COALESCE(executed_at, trade_datetime, created_at)) BETWEEN DATE(@date_from) AND DATE(@date_to)"
            )
            params["date_from"] = filters["date_from"]
            params["date_to"] = filters["date_to"]

        sql = f"""
        SELECT
          trade_id, run_id, trade_datetime, isin, executing_entity_lei,
          buyer_lei, seller_lei, price, currency, quantity, venue,
          report_status, instrument_type, execution_id, execution_status,
          execution_price, executed_quantity, executed_at,
          source_channel, source_system, source_ref, batch_id, created_at
        FROM {table_lookup}
        WHERE {" AND ".join(where)}
        ORDER BY COALESCE(executed_at, created_at) DESC
        """
        return sql.strip(), params

    if report_type == "execution_report":
        if filters.get("trade_id"):
            where.append("trade_id = @trade_id")
            params["trade_id"] = filters["trade_id"]

        sql = f"""
        SELECT
          trade_id, run_id, trade_datetime, isin, execution_id, execution_status,
          execution_price, executed_quantity, executed_at,
          source_channel, source_system, source_ref, batch_id, created_at
        FROM {table_lookup}
        WHERE {" AND ".join(where)}
        ORDER BY COALESCE(executed_at, trade_datetime, created_at) DESC
        """
        return sql.strip(), params

    if report_type == "hitl_review":
        if filters.get("trade_id"):
            where.append("trade_id = @trade_id")
            params["trade_id"] = filters["trade_id"]

        sql = f"""
        SELECT
          run_id, trade_id, final_status, decision_confidence, decision_reason,
          confidence_label, auto_fix_status, source_channel, source_system,
          source_ref, batch_id, created_at
        FROM {table_outcomes}
        WHERE {" AND ".join(where)}
        ORDER BY created_at DESC
        """
        return sql.strip(), params

    sql = f"""
    SELECT
      trade_id, run_id, trade_datetime, isin, executing_entity_lei, buyer_lei, seller_lei,
      price, currency, quantity, venue, report_status, instrument_type,
      execution_id, execution_status, execution_price, executed_quantity,
      executed_at, source_channel, source_system, source_ref, batch_id, created_at
    FROM {table_lookup}
    WHERE {" AND ".join(where)}
    ORDER BY COALESCE(executed_at, trade_datetime, created_at) DESC
    """
    return sql.strip(), params


def build_source_plan(intent: Dict[str, Any]) -> List[str]:
    sources: List[str] = []

    if should_use_inmemory(intent):
        sources.append("inmemory")

    if should_use_bigquery(intent):
        sources.append("bigquery")

    if not sources:
        sources = ["inmemory", "bigquery"]

    deduped: List[str] = []
    for src in sources:
        if src not in deduped:
            deduped.append(src)

    return deduped