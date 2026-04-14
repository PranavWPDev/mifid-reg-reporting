from __future__ import annotations

import csv
import io
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_batch_id() -> str:
    return str(uuid.uuid4())[:8].upper()


def _as_trade_list(payload: Any) -> List[dict]:
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]

    if isinstance(payload, dict):
        if isinstance(payload.get("trade_data"), list):
            return [x for x in payload["trade_data"] if isinstance(x, dict)]
        if isinstance(payload.get("trades"), list):
            return [x for x in payload["trades"] if isinstance(x, dict)]
        return [payload]

    return []


def normalize_trade(
    trade: dict,
    *,
    source_channel: str,
    source_system: str = "unknown",
    source_ref: str = "",
    batch_id: str = "",
) -> dict:
    normalized = dict(trade)

    # Preserve any trade-level metadata already present.
    normalized["source_channel"] = normalized.get("source_channel") or source_channel
    normalized["source_system"] = normalized.get("source_system") or source_system
    normalized["source_ref"] = normalized.get("source_ref") or source_ref
    normalized["batch_id"] = normalized.get("batch_id") or batch_id
    normalized["received_at"] = normalized.get("received_at") or utc_now_iso()

    return normalized


class ChannelRouter:
    """
    Normalizes all input channels into a single envelope contract.
    """

    def build_envelope(
        self,
        payload: Any,
        *,
        source_channel: str,
        source_system: str = "unknown",
        source_ref: str = "",
    ) -> dict:
        batch_id = new_batch_id()
        trade_list = _as_trade_list(payload)

        normalized_trades = [
            normalize_trade(
                t,
                source_channel=source_channel,
                source_system=source_system,
                source_ref=source_ref,
                batch_id=batch_id,
            )
            for t in trade_list
        ]

        return {
            "batch_id": batch_id,
            "source_channel": source_channel,
            "source_system": source_system,
            "source_ref": source_ref,
            "received_at": utc_now_iso(),
            "trade_data": normalized_trades,
        }

    def from_ui(self, payload: Any) -> dict:
        return self.build_envelope(
            payload,
            source_channel="ui",
            source_system="react-ui",
            source_ref="manual",
        )

    def from_rest_api(self, payload: Any) -> dict:
        return self.build_envelope(
            payload,
            source_channel="rest",
            source_system="trading-api",
            source_ref="rest-request",
        )

    def from_pubsub(self, payload_text: str, message_id: str = "") -> dict:
        payload = json.loads(payload_text)
        return self.build_envelope(
            payload,
            source_channel="pubsub",
            source_system="pubsub-topic",
            source_ref=message_id,
        )

    def from_gcs_csv(self, csv_text: str, file_name: str) -> dict:
        reader = csv.DictReader(io.StringIO(csv_text))
        rows = [dict(row) for row in reader]
        return self.build_envelope(
            rows,
            source_channel="gcs",
            source_system="cloud-storage",
            source_ref=file_name,
        )

    def from_gcs_json(self, json_text: str, file_name: str) -> dict:
        payload = json.loads(json_text)
        return self.build_envelope(
            payload,
            source_channel="gcs",
            source_system="cloud-storage",
            source_ref=file_name,
        )

    def from_scheduler(self, payload: Any) -> dict:
        return self.build_envelope(
            payload,
            source_channel="scheduler",
            source_system="cloud-scheduler",
            source_ref="t1-sweep",
        )