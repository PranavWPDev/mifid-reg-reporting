import csv
import datetime
import io
import json
import os
from typing import Any, Dict, List

from config import get_settings
from db.relational import SessionLocal, AuditLog, RunMetadata
from utils.llm_json import call_llm_json


def _safe_json_loads(text: str, fallback: Dict[str, Any]) -> Dict[str, Any]:
    cleaned = (text or "").strip().replace("```json", "").replace("```", "").strip()

    candidates = [cleaned]
    first = cleaned.find("{")
    last = cleaned.rfind("}")

    if first != -1 and last != -1 and last > first:
        candidates.append(cleaned[first:last + 1])

    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            continue

    return fallback


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def _safe_list_of_dicts(value: Any) -> List[dict]:
    if not isinstance(value, list):
        return []

    cleaned_rows: List[dict] = []
    for item in value:
        if isinstance(item, dict):
            cleaned_rows.append(item)
        elif isinstance(item, str):
            try:
                parsed = json.loads(item)
                if isinstance(parsed, dict):
                    cleaned_rows.append(parsed)
            except Exception:
                continue

    return cleaned_rows


def _make_row_from_trade(trade: dict) -> dict:
    row = {k: _stringify(v) for k, v in trade.items()}

    normalized_trade = trade.get("normalized_trade")
    if isinstance(normalized_trade, dict):
        for k, v in normalized_trade.items():
            row.setdefault(f"normalized_{k}", _stringify(v))

    corrections = trade.get("corrections")
    if isinstance(corrections, list):
        row["corrections"] = _stringify(corrections)

    row["auto_fix_status"] = _stringify(trade.get("auto_fix_status"))
    row["auto_fix_applied"] = _stringify(trade.get("auto_fix_applied"))
    return row


def _derive_csv_rows(state: dict, report_json: dict) -> List[dict]:
    csv_rows = _safe_list_of_dicts(report_json.get("csv_rows"))
    if csv_rows:
        return [_make_row_from_trade(r) for r in csv_rows]

    report_records = _safe_list_of_dicts(report_json.get("report_records"))
    if report_records:
        derived: List[dict] = []
        for record in report_records:
            row: Dict[str, Any] = {}

            row["trade_id"] = _stringify(record.get("trade_id"))
            row["final_status"] = _stringify(record.get("final_status") or record.get("status"))
            row["decision_reason"] = _stringify(record.get("decision_reason"))
            row["decision_confidence"] = _stringify(record.get("decision_confidence"))
            row["passed"] = _stringify(record.get("passed"))
            row["compliant"] = _stringify(record.get("compliant"))
            row["risk_level"] = _stringify(record.get("risk_level"))
            row["confidence"] = _stringify(record.get("confidence"))
            row["auto_fix_status"] = _stringify(record.get("auto_fix_status"))
            row["auto_fix_applied"] = _stringify(record.get("auto_fix_applied"))
            row["corrections"] = _stringify(record.get("corrections"))
            row["source_channel"] = _stringify(record.get("source_channel"))
            row["trace_id"] = _stringify(record.get("trace_id"))

            nested = record.get("normalized_fields") or record.get("trade_details") or record.get("normalized_trade") or {}
            if isinstance(nested, dict):
                for k, v in nested.items():
                    row.setdefault(k, _stringify(v))

            for k, v in record.items():
                if k in {"normalized_fields", "trade_details", "normalized_trade"}:
                    continue
                if isinstance(v, (dict, list)):
                    continue
                row.setdefault(k, _stringify(v))

            derived.append(row)

        if derived:
            return derived

    final_trades = state.get("final_trades", [])
    if isinstance(final_trades, list):
        return [_make_row_from_trade(t) for t in final_trades if isinstance(t, dict)]

    return []


def _build_csv_text(csv_rows: List[dict]) -> str:
    if not csv_rows:
        return ""

    cleaned_rows: List[dict] = []
    for row in csv_rows:
        if isinstance(row, dict):
            cleaned_rows.append({k: _stringify(v) for k, v in row.items()})
        elif isinstance(row, str):
            try:
                parsed = json.loads(row)
                if isinstance(parsed, dict):
                    cleaned_rows.append({k: _stringify(v) for k, v in parsed.items()})
            except Exception:
                continue

    if not cleaned_rows:
        return ""

    fieldnames: List[str] = []
    seen = set()
    for row in cleaned_rows:
        for key in row.keys():
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)

    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()

    for row in cleaned_rows:
        writer.writerow({k: row.get(k, "") for k in fieldnames})

    return buffer.getvalue()


def _build_fallback_report(state: dict) -> dict:
    final_trades = state.get("final_trades", [])
    hitl_queue = state.get("hitl_queue", [])
    corrections = state.get("corrections", [])
    validation_results = state.get("validation_results", [])
    risk_results = state.get("risk_results", [])
    compliance_results = state.get("compliance_results", [])

    passed = len([
        t for t in final_trades
        if isinstance(t, dict) and str(t.get("final_status", "")).upper() == "PASS"
    ])
    auto_fixed = len([
        t for t in final_trades
        if isinstance(t, dict) and str(t.get("auto_fix_status", "")).upper() == "APPLIED"
    ])
    hitl = len(hitl_queue)

    return {
        "summary": "Fallback report generated",
        "statistics": {
            "total": len(final_trades),
            "passed": passed,
            "auto_fixed": auto_fixed,
            "hitl": hitl,
        },
        "key_issues": ["LLM parsing failed or returned incomplete JSON"],
        "recommendations": [
            "Check LLM formatting",
            "Prefer deterministic report generation from pipeline outputs",
        ],
        "validation_results": validation_results,
        "risk_results": risk_results,
        "compliance_results": compliance_results,
        "corrections": corrections,
        "hitl_queue": hitl_queue,
        "report_records": [],
        "csv_rows": [],
    }


