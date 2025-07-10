# app.py
# Streamlit UI for Smart Entity Extraction and Document Clustering System

import streamlit as st
import pandas as pd
from text_extractor import extract_text_from_pdf, extract_named_entities
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import tempfile

st.set_page_config(page_title="Smart Entity Extraction & Document Clustering", layout="wide")

# Center the main content using Streamlit columns
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.title("Smart Entity Extraction & Document Clustering")
    st.markdown("""
    <style>
    .subtitle {text-align: center; font-size: 1.2em; color: #555; margin-bottom: 1.5em;}
    .stDataFrame {margin-left: auto !important; margin-right: auto !important;}
    .stButton>button {width: 100%;}
    </style>
    <div class="subtitle">A professional tool for extracting named entities, generating embeddings, and clustering documents.<br>Built with <b>spaCy</b>, <b>Hugging Face</b>, and <b>Streamlit</b>.</div>
    """, unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Upload PDF document(s)", type=["pdf"], accept_multiple_files=True)

    if uploaded_files:
        docs = []
        all_entities = []
        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name
            text = extract_text_from_pdf(tmp_path)
            entities = extract_named_entities(text)
            docs.append({"filename": uploaded_file.name, "text": text, "entities": entities})
            all_entities.append(" ".join([e[0] for e in entities]))

        st.markdown("<h3 style='text-align:center;'>Extracted Entities Table</h3>", unsafe_allow_html=True)
        entity_rows = []
        label_counts = {}
        for doc in docs:
            for ent, label in doc["entities"]:
                entity_rows.append({"Document": doc["filename"], "Entity": ent, "Label": label})
                label_counts[label] = label_counts.get(label, 0) + 1
        df_entities = pd.DataFrame(entity_rows)
        st.dataframe(df_entities.style.set_properties(subset=["Label"], **{"width": "200px"}), use_container_width=True)

        st.markdown("<h3 style='text-align:center;'>Entity Counts by Label</h3>", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(list(label_counts.items()), columns=["Label", "Count"]))

        st.markdown("<h3 style='text-align:center;'>Document Embedding & Clustering</h3>", unsafe_allow_html=True)
        embed_model = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = embed_model.encode([doc["text"] for doc in docs])
        n_clusters = min(5, len(docs)) if len(docs) > 1 else 1
        if n_clusters > 1:
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            cluster_ids = kmeans.fit_predict(embeddings)
        else:
            cluster_ids = [0] * len(docs)
        for i, doc in enumerate(docs):
            doc["cluster_id"] = int(cluster_ids[i])
        df_clusters = pd.DataFrame({
            "Document": [doc["filename"] for doc in docs],
            "Cluster": cluster_ids
        })
        st.dataframe(df_clusters)

        st.markdown("<h3 style='text-align:center;'>Cluster Visualization</h3>", unsafe_allow_html=True)
        if len(docs) > 1:
            from sklearn.decomposition import PCA
            pca = PCA(n_components=2)
            reduced = pca.fit_transform(embeddings)
            fig, ax = plt.subplots()
            scatter = ax.scatter(reduced[:,0], reduced[:,1], c=cluster_ids, cmap="tab10", s=100)
            for i, doc in enumerate(docs):
                ax.annotate(doc["filename"], (reduced[i,0], reduced[i,1]), fontsize=8)
            plt.xlabel("PCA 1")
            plt.ylabel("PCA 2")
            plt.title("Document Clusters (PCA)")
            st.pyplot(fig)

        st.markdown("<h3 style='text-align:center;'>Download Results</h3>", unsafe_allow_html=True)
        csv = df_entities.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        st.markdown(f'<div style="text-align:center;"><a href="data:file/csv;base64,{b64}" download="entities.csv" style="font-size:1.1em; color:#fff; background:#4F8BF9; padding:0.5em 1.5em; border-radius:6px; text-decoration:none;">Download Entities CSV</a></div>', unsafe_allow_html=True)
