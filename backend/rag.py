from typing import List, Dict

from backend.embeddings import EmbeddingModel
from backend.endee_sdk_client import EndeeVectorStore


INDEX_NAME = "documents"
TOP_K = 3


class RAGRetriever:
    def __init__(self):
        self.embedder = EmbeddingModel()
        self.store = EndeeVectorStore()
        self.index = self.store.get_index(INDEX_NAME)

    def retrieve(self, question: str) -> List[Dict]:
        # Step 1: Embed the question
        query_vector = self.embedder.embed_text(question)

        # Step 2: Semantic search in Endee
        results = self.index.query(
            vector=query_vector,
            top_k=TOP_K,
            include_vectors=False
        )

        # Step 3: Format results
        retrieved_chunks = []
        for item in results:
            retrieved_chunks.append({
                "id": item["id"],
                "score": item.get("similarity"),
                "text": item.get("meta", {}).get("text"),
                "source": item.get("meta", {}).get("source")
            })

        return retrieved_chunks
