# app.py
# Streamlit UI for Smart Entity Extraction and Document Clustering System

import streamlit as st
from main import extract_text_from_pdf, extract_entities
import tempfile

st.title("Smart Entity Extraction & Document Clustering")

uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name
    text = extract_text_from_pdf(tmp_path)
    st.subheader("Extracted Text (first 500 chars)")
    st.write(text[:500] + ("..." if len(text) > 500 else ""))
    entities = extract_entities(text)
    st.subheader("Named Entities")
    st.write(entities)
