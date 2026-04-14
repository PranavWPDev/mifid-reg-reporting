

# from __future__ import annotations

# from typing import Any, Dict, List

# from google.cloud import bigquery


# # ─────────────────────────────────────────────
# # TYPE INFERENCE FOR BQ PARAMS
# # ─────────────────────────────────────────────
# def _infer_bq_type(value: Any) -> str:
#     if isinstance(value, bool):
#         return "BOOL"
#     if isinstance(value, int):
#         return "INT64"
#     if isinstance(value, float):
#         return "FLOAT64"
#     return "STRING"


# # ─────────────────────────────────────────────
# # NORMALIZE OUTPUT ROW
# # ─────────────────────────────────────────────
# def _normalize_row(row: Dict[str, Any]) -> Dict[str, Any]:
#     record = dict(row)

#     record.setdefault("source_channel", "bigquery")
#     record.setdefault("source_system", "gcp-bigquery")
#     record.setdefault("source_ref", "bigquery-query")
#     record.setdefault("batch_id", "")

#     return record


# # ─────────────────────────────────────────────
# # MAIN FETCH FUNCTION
# # ─────────────────────────────────────────────
# def fetch_trades(
#     sql: str = "",
#     params: Dict[str, Any] = None,
#     limit: int = 100,
#     **kwargs  # ✅ IMPORTANT: prevents crash from extra args
# ) -> List[Dict[str, Any]]:

#     print("\n🚀 BQ TOOL CALLED")
#     print("📄 SQL:\n", sql)
#     print("📦 PARAMS:", params)

#     try:
#         # ✅ Create BigQuery client (uses ADC)
#         client = bigquery.Client()
#         print("✅ BigQuery client initialized")

#         query_sql = (sql or "").strip()

#         if not query_sql:
#             print("⚠️ Empty SQL received")
#             return []

#         # ✅ Add LIMIT if not present
#         if limit and "LIMIT" not in query_sql.upper():
#             query_sql += f"\nLIMIT {int(limit)}"

#         # ─────────────────────────────────────
#         # BUILD PARAMS
#         # ─────────────────────────────────────
#         job_config = bigquery.QueryJobConfig()

#         if params:
#             query_parameters = []

#             for key, value in params.items():
#                 if value is None:
#                     continue

#                 param_type = _infer_bq_type(value)

#                 query_parameters.append(
#                     bigquery.ScalarQueryParameter(key, param_type, value)
#                 )

#             job_config.query_parameters = query_parameters

#         # ─────────────────────────────────────
#         # EXECUTE QUERY
#         # ─────────────────────────────────────
#         print("🚀 Executing query...")
#         query_job = client.query(query_sql, job_config=job_config)

#         results = list(query_job.result())

#         print(f"✅ Rows fetched: {len(results)}")

#         # ─────────────────────────────────────
#         # NORMALIZE RESULTS
#         # ─────────────────────────────────────
#         output: List[Dict[str, Any]] = []

#         for row in results:
#             record = _normalize_row(dict(row))
#             output.append(record)

#         return output

#     except Exception as e:
#         print("❌ BQ ERROR:", str(e))
#         return []






# from typing import Any, Dict, List
# from google.cloud import bigquery


# def fetch_trades(sql: str = "", params: dict = None, limit: int = 100):
#     print("\n🚀 BQ TOOL CALLED")
#     print("SQL:\n", sql)
#     print("PARAMS:", params)

#     try:
#         client = bigquery.Client()
#         print("✅ BigQuery client initialized")

#         if not sql:
#             return []

#         if limit and "LIMIT" not in sql.upper():
#             sql += f"\nLIMIT {limit}"

#         job = client.query(sql)
#         rows = list(job.result())

#         print(f"✅ Rows fetched: {len(rows)}")

#         return [dict(row) for row in rows]

#     except Exception as e:
#         print("❌ BQ ERROR:", str(e))
#         return []


#-----------------------------------------------------------------------------------
# from __future__ import annotations

