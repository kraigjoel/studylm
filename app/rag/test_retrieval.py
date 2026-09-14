from app.rag.retriever import retrieve

queries = [
    "What is the R function used to check whether a number is prime?",
    "How do you calculate total price including tax in R?",
    "What is covered in Week 2?"
]

for query in queries:
    print(f"\n{'=' * 60}")
    print(f"QUERY: {query}")
    print('=' * 60)

    results = retrieve(query, k=3)

    for i, doc in enumerate(results["documents"][0]):
        print(f"\n--- Result {i + 1} ---")
        print(doc[:500])