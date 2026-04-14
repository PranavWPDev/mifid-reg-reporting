# import datetime
# import os
# import re
# from typing import Any, Dict, List

# import chromadb
# import pandas as pd
# from chromadb.utils import embedding_functions


# os.environ["ANONYMIZED_TELEMETRY"] = "FALSE"
# os.environ["CHROMA_TELEMETRY"] = "FALSE"

# def _get_settings():
#     from config import get_settings
#     return get_settings()

# def get_chroma_client():
#     settings = _get_settings()
#     return chromadb.PersistentClient(path=str(settings.chroma_path))


# def get_embedding_function():
#     return embedding_functions.DefaultEmbeddingFunction()


# def _chunk_text(text: str, max_chars: int = 800, overlap: int = 120) -> List[str]:
#     """
#     Splits long text into overlapping chunks.
#     Keeps rules readable and prevents a single huge or single tiny chunk.
#     """
#     if not text:
#         return []

#     paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
#     chunks: List[str] = []
#     current = ""

#     for para in paragraphs:
#         if not current:
#             current = para
#             continue

#         if len(current) + len(para) + 2 <= max_chars:
#             current = current + "\n\n" + para
#         else:
#             chunks.append(current)

#             if len(para) <= max_chars:
#                 current = para
#             else:
#                 step = max(1, max_chars - overlap)
#                 for i in range(0, len(para), step):
#                     part = para[i : i + max_chars].strip()
#                     if part:
#                         chunks.append(part)
#                 current = ""

#     if current:
#         chunks.append(current)

#     return chunks or [text[:max_chars]]


# def _safe_read_text(path: str) -> str:
#     with open(path, "r", encoding="utf-8") as f:
#         return f.read()


# def initialize_vector_store():
#     client = get_chroma_client()
#     ef = get_embedding_function()

#     # Rules collection
#     rules_col = client.get_or_create_collection(
#         "mifid_rules",
#         embedding_function=ef
#     )

#     if rules_col.count() == 0:
#         text = _safe_read_text("data/mifid_rules.txt")
#         chunks = _chunk_text(text, max_chars=900, overlap=150)

#         rules_col.add(
#             documents=chunks,
#             ids=[f"rule_{i}" for i in range(len(chunks))],
#             metadatas=[
#                 {
#                     "source": "mifid_rules.txt",
#                     "chunk_index": i,
#                     "created_at": datetime.datetime.utcnow().isoformat(),
#                 }
#                 for i in range(len(chunks))
#             ],
#         )
#         print(f"✅ Loaded {len(chunks)} MiFID rule chunks")
#     else:
#         print(f"✅ MiFID rules already indexed: {rules_col.count()} chunks")

#     # ISIN collection
#     isin_col = client.get_or_create_collection(
#         "isin_reference",
#         embedding_function=ef
#     )

#     if isin_col.count() == 0:
#         df = pd.read_csv("data/isin_reference.csv").fillna("")
#         docs = [
#             f"ISIN {row['isin']} belongs to {row['name']}, currency {row['currency']}, exchange {row['exchange']}, country {row['country']}"
#             for _, row in df.iterrows()
#         ]
#         isin_col.add(
#             documents=docs,
#             ids=[f"isin_{i}" for i in range(len(docs))],
#             metadatas=[
#                 {
#                     "isin": row["isin"],
#                     "name": row["name"],
#                     "currency": row["currency"],
#                     "exchange": row["exchange"],
#                     "country": row["country"],
#                 }
#                 for _, row in df.iterrows()
#             ],
#         )
#         print(f"✅ Loaded {len(docs)} ISIN records")
#     else:
#         print(f"✅ ISIN reference already indexed: {isin_col.count()} records")

#     # LEI collection
#     lei_col = client.get_or_create_collection(
#         "lei_reference",
#         embedding_function=ef
#     )

#     if lei_col.count() == 0:
#         df = pd.read_csv("data/lei_reference.csv").fillna("")
#         docs = [
#             f"LEI {row['lei']} belongs to {row['entity_name']}, country {row['country']}, status {row['status']}"
#             for _, row in df.iterrows()
#         ]
#         lei_col.add(
#             documents=docs,
#             ids=[f"lei_{i}" for i in range(len(docs))],
#             metadatas=[
#                 {
#                     "lei": row["lei"],
#                     "entity_name": row["entity_name"],
#                     "country": row["country"],
#                     "status": row["status"],
#                 }
#                 for _, row in df.iterrows()
#             ],
#         )
#         print(f"✅ Loaded {len(docs)} LEI records")
#     else:
#         print(f"✅ LEI reference already indexed: {lei_col.count()} records")

#     # Memory collection
#     client.get_or_create_collection("agent_memory", embedding_function=ef)

#     return client


# def _query_collection(collection_name: str, query: str, n_results: int = 3, k: int = None):
#     client = get_chroma_client()
#     ef = get_embedding_function()
#     col = client.get_collection(collection_name, embedding_function=ef)

