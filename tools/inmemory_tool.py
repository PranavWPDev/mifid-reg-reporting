from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from config import get_settings

_SAMPLE_ROWS = [
    {
        "trade_id": "T1001",
        "trade_datetime": "2026-04-09T06:15:00Z",
        "isin": "US0378331005",
        "executing_entity_lei": "5493001KJTIIGC8Y1R12",
        "buyer_lei": "5493001KJTIIGC8Y1R13",
        "seller_lei": "5493001KJTIIGC8Y1R14",
        "price": "150.25",
        "currency": "USD",
        "quantity": "100",
        "venue": "XNAS",
        "report_status": "NEWT",
        "instrument_type": "EQUITY",
        "source_channel": "inmemory",
        "source_system": "structured-intake-csv",
        "source_ref": "manual",
        "batch_id": "BATCH-001",
        "received_at": "2026-04-09T06:15:00Z",
    },
    {
        "trade_id": "T1002",
        "trade_datetime": "2026-04-09T07:00:00Z",
        "isin": "DE0007164600",
        "executing_entity_lei": "529900T8BM49AURSDO55",
        "buyer_lei": "529900T8BM49AURSDO56",
        "seller_lei": "529900T8BM49AURSDO57",
        "price": "142.10",
        "currency": "EUR",
        "quantity": "200",
        "venue": "XETR",
        "report_status": "AMND",
        "instrument_type": "EQUITY",
        "source_channel": "inmemory",
        "source_system": "structured-intake-csv",
        "source_ref": "manual",
        "batch_id": "BATCH-001",
        "received_at": "2026-04-09T07:00:00Z",
    },
    {
        "trade_id": "T1003",
        "trade_datetime": "2026-04-09T08:30:00Z",
        "isin": "GB0005405286",
        "executing_entity_lei": "5493001KJTIIGC8Y1R20",
        "buyer_lei": "5493001KJTIIGC8Y1R21",
        "seller_lei": "5493001KJTIIGC8Y1R22",
        "price": "650.00",
        "currency": "GBP",
        "quantity": "100",
        "venue": "XLON",
        "report_status": "CANC",
        "instrument_type": "EQUITY",
        "source_channel": "inmemory",
        "source_system": "structured-intake-csv",
        "source_ref": "manual",
        "batch_id": "BATCH-001",
        "received_at": "2026-04-09T08:30:00Z",
    },
    {
        "trade_id": "T1004",
        "trade_datetime": "2026-04-09T09:00:00Z",
        "isin": "US5949181045",
        "executing_entity_lei": "5493001KJTIIGC8Y1R30",
        "buyer_lei": "5493001KJTIIGC8Y1R30",
        "seller_lei": "5493001KJTIIGC8Y1R30",
        "price": "0",
        "currency": "USD",
        "quantity": "0",
        "venue": "XNAS",
        "report_status": "NEWT",
        "instrument_type": "EQUITY",
        "source_channel": "inmemory",
        "source_system": "structured-intake-csv",
        "source_ref": "manual",
        "batch_id": "BATCH-001",
        "received_at": "2026-04-09T09:00:00Z",
    },
]


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ensure_sample_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return

    fieldnames = list(_SAMPLE_ROWS[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(_SAMPLE_ROWS)


def _safe_float(value: Any) -> Any:
    if value in (None, ""):
        return value
    try:
        return float(value)
    except Exception:
        return value


def _coerce_row(row: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(row)

    out["price"] = _safe_float(out.get("price"))
    out["quantity"] = _safe_float(out.get("quantity"))

    out.setdefault("source_channel", "inmemory")
    out.setdefault("source_system", "structured-intake-csv")
    out.setdefault("source_ref", "manual")
    out.setdefault("batch_id", "BATCH-001")
    out.setdefault("received_at", _utc_now_iso())

    trade_id = str(out.get("trade_id") or "UNKNOWN")
    batch_id = str(out.get("batch_id") or "BATCH")
    out.setdefault("trace_id", f"{batch_id}-{trade_id}")

    return out


def _matches_filters(row: Dict[str, Any], filters: Dict[str, Any]) -> bool:
    if filters.get("trade_id") and str(row.get("trade_id")) != str(filters["trade_id"]):
        return False
    if filters.get("isin") and str(row.get("isin")) != str(filters["isin"]):
        return False
    if filters.get("status") and str(row.get("report_status")) != str(filters["status"]):
        return False
    if filters.get("venue") and str(row.get("venue")) != str(filters["venue"]):
        return False
    if filters.get("instrument_type") and str(row.get("instrument_type")) != str(filters["instrument_type"]):
        return False

    date_from = filters.get("date_from")
    date_to = filters.get("date_to")
    if date_from or date_to:
        trade_dt = str(row.get("trade_datetime") or "")[:10]
        if date_from and trade_dt < str(date_from):
            return False
        if date_to and trade_dt > str(date_to):
            return False

    return True


def fetch_trades(
    filters: Optional[Dict[str, Any]] = None,
    limit: Optional[int] = None,
    **kwargs,
) -> List[dict]:
    """
    Read the structured intake CSV and return normalized trade dictionaries.
    Extra kwargs are accepted for planner compatibility and ignored.
    """
    settings = get_settings()
    csv_path = Path(settings.inmemory_csv_path)

    _ensure_sample_csv(csv_path)

    with csv_path.open("r", encoding="utf-8") as f:
        rows = [dict(r) for r in csv.DictReader(f)]

    records = [_coerce_row(r) for r in rows]
    filters = filters or {}

    result: List[dict] = []
    for row in records:
        if not _matches_filters(row, filters):
            continue
        result.append(row)
        if limit and len(result) >= int(limit):
            break

    return result