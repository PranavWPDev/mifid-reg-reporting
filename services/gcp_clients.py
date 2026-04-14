from __future__ import annotations

from functools import lru_cache

from google.cloud import bigquery

from config import get_settings


@lru_cache(maxsize=1)
def get_bigquery_client() -> bigquery.Client:
    settings = get_settings()
    if not settings.gcp_project_id:
        raise RuntimeError("GCP_PROJECT_ID is not set.")
    return bigquery.Client(project=settings.gcp_project_id)


def get_bigquery_table(table_name: str) -> str:
    settings = get_settings()
    if not settings.gcp_project_id:
        raise RuntimeError("GCP_PROJECT_ID is not set.")
    return f"{settings.gcp_project_id}.{settings.bq_dataset}.{table_name}"