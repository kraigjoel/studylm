from app.ingestion.loader import load_documents, split_documents
from app.rag.retriever import model

documents = load_documents()
chunks = split_documents(documents)

print(f"Chunks available: {len(chunks)}")

# Test embedding one chunk
text = chunks[0]["text"]
embedding = model.encode(text)

print(f"Embedding type: {type(embedding)}")
print(f"Embedding dimensions: {len(embedding)}")
print(f"First 10 values: {embedding[:10]}")