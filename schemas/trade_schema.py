from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class TradeRecord(BaseModel):
    trade_id: str
    trade_datetime: Optional[str] = None
    isin: Optional[str] = None
    executing_entity_lei: Optional[str] = None
    buyer_lei: Optional[str] = None
    seller_lei: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    quantity: Optional[float] = None
    venue: Optional[str] = None
    report_status: Optional[str] = None
    instrument_type: Optional[str] = None

    execution_id: Optional[str] = None
    execution_status: Optional[str] = None
    execution_price: Optional[float] = None
    executed_quantity: Optional[float] = None
    executed_at: Optional[str] = None

    source_channel: str = "inmemory"
    source_system: str = "structured-intake-csv"
    source_ref: str = "manual"
    batch_id: str = ""
    received_at: Optional[str] = None
    trace_id: Optional[str] = None

    payload_json: Optional[str] = None


class AuditQueryRequest(BaseModel):
    query: str = Field(min_length=1, max_length=1000)


class AuditQueryResponse(BaseModel):
    response: str
    run_id: Optional[str] = None
    stats: Dict[str, Any] = Field(default_factory=dict)
    source_breakdown: Dict[str, int] = Field(default_factory=dict)
    report_path: Optional[str] = None
    csv_path: Optional[str] = None
    exception_report_path: Optional[str] = None


class IntentResult(BaseModel):
    report_type: Literal[
        "trade_lookup",
        "exception_report",
        "t1_sweep",
        "compliance_summary",
        "hitl_review",
        "execution_report",
    ]
    filters: Dict[str, Any] = Field(default_factory=dict)
    data_sources_needed: List[Literal["inmemory", "bigquery"]] = Field(default_factory=list)
    reasoning: str = ""
    confidence: float = 0.5


class PlanStep(BaseModel):
    tool: Literal["inmemory", "bigquery"]
    params: Dict[str, Any] = Field(default_factory=dict)