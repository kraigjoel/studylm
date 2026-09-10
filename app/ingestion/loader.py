import pymupdf
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DOCUMENTS_FOLDER = PROJECT_ROOT / "data" / "documents"


def load_documents(folder=DEFAULT_DOCUMENTS_FOLDER):
    docs = []

    for file in Path(folder).glob("*.pdf"):
        with pymupdf.open(file) as pdf:
            text = "".join(page.get_text() for page in pdf)

        docs.append({
            "source": file.name,
            "text": text
        })

    return docs


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=150,
    )

    chunks = []

    for doc in documents:
        for chunk in splitter.split_text(doc["text"]):
            chunks.append({
                "text": chunk,
                "source": doc["source"],
            })

    return chunks
