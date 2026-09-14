from app.ingestion.loader import load_documents, split_documents
from app.rag.retriever import index_chunks, collection

documents = load_documents()
chunks = split_documents(documents)

print(f"Chunks to index: {len(chunks)}")

# Index the chunks
index_chunks(chunks)

# Check how many documents are in ChromaDB
count = collection.count()

print(f"Documents in ChromaDB: {count}")

# Inspect stored documents
results = collection.get()

print("\nStored documents:")
for i, doc in enumerate(results["documents"][:5]):
    print(f"\n--- Stored document {i + 1} ---")
    print(doc[:500])