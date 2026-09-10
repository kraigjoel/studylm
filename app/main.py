import streamlit as st

from app.rag.retriever import retrieve
from app.llm.chat import ask_llm

st.title("StudyLM")

question = st.text_input("Ask your notes anything")

if question:

    retrieved = retrieve(question)

    answer = ask_llm(question, retrieved)

    st.write(answer)

    st.subheader("Sources")

    for meta in retrieved["metadatas"][0]:
        st.write(meta["source"])