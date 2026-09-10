from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3.1:8b")

def ask_llm(question, retrieved):

    context = "\n\n".join(retrieved["documents"][0])

    prompt = f"""
Answer ONLY using the provided study material.

Study Material:

{context}

Question:
{question}

If the answer is not contained in the notes, say so.
"""

    return llm.invoke(prompt)