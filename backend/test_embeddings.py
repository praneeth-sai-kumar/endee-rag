from backend.embeddings import EmbeddingModel

model = EmbeddingModel()

text = "Endee is a high-performance vector database for AI applications."
vec = model.embed_text(text)

print("Embedding length:", len(vec))
print("First 5 values:", vec[:5])