# from typing import Any, Dict, List, Optional

# from config import get_settings

# try:
#     from google.cloud import bigquery
# except Exception:
#     bigquery = None


# def fetch_trades(
#     sql: Optional[str] = None,
#     params: Optional[Dict[str, Any]] = None,
#     limit: int = 100,
#     **kwargs,  # ✅ prevents crash from extra params
# ) -> List[Dict[str, Any]]:
#     """
#     Fetch trades from BigQuery safely
#     """

#     print("\n🚀 BQ TOOL CALLED")
#     print("SQL:\n", sql)
#     print("PARAMS:", params)

#     if bigquery is None:
#         print("❌ BigQuery not installed")
#         return []

#     try:
#         settings = get_settings()
#         client = bigquery.Client(project=settings.gcp_project_id)

#         print("✅ BigQuery client initialized")

#         if not sql:
#             print("⚠️ No SQL provided")
#             return []

#         # ✅ Ensure LIMIT exists
#         if limit and "LIMIT" not in sql.upper():
#             sql = f"{sql.strip()}\nLIMIT {limit}"

#         query_job = client.query(sql)
#         rows = list(query_job.result())

#         print(f"✅ Rows fetched: {len(rows)}")

#         return [dict(row) for row in rows]

#     except Exception as e:
#         print("❌ BQ ERROR:", str(e))
#         return []



from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional

from config import get_settings

try:
    from google.cloud import bigquery
except Exception:  # pragma: no cover
    bigquery = None


def _json_safe(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, bytes):
        try:
            return value.decode("utf-8")
        except Exception:
            return str(value)
    if isinstance(value, dict):
        return {k: _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_safe(v) for v in value]
    return value


def _infer_bq_type(value: Any) -> str:
    if isinstance(value, bool):
        return "BOOL"
    if isinstance(value, int):
        return "INT64"
    if isinstance(value, float):
        return "FLOAT64"
    return "STRING"


def _build_query_job_config(params: Optional[Dict[str, Any]]) -> "bigquery.QueryJobConfig":
    query_parameters = []
    for key, value in (params or {}).items():
        if value is None:
            continue
        query_parameters.append(
            bigquery.ScalarQueryParameter(key, _infer_bq_type(value), value)
        )
    return bigquery.QueryJobConfig(query_parameters=query_parameters)


def _normalize_row(row: Dict[str, Any]) -> Dict[str, Any]:
    record = _json_safe(dict(row))
    record.setdefault("source_channel", "bigquery")
    record.setdefault("source_system", "gcp-bigquery")
    record.setdefault("source_ref", "bigquery-query")
    record.setdefault("batch_id", "")
    return record


def fetch_trades(
    sql: str = "",
    params: Optional[Dict[str, Any]] = None,
    limit: int = 100,
    **kwargs,
) -> List[Dict[str, Any]]:
    """
    Fetch rows from BigQuery and return JSON-safe dictionaries.
    Extra kwargs are ignored safely.
    """
    print("\n🚀 BQ TOOL CALLED")
    print("SQL:\n", sql)
    print("PARAMS:", params)

    if bigquery is None:
        print("❌ google-cloud-bigquery is not installed")
        return []

    query_sql = (sql or "").strip()
    if not query_sql:
        return []

    try:
        settings = get_settings()
        if not settings.gcp_project_id:
            raise RuntimeError("GCP_PROJECT_ID is not configured")

        client = bigquery.Client(project=settings.gcp_project_id)
        print("✅ BigQuery client initialized")

        if limit and "LIMIT" not in query_sql.upper():
            query_sql = f"{query_sql}\nLIMIT {int(limit)}"

        job_config = _build_query_job_config(params or {})
        rows = client.query(query_sql, job_config=job_config).result()

        out: List[dict] = []
        for row in rows:
            out.append(_normalize_row(dict(row.items())))

        print(f"✅ Rows fetched: {len(out)}")
        return out

    except Exception as e:
        print("❌ BQ ERROR:", str(e))
        return []


