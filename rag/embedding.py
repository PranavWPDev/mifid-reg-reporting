from vertexai.language_models import TextEmbeddingModel

# Vertex AI embedding model (enterprise standard)
model = TextEmbeddingModel.from_pretrained("text-embedding-004")


def get_embedding(text: str):
    """Return embedding vector"""
    return model.get_embeddings([text])[0].values