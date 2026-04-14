# from langgraph.graph import StateGraph, END
# from typing import TypedDict, List, Any, Annotated
# from operator import add
# import uuid

# from agents.ingestion import ingestion_agent
# from agents.enrichment import enrichment_agent
# from agents.validation import validation_agent
# from agents.risk import risk_agent
# from agents.compliance import compliance_agent
# from agents.decision import decision_agent
# from agents.report_generator import report_generator_agent


# class State(TypedDict):
#     run_id: str
#     raw_input: Any

#     raw_trades: List[dict]
#     enriched_trades: List[dict]
#     modified_trades: List[dict]

#     validation_results: Annotated[List[dict], add]
#     risk_results: Annotated[List[dict], add]
#     compliance_results: Annotated[List[dict], add]

#     final_trades: List[dict]
#     corrections: List[dict]
#     hitl_queue: List[dict]

#     mifid_report_csv: str
#     report_path: str
#     exception_report_path: str
#     csv_path: str

#     stats: dict
#     run_stats: dict

#     agent_log: Annotated[List[str], add]
#     status: str


# def route_after_decision(state: dict) -> str:
#     return "reprocess" if state.get("status") == "reprocess" else "report"


# def build_graph():
#     g = StateGraph(State)

#     # =========================
#     # NODES
#     # =========================
#     g.add_node("ingest", ingestion_agent)
#     g.add_node("enrich", enrichment_agent)
#     g.add_node("validate", validation_agent)
#     g.add_node("risk", risk_agent)
#     g.add_node("compliance", compliance_agent)
#     g.add_node("decision", decision_agent)
#     g.add_node("report", report_generator_agent)

#     # =========================
#     # FLOW
#     # =========================
#     g.set_entry_point("ingest")
#     g.add_edge("ingest", "enrich")

#     # Parallel fan-out
#     g.add_edge("enrich", "validate")
#     g.add_edge("enrich", "risk")
#     g.add_edge("enrich", "compliance")

#     # Fan-in
#     g.add_edge("validate", "decision")
#     g.add_edge("risk", "decision")
#     g.add_edge("compliance", "decision")

#     # After decision:
#     # - if HITL Modify happened, go back through enrich again
#     # - otherwise go to report
#     g.add_conditional_edges(
#         "decision",
#         route_after_decision,
#         {
#             "reprocess": "enrich",
#             "report": "report",
#         },
#     )

#     g.add_edge("report", END)

#     return g.compile()


# def run_pipeline(raw_input) -> dict:
#     graph = build_graph()
#     run_id = f"RUN-{uuid.uuid4().hex[:8].upper()}"

#     initial_state = {
#         "run_id": run_id,
#         "raw_input": raw_input,
#         "raw_trades": [],
#         "modified_trades": [],
#         "enriched_trades": [],
#         "validation_results": [],
#         "risk_results": [],
#         "compliance_results": [],
#         "final_trades": [],
#         "corrections": [],
#         "hitl_queue": [],
#         "mifid_report_csv": "",
#         "report_path": "",
#         "exception_report_path": "",
#         "csv_path": "",
#         "stats": {},
#         "run_stats": {},
#         "agent_log": [],
#         "status": "start",
#     }

#     return graph.invoke(initial_state)

from __future__ import annotations

import uuid
from operator import add
from typing import TypedDict, List, Any, Annotated, Dict, Tuple

from langgraph.graph import StateGraph, END

from agents.ingestion import ingestion_agent
from agents.enrichment import enrichment_agent
from agents.validation import validation_agent
from agents.risk import risk_agent
from agents.compliance import compliance_agent
from agents.decision import decision_agent
from agents.report_generator import report_generator_agent


class State(TypedDict):
    run_id: str
    raw_input: Any

    batch_id: str
    source_channel: str
    source_system: str
    source_ref: str
    received_at: str

    raw_trades: List[dict]
    enriched_trades: List[dict]
    modified_trades: List[dict]

    validation_results: Annotated[List[dict], add]
    risk_results: Annotated[List[dict], add]
    compliance_results: Annotated[List[dict], add]

    final_trades: List[dict]
    corrections: List[dict]
    hitl_queue: List[dict]

    mifid_report_csv: str
    report_path: str
    exception_report_path: str
    csv_path: str

    stats: dict
    run_stats: dict

    agent_log: Annotated[List[str], add]
    status: str


