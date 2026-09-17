from __future__ import annotations

import json
import re
from pathlib import Path

import fitz
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

from darukaa_assignment.config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    MODEL_NAME,
    VECTOR_COLLECTION_NAME,
    VECTOR_DB_PATH,
)
from darukaa_assignment.knowledge.sources import SOURCE_CATALOG

DATA_DIR = Path(__file__).resolve().parents[3] / "data" / "knowledge_base"


def ensure_knowledge_base_dirs() -> None:
    (DATA_DIR / "pdfs").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "json").mkdir(parents=True, exist_ok=True)


def save_source_manifest() -> None:
    ensure_knowledge_base_dirs()
    manifest_path = DATA_DIR / "json" / "source_manifest.json"
    payload = [
        {
            "title": source.title,
            "source_org": source.source_org,
            "url": source.url,
            "year": source.year,
            "domain": source.domain,
            "doc_type": source.doc_type,
        }
        for source in SOURCE_CATALOG
    ]
    manifest_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def read_metadata_manifest() -> list[dict[str, str]]:
    manifest_path = DATA_DIR / "json" / "source_manifest.json"
    if manifest_path.exists():
        return json.loads(manifest_path.read_text(encoding="utf-8"))

    metadata_files = sorted((DATA_DIR / "json").glob("*.json"))
    records: list[dict[str, str]] = []
    for file_path in metadata_files:
        if file_path.name == "source_manifest.json":
            continue
        records.append(json.loads(file_path.read_text(encoding="utf-8")))
    return records


def extract_pdf_text(pdf_path: str | Path) -> str:
    pdf_file = Path(pdf_path)
    document = fitz.open(str(pdf_file))
    parts: list[str] = []
    for page in document:
        text = page.get_text()
        if text:
            parts.append(text)
    document.close()
    return "\n".join(parts)


def extract_html_text(html_path: str | Path) -> str:
    raw_html = Path(html_path).read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(raw_html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator="\n", strip=True)
    return re.sub(r"\n{3,}", "\n\n", text)


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_text(text)


def build_chunks_from_metadata(metadata: dict[str, str], source_root: Path | None = None) -> list[dict[str, str]]:
    source_root = source_root or DATA_DIR
    local_file = source_root / "pdfs" / metadata.get("local_file_name", "")
    if not local_file.exists():
        return []

    if metadata.get("doc_type", "").lower() in {"pdf"}:
        text = extract_pdf_text(local_file)
    else:
        text = extract_html_text(local_file)

    chunks = chunk_text(text)
    records: list[dict[str, str]] = []
    for index, chunk in enumerate(chunks):
        records.append(
            {
                "title": metadata.get("title", "unknown"),
                "source_org": metadata.get("source_org", "unknown"),
                "url": metadata.get("url", ""),
                "year": metadata.get("year", ""),
                "domain": metadata.get("domain", "general"),
                "doc_type": metadata.get("doc_type", "unknown"),
                "chunk_index": str(index),
                "text": chunk,
            }
        )
    return records


def embed_chunks(chunks: list[str]) -> list[list[float]]:
    model = SentenceTransformer(MODEL_NAME)
    return model.encode(chunks).tolist()


def insert_chunks_into_vector_db(chunks: list[dict[str, str]]) -> list[dict[str, str]]:
    import chromadb

    if not chunks:
        return []

    documents = [chunk["text"] for chunk in chunks]
    metadatas = [
        {
            "title": chunk["title"],
            "source_org": chunk["source_org"],
            "url": chunk["url"],
            "year": chunk["year"],
            "domain": chunk["domain"],
            "doc_type": chunk["doc_type"],
            "chunk_index": chunk["chunk_index"],
        }
        for chunk in chunks
    ]
    ids = [f"{chunk['title']}-{chunk['chunk_index']}" for chunk in chunks]

    client = chromadb.PersistentClient(path=str(Path(VECTOR_DB_PATH)))
    collection = client.get_or_create_collection(name=VECTOR_COLLECTION_NAME)
    collection.upsert(documents=documents, metadatas=metadatas, ids=ids)
    return chunks


def ingest_all_documents() -> list[dict[str, str]]:
    metadata_list = read_metadata_manifest()
    all_chunks: list[dict[str, str]] = []
    for metadata in metadata_list:
        source_chunks = build_chunks_from_metadata(metadata)
        if source_chunks:
            all_chunks.extend(source_chunks)
    insert_chunks_into_vector_db(all_chunks)
    return all_chunks
