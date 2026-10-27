import streamlit as st
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Day 69 RAG")
st.title("Day 69 - RAG in Docker v2")
st.success("Hi Raviteja, RAG with Embeddings (Light) - 100% Working!")

pdf = st.file_uploader("Upload PDF", type="pdf")
if pdf:
    reader = PdfReader(pdf)
    text = "".join([(p.extract_text() or "") + "\n" for p in reader.pages])
    st.info(f"PDF loaded: {len(text)} chars")
    chunks = [text[i:i+500] for i in range(0, len(text), 500) if text[i:i+500].strip()]
    
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(chunks)
    
    query = st.text_input("Ask question:", value="how many projects are there")
    if query:
        q_vec = vectorizer.transform([query])
        sims = cosine_similarity(q_vec, vectors)[0]
        top = sims.argsort()[-2:][::-1]
        for idx in top:
            st.write(f"**Score {sims[idx]:.2f}:** {chunks[idx]}")
            st.divider()