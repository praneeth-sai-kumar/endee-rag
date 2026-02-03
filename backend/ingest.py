import os
from typing import List

from endee.exceptions import ConflictException

from backend.embeddings import EmbeddingModel
from backend.endee_sdk_client import EndeeVectorStore


# -----------------------------
# Configuration
# -----------------------------
DATA_DIR = "data"
INDEX_NAME = "documents"
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50


# -----------------------------
# Utility Functions
# -----------------------------
def read_text_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap
        if start < 0:
            start = 0

    return chunks


# -----------------------------
# Ingestion Pipeline
# -----------------------------
def ingest_documents():
    print("Starting ingestion pipeline...")

    embedder = EmbeddingModel()
    store = EndeeVectorStore()

    # -----------------------------
    # Create index safely (IDEMPOTENT)
    # -----------------------------
    try:
        print(f"Ensuring index '{INDEX_NAME}' exists...")
        store.create_index(
            name=INDEX_NAME,
            dim=embedder.dimension
        )
        print(f"Index '{INDEX_NAME}' created.")
    except ConflictException:
        print(f"Index '{INDEX_NAME}' already exists. Continuing...")

    index = store.get_index(INDEX_NAME)

    # -----------------------------
    # Read and ingest documents
    # -----------------------------
    vectors = []
    total_chunks = 0

    if not os.path.exists(DATA_DIR):
        print(f"Data directory '{DATA_DIR}' not found.")
        return

    for filename in os.listdir(DATA_DIR):
        if not filename.lower().endswith(".txt"):
            continue

        file_path = os.path.join(DATA_DIR, filename)
        print(f"Ingesting file: {filename}")

        text = read_text_file(file_path)
        chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)

        for i, chunk in enumerate(chunks):
            embedding = embedder.embed_text(chunk)

            vectors.append({
                "id": f"{filename}_{i}",
                "vector": embedding,
                "meta": {
                    "text": chunk,
                    "source": filename
                },
                "filter": {
                    "file": filename,
                    "type": "text"
                }
            })

            total_chunks += 1

    # -----------------------------
    # Upsert into Endee
    # -----------------------------
    if vectors:
        index.upsert(vectors)
        print(f"Successfully ingested {total_chunks} chunks into Endee.")
    else:
        print("No documents found to ingest.")


# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    ingest_documents()
