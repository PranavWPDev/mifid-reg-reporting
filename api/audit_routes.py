from __future__ import annotations

from typing import Any, Dict, List, Optional

from google.cloud import bigquery

from services.gcp_clients import get_bigquery_client


def _infer_bq_type(value: Any) -> str:
    if isinstance(value, bool):
        return "BOOL"
    if isinstance(value, int):
        return "INT64"
    if isinstance(value, float):
        return "FLOAT64"
    return "STRING"


def _build_query_job_config(params: Dict[str, Any]) -> bigquery.QueryJobConfig:
    query_parameters = []
    for key, value in (params or {}).items():
        if value is None:
            continue
        query_parameters.append(
            bigquery.ScalarQueryParameter(key, _infer_bq_type(value), value)
        )
    return bigquery.QueryJobConfig(query_parameters=query_parameters)


def _normalize_row(row: Dict[str, Any]) -> Dict[str, Any]:
    record = dict(row)

    # Ensure traceability fields exist even if source table is missing them
    record.setdefault("source_channel", "bigquery")
    record.setdefault("source_system", "gcp-bigquery")
    record.setdefault("source_ref", "bigquery-query")
    record.setdefault("batch_id", "")

    return record


def fetch_trades(
    sql: str,
    params: Optional[Dict[str, Any]] = None,
    limit: Optional[int] = None,
    **kwargs,  # ✅ IMPORTANT FIX
) -> List[dict]:
    """
    Execute a BigQuery SQL statement and return normalized rows.
    Accepts extra kwargs for agent compatibility.
    """
    client = get_bigquery_client()

    query_sql = sql.strip()
    if limit and "LIMIT" not in query_sql.upper():
        query_sql = f"{query_sql}\nLIMIT {int(limit)}"

    job_config = _build_query_job_config(params or {})
    rows = client.query(query_sql, job_config=job_config).result()

    out: List[dict] = []
    for row in rows:
        record = _normalize_row(dict(row.items()))
        out.append(record)

    return out
    """
    Execute a BigQuery SQL statement and return normalized rows.

    Intended for execution facts, pipeline summaries, exceptions, and audit-style reporting.
    """
    client = get_bigquery_client()

    query_sql = sql.strip()
    if limit and "LIMIT" not in query_sql.upper():
        query_sql = f"{query_sql}\nLIMIT {int(limit)}"

    job_config = _build_query_job_config(params or {})
    rows = client.query(query_sql, job_config=job_config).result()

    out: List[dict] = []
    for row in rows:
        record = _normalize_row(dict(row.items()))
        out.append(record)

    return out