# from rag.vector_store import get_chroma_client, get_embedding_function


# def _safe_n_results(col, requested: int):
#     """
#     Prevent Chroma warning:
#     requested > available documents
#     """
#     try:
#         total = col.count() or 0
#         return max(1, min(requested, total)) if total > 0 else 1
#     except:
#         return 1


# def search_rules(query: str, rule_type: str = None, n_results: int = 5):
#     try:
#         client = get_chroma_client()
#         ef = get_embedding_function()

#         col = client.get_collection(
#             name="mifid_rules",
#             embedding_function=ef
#         )

#         # ✅ FIX: dynamic n_results
#         safe_n = _safe_n_results(col, n_results)

#         where_filter = {}
#         if rule_type:
#             where_filter["type"] = rule_type.lower()

#         results = col.query(
#             query_texts=[query],
#             n_results=safe_n,
#             where=where_filter if where_filter else None
#         )

#         docs = (results.get("documents") or [[]])[0]
#         distances = (results.get("distances") or [[]])[0]

#         # fallback without filter
#         if not docs and rule_type:
#             results = col.query(
#                 query_texts=[query],
#                 n_results=safe_n
#             )
#             docs = (results.get("documents") or [[]])[0]
#             distances = (results.get("distances") or [[]])[0]

#         if not docs:
#             return []

#         output = []
#         for d, s in zip(docs, distances):
#             try:
#                 score = round(1 / (1 + float(s)), 3)  # better scoring
#             except:
#                 score = 0.0

#             output.append({
#                 "text": d,
#                 "score": score
#             })

#         return output

#     except Exception as e:
#         print(f"⚠️ search_rules error: {e}")
#         return []


# def search_isin(query: str, n_results: int = 3):
#     return _search("isin_reference", query, n_results)


# def search_lei(query: str, n_results: int = 3):
#     return _search("lei_reference", query, n_results)


# def search_correction_memory(query: str, n_results: int = 3):
#     return _search("agent_memory", query, n_results)


# def _search(collection_name: str, query: str, n_results: int):
#     try:
#         client = get_chroma_client()
#         ef = get_embedding_function()

#         col = client.get_collection(
#             name=collection_name,
#             embedding_function=ef
#         )

#         # ✅ FIX here also
#         safe_n = _safe_n_results(col, n_results)

#         results = col.query(
#             query_texts=[query],
#             n_results=safe_n
#         )

#         docs = (results.get("documents") or [[]])[0]
#         distances = (results.get("distances") or [[]])[0]

#         if not docs:
#             return []

#         output = []
#         for d, s in zip(docs, distances):
#             try:
#                 score = round(1 / (1 + float(s)), 3)
#             except:
#                 score = 0.0

#             output.append({
#                 "text": d,
#                 "score": score
#             })

#         return output

#     except Exception as e:
#         print(f"⚠️ {collection_name} search failed: {e}")
#         return []
from __future__ import annotations

from rag.vector_store import (
    search_rules,
    search_isin,
    search_lei,
    search_correction_memory,
)

# Just re-export (clean layer)
__all__ = [
    "search_rules",
    "search_isin",
    "search_lei",
    "search_correction_memory",
]