# StudyLM RAG Debugging Process

## Overview

This document records the debugging process used to verify the StudyLM
document-question-answering pipeline.

The original issue was that the AI appeared unable to answer questions
from uploaded documents. Each stage of the Retrieval-Augmented
Generation (RAG) pipeline was tested independently.

## RAG Pipeline

``` text
PDF documents
    ↓
Document loading
    ↓
Text extraction
    ↓
Text chunking
    ↓
Embedding generation
    ↓
ChromaDB indexing
    ↓
User question
    ↓
Query embedding
    ↓
Relevant chunk retrieval
    ↓
Context passed to Ollama
    ↓
LLM-generated answer
```

## 1. PDF Loading and Text Extraction

The loader test successfully found and extracted text from:

``` text
Lab 1B - Solution.pdf
```

The output contained meaningful content, including the course title,
workshop information, Week 2 material, R programming questions, and code
examples.

### Result

``` text
PDF loading: PASS
Text extraction: PASS
```

## 2. Text Chunking

The chunking test produced:

``` text
Documents loaded: 1
Chunks created: 10
```

The chunks contained meaningful sections of the source PDF. Examples
included:

-   The invoice question
-   R code for calculating total price
-   The `is_prime` question
-   The implementation of the `is_prime` function

The initial test assumed chunks were LangChain `Document` objects and
attempted to access `chunk.page_content`. This caused an
`AttributeError`.

Inspection showed that the project returns dictionaries in this
structure:

``` python
{
    "text": "...",
    "source": "Lab 1B - Solution.pdf"
}
```

The test was corrected to inspect the dictionary directly.

### Result

``` text
Document loading: PASS
Chunking: PASS
Chunk content quality: PASS
```

## 3. Embedding Generation

The embedding model is defined in `app/rag/retriever.py`:

``` python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
```

The first test attempted to import `embedding_model`, but the actual
variable was named `model`. The test was corrected to import:

``` python
from app.rag.retriever import model
```

The model successfully encoded document text into numerical vectors. The
`all-MiniLM-L6-v2` model produces 384-dimensional embeddings.

### Result

``` text
Embedding generation: PASS
```

## 4. ChromaDB Indexing

The indexing test loaded the documents, split them into chunks, called
`index_chunks(chunks)`, and inspected the ChromaDB collection.

The output was:

``` text
Chunks to index: 10
Documents in ChromaDB: 10
```

The stored documents contained the original extracted text.

### Result

``` text
ChromaDB indexing: PASS
Stored document count: PASS
Stored document content: PASS
```

## 5. Semantic Retrieval

The retrieval test used several questions.

### Query

``` text
What is the R function used to check whether a number is prime?
```

The retrieved results included:

``` text
Write a function in R named is_prime that checks whether a given number is a prime number or not.
```

The results also included the actual implementation:

``` r
is_prime <- function(n) {
  if (n <= 1) {
    return(FALSE)
  }

  for (i in 2:sqrt(n)) {
    if (n %% i == 0) {
      return(FALSE)
    }
  }

  return(TRUE)
}
```

### Query

``` text
How do you calculate total price including tax in R?
```

The retrieved results included:

``` r
total_price <- itemprice + (itemprice * tax / 100)
```

### Query

``` text
What is covered in Week 2?
```

The retrieved results included relevant Week 2 content, including R
basic operations, prime-number checking, and number guessing exercises.

### Result

``` text
Semantic retrieval: PASS
Relevant chunks returned: PASS
```

## 6. LLM Context Pipeline

The LLM code constructs context from the retrieved ChromaDB documents:

``` python
context = "\n\n".join(retrieved["documents"][0])
```

It then inserts that context into the prompt before calling Ollama:

``` python
return llm.invoke(prompt)
```

The Streamlit application performs:

``` python
retrieved = retrieve(question)
answer = ask_llm(question, retrieved)
```

This confirmed that retrieved context was being passed to the LLM.

## 7. Final End-to-End Test

The application was tested with:

``` text
What is the R function used to check whether a number is prime?
```

The model returned:

``` text
The R function used to check whether a number is prime is `is_prime(n)`.
```

### Final Result

``` text
PDF loading              PASS
Text extraction           PASS
Text chunking             PASS
Embedding generation      PASS
ChromaDB indexing         PASS
Semantic retrieval        PASS
Context construction      PASS
LLM invocation            PASS
Final answer generation   PASS
```

## Key Findings

The issue was not caused by:

-   PDF extraction
-   Text chunking
-   Embedding generation
-   ChromaDB indexing
-   Semantic retrieval
-   Basic LLM prompt wiring

The likely issue was related to the document indexing lifecycle.
Documents were not necessarily being ingested and indexed automatically
before questions were asked.

After manually indexing the documents, the application answered
questions correctly.

## Current Architecture Status

The backend works when documents have already been indexed.

The next major improvement is automatic ingestion for new documents:

``` text
Upload PDF
    ↓
Extract text
    ↓
Split into chunks
    ↓
Generate embeddings
    ↓
Index new chunks in ChromaDB
    ↓
Allow user questions
```

The application should also avoid re-indexing the same documents every
time Streamlit reruns.

## Future Improvements

### Automatic ingestion

New PDFs should be indexed automatically after upload.

### Duplicate prevention

The current indexing code uses:

``` python
ids=[str(i)]
```

This can cause duplicate-ID errors when the same chunks are indexed
repeatedly.

A more robust approach would generate stable IDs based on the document
name, page, chunk index, or a content hash.

### Persistent paths

The current ChromaDB path is:

``` python
client = chromadb.PersistentClient("data/vectorstore")
```

This is a relative path. It should eventually be based on the project
root to prevent different databases from being created depending on the
launch directory.

### Debugging visibility

The application should log or display:

-   Number of documents loaded
-   Number of chunks created
-   Number of chunks indexed
-   Number of documents stored in ChromaDB
-   Number of chunks retrieved
-   Retrieved source filenames
-   Context length passed to the LLM

## Conclusion

The debugging process confirmed that StudyLM's core RAG functionality is
operational. The system can load PDF text, split it into chunks,
generate embeddings, store them in ChromaDB, retrieve relevant content,
and pass that content to Ollama to generate an answer.

The next major development task is improving the ingestion lifecycle so
uploaded documents are automatically indexed and available to the
assistant without manually running indexing scripts.
