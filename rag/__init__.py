from rag.vector_store import initialize_vector_store


def init_rag():
    initialize_vector_store()
    print("✅ RAG initialized (Enterprise Mode)")