import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient("data/vectorstore")

collection = client.get_or_create_collection("studylm")

def index_chunks(chunks):

    for i, chunk in enumerate(chunks):

        embedding = model.encode(chunk["text"]).tolist()

        collection.add(
            ids=[str(i)],
            documents=[chunk["text"]],
            embeddings=[embedding],
            metadatas=[{"source": chunk["source"]}]
        )