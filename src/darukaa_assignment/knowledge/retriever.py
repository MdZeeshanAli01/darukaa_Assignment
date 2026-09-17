from __future__ import annotations

from typing import Any

import chromadb

from darukaa_assignment.config import VECTOR_COLLECTION_NAME, VECTOR_DB_PATH


class MultiDocumentRetriever:
    """Retrieve text chunks across all knowledge documents and group them by source."""

    def __init__(self, vector_store: Any | None = None) -> None:
        self.vector_store = vector_store

    def get_collection(self) -> Any:
        if self.vector_store is not None:
            return self.vector_store
        client = chromadb.PersistentClient(path=str(VECTOR_DB_PATH))
        return client.get_or_create_collection(name=VECTOR_COLLECTION_NAME)

    def retrieve(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        collection = self.get_collection()
        results = collection.query(query_texts=[query], n_results=top_k)
        chunk_records: list[dict[str, Any]] = []
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        for idx, document in enumerate(documents):
            metadata = metadatas[idx] if idx < len(metadatas) else {}
            chunk_records.append(
                {
                    "text": document,
                    "metadata": metadata,
                }
            )
        return chunk_records

    def aggregate_sources(self, retrieved_chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
        grouped: dict[str, dict[str, Any]] = {}
        for chunk in retrieved_chunks:
            metadata = chunk.get("metadata", {})
            source_name = metadata.get("title") or metadata.get("source_org") or "unknown-source"
            entry = grouped.setdefault(
                source_name,
                {
                    "title": source_name,
                    "source_org": metadata.get("source_org", "unknown"),
                    "url": metadata.get("url", ""),
                    "year": metadata.get("year", ""),
                    "matches": [],
                },
            )
            entry["matches"].append(chunk["text"])
        return list(grouped.values())
