from __future__ import annotations

from typing import Any


class MultiDocumentRetriever:
    """Simple retriever contract for a multi-document evidence pipeline."""

    def __init__(self, vector_store: Any | None = None) -> None:
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        if self.vector_store is None:
            return []
        return self.vector_store.similarity_search(query, k=top_k)

    def aggregate_sources(self, retrieved_chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
        deduped: dict[str, dict[str, Any]] = {}
        for chunk in retrieved_chunks:
            metadata = chunk.get("metadata", {})
            source_key = metadata.get("source", metadata.get("title", "unknown"))
            deduped.setdefault(source_key, {"source": source_key, "matches": []})
            deduped[source_key]["matches"].append(chunk)
        return list(deduped.values())
