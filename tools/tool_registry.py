from __future__ import annotations

from tools.inmemory_tool import fetch_trades as fetch_inmemory_trades
from tools.bq_tool import fetch_trades as fetch_bigquery_trades

TOOL_REGISTRY = {
    "inmemory": fetch_inmemory_trades,
    "bigquery": fetch_bigquery_trades,
}