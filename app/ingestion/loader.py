import fitz
from pathlib import Path

def load_documents(folder="data/documents"):
    docs = []

    for file in Path(folder).glob("*.pdf"):
        pdf = fitz.open(file)

        text = ""

        for page in pdf:
            text += page.get_text()

        docs.append({
            "source": file.name,
            "text": text
        })

    return docs