def _extract_trade_payload(raw_input: Any) -> Tuple[List[dict], Dict[str, Any]]:
    meta = {
        "batch_id": "",
        "source_channel": "ui",
        "source_system": "react-ui",
        "source_ref": "manual",
        "received_at": "",
    }

    if raw_input is None:
        return [], meta

    if isinstance(raw_input, dict):
        meta["batch_id"] = str(raw_input.get("batch_id") or "")
        meta["source_channel"] = str(raw_input.get("source_channel") or meta["source_channel"])
        meta["source_system"] = str(raw_input.get("source_system") or meta["source_system"])
        meta["source_ref"] = str(raw_input.get("source_ref") or meta["source_ref"])
        meta["received_at"] = str(raw_input.get("received_at") or "")

        if isinstance(raw_input.get("trade_data"), list):
            return [x for x in raw_input["trade_data"] if isinstance(x, dict)], meta

        if isinstance(raw_input.get("trades"), list):
            return [x for x in raw_input["trades"] if isinstance(x, dict)], meta

        return [raw_input], meta

    if isinstance(raw_input, list):
        return [x for x in raw_input if isinstance(x, dict)], meta

    return [], meta


def route_after_decision(state: dict) -> str:
    return "reprocess" if state.get("status") == "reprocess" else "report"


def build_graph():
    g = StateGraph(State)

    g.add_node("ingest", ingestion_agent)
    g.add_node("enrich", enrichment_agent)
    g.add_node("validate", validation_agent)
    g.add_node("risk", risk_agent)
    g.add_node("compliance", compliance_agent)
    g.add_node("decision", decision_agent)
    g.add_node("report", report_generator_agent)

    g.set_entry_point("ingest")
    g.add_edge("ingest", "enrich")

    g.add_edge("enrich", "validate")
    g.add_edge("enrich", "risk")
    g.add_edge("enrich", "compliance")

    g.add_edge("validate", "decision")
    g.add_edge("risk", "decision")
    g.add_edge("compliance", "decision")

    g.add_conditional_edges(
        "decision",
        route_after_decision,
        {
            "reprocess": "enrich",
            "report": "report",
        },
    )

    g.add_edge("report", END)

    return g.compile()


def run_pipeline(
    raw_input,
    *,
    source_channel: str = "",
    source_system: str = "",
    source_ref: str = "",
) -> dict:
    graph = build_graph()
    run_id = f"RUN-{uuid.uuid4().hex[:8].upper()}"

    trades, meta = _extract_trade_payload(raw_input)

    if source_channel:
        meta["source_channel"] = source_channel
    if source_system:
        meta["source_system"] = source_system
    if source_ref:
        meta["source_ref"] = source_ref

    initial_state = {
        "run_id": run_id,
        "raw_input": trades,
        "batch_id": meta.get("batch_id", ""),
        "source_channel": meta.get("source_channel", "ui"),
        "source_system": meta.get("source_system", "react-ui"),
        "source_ref": meta.get("source_ref", "manual"),
        "received_at": meta.get("received_at", ""),

        "raw_trades": [],
        "modified_trades": [],
        "enriched_trades": [],
        "validation_results": [],
        "risk_results": [],
        "compliance_results": [],
        "final_trades": [],
        "corrections": [],
        "hitl_queue": [],
        "mifid_report_csv": "",
        "report_path": "",
        "exception_report_path": "",
        "csv_path": "",
        "stats": {},
        "run_stats": {},
        "agent_log": [],
        "status": "start",
    }

    result = graph.invoke(initial_state)

    # Propagate metadata to every final trade
    for trade in result.get("final_trades", []):
        if isinstance(trade, dict):
            trade["source_channel"] = initial_state["source_channel"]
            trade["source_system"] = initial_state["source_system"]
            trade["source_ref"] = initial_state["source_ref"]
            trade["batch_id"] = initial_state["batch_id"]
            trade["received_at"] = initial_state["received_at"]

    return result