# data_sources.py

from typing import List


# ─── SOURCE A: In-Memory Database ─────────────────────────────────────────────

IN_MEMORY_DB: List[dict] = [

    # ✅ PASS TRADE
    {
        "trade_id": "DB_PASS_001",
        "trade_datetime": "2026-04-09T09:00:00Z",
        "reporting_datetime": "2026-04-09T10:00:00Z",  # within T+1
        "isin": "US0378331005",
        "executing_entity_lei": "5493001KJTIIGC8Y1R12",
        "buyer_lei": "213800D1EI4B9WTWWD28",
        "seller_lei": "529900T8BM49AURSDO55",
        "price": 180,
        "currency": "USD",
        "quantity": 30,
        "venue": "XNAS",
        "notional_amount": 5400,
        "report_status": "NEWT",
        "instrument_type": "EQUITY",
        "_source": "in_memory_db",
        "_source_label": "Trading System DB"
    },

    # ⚠️ HITL TRADE (late reporting)
    {
        "trade_id": "DB_HITL_001",
        "trade_datetime": "2024-03-10T09:00:00Z",
        "reporting_datetime": "2026-04-08T10:00:00Z",  # ❌ very late
        "isin": "US5949181045",
        "executing_entity_lei": "213800D1EI4B9WTWWD28",
        "buyer_lei": "5493001KJTIIGC8Y1R12",
        "seller_lei": "529900T8BM49AURSDO55",
        "price": 420,
        "currency": "USD",
        "quantity": 50,
        "venue": "XNAS",
        "notional_amount": 21000,
        "report_status": "NEWT",
        "instrument_type": "EQUITY",
        "_source": "in_memory_db",
        "_source_label": "Trading System DB"
    },

    # ❌ FAIL TRADE (invalid data)
    {
        "trade_id": "DB_FAIL_001",
        "trade_datetime": "2026-04-07T11:00:00Z",
        "reporting_datetime": "2026-04-07T12:00:00Z",
        "isin": "INVALID123",
        "executing_entity_lei": "BADLEI",
        "buyer_lei": "213800D1EI4B9WTWWD28",
        "seller_lei": "529900T8BM49AURSDO55",
        "price": -50,
        "currency": "XXX",
        "quantity": -10,
        "venue": "UNKNOWN",
        "notional_amount": 500,
        "report_status": "WRONG",
        "instrument_type": "EQUITY",
        "_source": "in_memory_db",
        "_source_label": "Trading System DB"
    },
]


def get_db_trades() -> List[dict]:
    """Return all trades from the in-memory trading system database."""
    return [dict(t) for t in IN_MEMORY_DB]

# ─── SOURCE B: CSV File ────────────────────────────────────────────────────────
import csv

CSV_FILE_PATH = "/home/pendharipranav_vilas/mifid-poc/backend/data/sampleTrades.csv"


def get_csv_trades():
    trades = []

    with open(CSV_FILE_PATH, "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            row["_source"] = "csv_file"
            row["_source_label"] = "CSV File"
            trades.append(row)

    return trades