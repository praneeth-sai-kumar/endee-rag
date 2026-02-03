from backend.endee_sdk_client import EndeeVectorStore

INDEX_NAME = "documents"
DIMENSION = 384  # for sentence-transformers

store = EndeeVectorStore()

# Create index if it doesn't exist
indexes = store.list_indexes()
print("Existing indexes:", indexes)

if INDEX_NAME not in indexes:
    print(f"Creating index: {INDEX_NAME}")
    store.create_index(
        name=INDEX_NAME,
        dim=DIMENSION
    )

print("Final indexes:", store.list_indexes())
