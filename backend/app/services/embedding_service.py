"""Vector embedding service using sentence-transformers (all-MiniLM-L6-v2)."""
from typing import List, Optional

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384


class EmbeddingService:
    """In-memory singleton vector embedding service using sentence-transformers."""

    _instance = None
    _model = None

    def __new__(cls) -> "EmbeddingService":
        if cls._instance is None:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
        return cls._instance

    @property
    def model(self):
        """Lazy-load the SentenceTransformer model singleton."""
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            try:
                self._model = SentenceTransformer(MODEL_NAME, local_files_only=True)
            except Exception:
                self._model = SentenceTransformer(MODEL_NAME)
        return self._model

    def embed_text(self, text: str) -> List[float]:
        """Embed a single text string into a normalized 384-dimensional vector."""
        if not text or not text.strip():
            return [0.0] * EMBEDDING_DIM
        embedding = self.model.encode(text.strip(), normalize_embeddings=True)
        return embedding.tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple text chunks in batch returning normalized vectors."""
        if not texts:
            return []
        cleaned = [t.strip() if t and t.strip() else "" for t in texts]
        embeddings = self.model.encode(cleaned, normalize_embeddings=True)
        return [e.tolist() for e in embeddings]


# Singleton instance
embedding_service = EmbeddingService()


def embed_text(text: str) -> List[float]:
    """Expose embed_text function returning a normalized 384-dimensional vector."""
    return embedding_service.embed_text(text)