#     total = col.count() or 0
#     requested = k if k is not None else n_results
#     safe_n = max(1, min(int(requested), total)) if total > 0 else 1

#     results = col.query(
#         query_texts=[query],
#         n_results=safe_n,
#         include=["documents", "metadatas", "distances", "ids"],
#     )

#     docs = results.get("documents", [[]])[0] or []
#     metas = results.get("metadatas", [[]])[0] or []
#     dists = results.get("distances", [[]])[0] or []
#     ids = results.get("ids", [[]])[0] or []

#     payload = []
#     for i, doc in enumerate(docs):
#         dist = dists[i] if i < len(dists) else None
#         score = round(1.0 / (1.0 + float(dist)), 4) if dist is not None else 0.0
#         payload.append(
#             {
#                 "id": ids[i] if i < len(ids) else "",
#                 "text": doc,
#                 "metadata": metas[i] if i < len(metas) else {},
#                 "score": score,
#             }
#         )

#     return payload


# def search_rules(query: str, n_results: int = 3, k: int = None, **kwargs):
#     try:
#         return _query_collection("mifid_rules", query, n_results=n_results, k=k)
#     except Exception as e:
#         print(f"⚠️ search_rules failed: {e}")
#         return []


# def search_isin(query: str, n_results: int = 3, k: int = None, **kwargs):
#     try:
#         return _query_collection("isin_reference", query, n_results=n_results, k=k)
#     except Exception as e:
#         print(f"⚠️ search_isin failed: {e}")
#         return []


# def search_lei(query: str, n_results: int = 3, k: int = None, **kwargs):
#     try:
#         return _query_collection("lei_reference", query, n_results=n_results, k=k)
#     except Exception as e:
#         print(f"⚠️ search_lei failed: {e}")
#         return []


# def search_correction_memory(query: str, n_results: int = 3, k: int = None, **kwargs):
#     try:
#         return _query_collection("agent_memory", query, n_results=n_results, k=k)
#     except Exception as e:
#         print(f"⚠️ search_correction_memory failed: {e}")
#         return []


# def store_correction_memory(
#     trade_id: str,
#     field: str,
#     original_value: str,
#     corrected_value: str,
#     reasoning: str,
#     confidence: float,
# ):
#     try:
#         client = get_chroma_client()
#         ef = get_embedding_function()
#         col = client.get_collection("agent_memory", embedding_function=ef)

#         doc = (
#             f"Trade {trade_id} | Field {field} | "
#             f"Original {original_value} | Corrected {corrected_value} | "
#             f"Reasoning {reasoning} | Confidence {confidence}"
#         )

#         col.add(
#             documents=[doc],
#             ids=[f"mem_{trade_id}_{field}_{datetime.datetime.utcnow().timestamp()}"],
#             metadatas=[
#                 {
#                     "trade_id": trade_id,
#                     "field": field,
#                     "confidence": confidence,
#                 }
#             ],
#         )
#     except Exception as e:
#         print(f"⚠️ store_correction_memory failed: {e}")

import datetime
import os
import re
from typing import Any, Dict, List

import chromadb
import pandas as pd
from chromadb.utils import embedding_functions

from config import get_settings

os.environ["ANONYMIZED_TELEMETRY"] = "FALSE"
os.environ["CHROMA_TELEMETRY"] = "FALSE"

settings = get_settings()


def get_chroma_client():
    return chromadb.PersistentClient(path=str(settings.chroma_path))


def get_embedding_function():
    return embedding_functions.DefaultEmbeddingFunction()


def _chunk_text(text: str, max_chars: int = 800, overlap: int = 120) -> List[str]:
    if not text:
        return []

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks: List[str] = []
    current = ""

    for para in paragraphs:
        if not current:
            current = para
            continue

        if len(current) + len(para) + 2 <= max_chars:
            current = current + "\n\n" + para
        else:
            chunks.append(current)

            if len(para) <= max_chars:
                current = para
            else:
                step = max(1, max_chars - overlap)
                for i in range(0, len(para), step):
                    part = para[i : i + max_chars].strip()
                    if part:
                        chunks.append(part)
                current = ""

    if current:
        chunks.append(current)

    return chunks or [text[:max_chars]]


