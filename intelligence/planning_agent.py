from __future__ import annotations

from typing import Any, Dict, List

from intelligence.query_generator import build_bigquery_sql, build_inmemory_filters, build_source_plan


def planning_agent(intent: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert intent into an execution plan.

    This is the real planner:
    - chooses source order
    - generates source-specific params
    - keeps the plan deterministic and auditable
    """
    report_type = intent.get("report_type", "trade_lookup")
    source_plan = build_source_plan(intent)
    steps: List[Dict[str, Any]] = []

    for source in source_plan:
        if source == "inmemory":
            steps.append(
                {
                    "tool": "inmemory",
                    "params": {
                        "filters": build_inmemory_filters(intent),
                        "limit": 500,
                        "source_channel": "inmemory",
                        "source_system": "structured-intake-csv",
                        "source_ref": "manual",
                    },
                }
            )

        elif source == "bigquery":
            sql, params = build_bigquery_sql(intent)
            steps.append(
                {
                    "tool": "bigquery",
                    "params": {
                        "sql": sql,
                        "params": params,
                        "limit": 1000,
                        "source_channel": "bigquery",
                        "source_system": "gcp-bigquery",
                        "source_ref": "bigquery-query",
                    },
                }
            )

    return {
        "report_type": report_type,
        "source_plan": source_plan,
        "steps": steps,
    }