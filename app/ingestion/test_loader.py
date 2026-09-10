import sys
from pathlib import Path

# Allow this file to be run directly from VS Code or the command line.
if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.ingestion.loader import load_documents


def main():
    # PyMuPDF can extract Unicode characters not supported by the Windows
    # console's legacy CP1252 encoding.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    docs = load_documents()
    if not docs:
        raise RuntimeError("No PDF documents were found in data/documents.")

    print(docs[0]["source"])
    print(docs[0]["text"][:500])


if __name__ == "__main__":
    main()
