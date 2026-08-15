from app.ingestion.loader import load_documents

docs = load_documents()

print(docs[0]["source"])
print(docs[0]["text"][:500])