def _normalize_report_json(report_json: dict, fallback_report: dict) -> dict:
    if not isinstance(report_json, dict):
        return fallback_report

    report_json.setdefault("summary", "")
    report_json.setdefault("statistics", {})
    report_json.setdefault("key_issues", [])
    report_json.setdefault("recommendations", [])
    report_json.setdefault("report_records", [])
    report_json.setdefault("csv_rows", [])
    report_json.setdefault("corrections", [])

    for key in ["report_records", "csv_rows", "key_issues", "recommendations", "corrections"]:
        if not isinstance(report_json.get(key), list):
            report_json[key] = []

    if not isinstance(report_json.get("statistics"), dict):
        report_json["statistics"] = {}

    return report_json


def report_generator_agent(state: dict) -> dict:
    settings = get_settings()
    os.makedirs(settings.reports_dir, exist_ok=True)

    run_id = state["run_id"]
    db = SessionLocal()

    fallback_report = _build_fallback_report(state)

    prompt = f"""
Return ONLY JSON.

You are generating a MiFID II reporting summary for a completed pipeline run.

Do not recreate trade tables.
Do not return large arrays.
Focus only on:
- summary
- statistics
- key_issues
- recommendations
- corrections

Final Trades:
{json.dumps(state.get("final_trades", []), ensure_ascii=False, indent=2)}

Corrections:
{json.dumps(state.get("corrections", []), ensure_ascii=False, indent=2)}

HITL Queue:
{json.dumps(state.get("hitl_queue", []), ensure_ascii=False, indent=2)}

Validation:
{json.dumps(state.get("validation_results", []), ensure_ascii=False, indent=2)}

Risk:
{json.dumps(state.get("risk_results", []), ensure_ascii=False, indent=2)}

Compliance:
{json.dumps(state.get("compliance_results", []), ensure_ascii=False, indent=2)}

Return JSON:
{{
  "summary": "",
  "statistics": {{
    "total": 0,
    "passed": 0,
    "auto_fixed": 0,
    "hitl": 0
  }},
  "key_issues": [],
  "recommendations": [],
  "corrections": []
}}
""".strip()

    try:
        report_json, raw = call_llm_json(prompt, fallback_report, retries=2)
        print("\n🧠 REPORT LLM OUTPUT:\n", raw, "\n")

        if not isinstance(report_json, dict):
            report_json = fallback_report

        report_json = _normalize_report_json(report_json, fallback_report)

        if not report_json.get("corrections"):
            report_json["corrections"] = state.get("corrections", [])

        csv_rows = _derive_csv_rows(state, report_json)
        csv_text = _build_csv_text(csv_rows)

        if not report_json.get("csv_rows"):
            report_json["csv_rows"] = csv_rows

        report_path = os.path.join(settings.reports_dir, f"{run_id}_final_report.json")
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report_json, f, indent=2, ensure_ascii=False)

        csv_path = ""
        if csv_text:
            csv_path = os.path.join(settings.reports_dir, f"{run_id}_llm_report.csv")
            with open(csv_path, "w", encoding="utf-8", newline="") as f:
                f.write(csv_text)

        exception_report_path = os.path.join(settings.reports_dir, f"{run_id}_exceptions.json")
        with open(exception_report_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "run_id": run_id,
                    "hitl_queue": state.get("hitl_queue", []),
                    "validation_results": state.get("validation_results", []),
                    "risk_results": state.get("risk_results", []),
                    "compliance_results": state.get("compliance_results", []),
                    "corrections": state.get("corrections", []),
                    "modified_trades": state.get("modified_trades", []),
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

        final_trades = state.get("final_trades", [])
        stats = report_json.get("statistics", {})
        if not stats or stats.get("total", 0) == 0:
            stats = {
                "total": len(final_trades),
                "passed": len([
                    t for t in final_trades
                    if isinstance(t, dict) and str(t.get("final_status", "")).upper() == "PASS"
                ]),
                "auto_fixed": len([
                    t for t in final_trades
                    if isinstance(t, dict) and str(t.get("auto_fix_status", "")).upper() == "APPLIED"
                ]),
                "hitl": len(state.get("hitl_queue", [])),
            }

        stats.update({
            "run_id": run_id,
            "generated_at": datetime.datetime.utcnow().isoformat(),
        })

        db.add(AuditLog(
            run_id=run_id,
            trade_id="ALL",
            agent="ReportGeneratorAgent",
            action="LLM_REPORT_GENERATED",
            detail=json.dumps(report_json, ensure_ascii=False),
        ))

        db.add(RunMetadata(
            run_id=run_id,
            total_trades=stats.get("total", 0),
            exceptions_count=len(state.get("hitl_queue", [])),
            auto_corrected=len(state.get("corrections", [])),
            hitl_count=len(state.get("hitl_queue", [])),
            status="done",
        ))

        db.commit()

        return {
            "report_json": report_json,
            "report_path": report_path,
            "csv_path": csv_path,
            "exception_report_path": exception_report_path,
            "mifid_report_csv": csv_text,
            "stats": stats,
            "agent_log": ["ReportGeneratorAgent (LLM-driven) completed"],
            "status": "done",
        }

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()