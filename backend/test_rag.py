from backend.rag import RAGRetriever

rag = RAGRetriever()

question = "What is Endee used for?"

results = rag.retrieve(question)

for r in results:
    print("----")
    print("Score:", r["score"])
    print("Source:", r["source"])
    print("Text:", r["text"])