def _safe_read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def initialize_vector_store():
    client = get_chroma_client()
    ef = get_embedding_function()

    rules_col = client.get_or_create_collection(
        name="mifid_rules",
        embedding_function=ef,
    )

    if rules_col.count() == 0:
        text = _safe_read_text(str(settings.backend_root / "data" / "mifid_rules.txt"))
        chunks = _chunk_text(text, max_chars=900, overlap=150)

        rules_col.add(
            documents=chunks,
            ids=[f"rule_{i}" for i in range(len(chunks))],
            metadatas=[
                {
                    "source": "mifid_rules.txt",
                    "chunk_index": i,
                    "created_at": datetime.datetime.utcnow().isoformat(),
                }
                for i in range(len(chunks))
            ],
        )
        print(f"✅ Loaded {len(chunks)} MiFID rule chunks")
    else:
        print(f"✅ MiFID rules already indexed: {rules_col.count()} chunks")

    isin_col = client.get_or_create_collection(
        name="isin_reference",
        embedding_function=ef,
    )

    if isin_col.count() == 0:
        df = pd.read_csv(settings.backend_root / "data" / "isin_reference.csv").fillna("")
        docs = [
            f"ISIN {row['isin']} belongs to {row['name']}, currency {row['currency']}, exchange {row['exchange']}, country {row['country']}"
            for _, row in df.iterrows()
        ]
        isin_col.add(
            documents=docs,
            ids=[f"isin_{i}" for i in range(len(docs))],
            metadatas=[
                {
                    "isin": row["isin"],
                    "name": row["name"],
                    "currency": row["currency"],
                    "exchange": row["exchange"],
                    "country": row["country"],
                }
                for _, row in df.iterrows()
            ],
        )
        print(f"✅ Loaded {len(docs)} ISIN records")
    else:
        print(f"✅ ISIN reference already indexed: {isin_col.count()} records")

    lei_col = client.get_or_create_collection(
        name="lei_reference",
        embedding_function=ef,
    )

    if lei_col.count() == 0:
        df = pd.read_csv(settings.backend_root / "data" / "lei_reference.csv").fillna("")
        docs = [
            f"LEI {row['lei']} belongs to {row['entity_name']}, country {row['country']}, status {row['status']}"
            for _, row in df.iterrows()
        ]
        lei_col.add(
            documents=docs,
            ids=[f"lei_{i}" for i in range(len(docs))],
            metadatas=[
                {
                    "lei": row["lei"],
                    "entity_name": row["entity_name"],
                    "country": row["country"],
                    "status": row["status"],
                }
                for _, row in df.iterrows()
            ],
        )
        print(f"✅ Loaded {len(docs)} LEI records")
    else:
        print(f"✅ LEI reference already indexed: {lei_col.count()} records")

    client.get_or_create_collection("agent_memory", embedding_function=ef)

    return client


def _safe_n_results(col, requested: int) -> int:
    try:
        total = col.count() or 0
        return max(1, min(int(requested), total)) if total > 0 else 1
    except Exception:
        return 1


def _query_collection(collection_name: str, query: str, n_results: int = 3):
    try:
        client = get_chroma_client()
        ef = get_embedding_function()
        col = client.get_collection(name=collection_name, embedding_function=ef)

        safe_n = _safe_n_results(col, n_results)

        results = col.query(
            query_texts=[query],
            n_results=safe_n,
            include=["documents", "metadatas", "distances"],
        )

        docs = (results.get("documents") or [[]])[0] or []
        metas = (results.get("metadatas") or [[]])[0] or []
        dists = (results.get("distances") or [[]])[0] or []
        ids = (results.get("ids") or [[]])[0] or []

        payload = []
        for i, doc in enumerate(docs):
            dist = dists[i] if i < len(dists) else None
            score = round(1.0 / (1.0 + float(dist)), 4) if dist is not None else 0.0
            payload.append(
                {
                    "id": ids[i] if i < len(ids) else "",
                    "text": doc,
                    "metadata": metas[i] if i < len(metas) else {},
                    "score": score,
                }
            )

        return payload

    except Exception as e:
        print(f"⚠️ _query_collection failed for {collection_name}: {e}")
        return []


def search_rules(query: str, n_results: int = 3, **kwargs):
    try:
        return _query_collection("mifid_rules", query, n_results=n_results)
    except Exception as e:
        print(f"⚠️ search_rules failed: {e}")
        return []


def search_isin(query: str, n_results: int = 3, **kwargs):
    try:
        return _query_collection("isin_reference", query, n_results=n_results)
    except Exception as e:
        print(f"⚠️ search_isin failed: {e}")
        return []


def search_lei(query: str, n_results: int = 3, **kwargs):
    try:
        return _query_collection("lei_reference", query, n_results=n_results)
    except Exception as e:
        print(f"⚠️ search_lei failed: {e}")
        return []


def search_correction_memory(query: str, n_results: int = 3, **kwargs):
    try:
        return _query_collection("agent_memory", query, n_results=n_results)
    except Exception as e:
        print(f"⚠️ search_correction_memory failed: {e}")
        return []


def store_correction_memory(
    trade_id: str,
    field: str,
    original_value: str,
    corrected_value: str,
    reasoning: str,
    confidence: float,
):
    try:
        client = get_chroma_client()
        ef = get_embedding_function()
        col = client.get_collection("agent_memory", embedding_function=ef)

        doc = (
            f"Trade {trade_id} | Field {field} | "
            f"Original {original_value} | Corrected {corrected_value} | "
            f"Reasoning {reasoning} | Confidence {confidence}"
        )

        col.add(
            documents=[doc],
            ids=[f"mem_{trade_id}_{field}_{datetime.datetime.utcnow().timestamp()}"],
            metadatas=[{"trade_id": trade_id, "field": field, "confidence": confidence}],
        )
    except Exception as e:
        print(f"⚠️ store_correction_memory failed: {e}")