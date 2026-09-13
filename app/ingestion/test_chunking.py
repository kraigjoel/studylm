from app.ingestion.loader import load_documents, split_documents

documents = load_documents()
chunks = split_documents(documents)

print(f"Documents loaded: {len(documents)}")
print(f"Chunks created: {len(chunks)}")

for i, chunk in enumerate(chunks[:5]):
    print(f"\n--- Chunk {i + 1} ---")
    print(f"Type: {type(chunk)}")
    print(chunk)