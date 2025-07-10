# Smart Entity Extraction and Document Clustering System

## Concept
A modern web app for extracting named entities from PDFs, generating embeddings, and clustering similar documents. Built for business, research, legal, and analytics use cases. Upload documents, extract insights, and visualize clusters—all in your browser.

## Overview
A Python-based AI system for extracting named entities from PDFs or HTML, generating embeddings, and clustering similar documents. Features a Streamlit UI for easy interaction.

## Features
- PDF/HTML text extraction
- Named Entity Recognition (NER)
- Embedding & clustering
- Streamlit frontend
- Deployable to Hugging Face Spaces or Render

## Quickstart
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_trf
   ```
2. Run the app:
   ```bash
   streamlit run app.py
   ```

## Folder Structure
- `main.py` — core logic
- `app.py` — Streamlit UI
- `requirements.txt` — dependencies
- `/examples/` — sample PDFs/HTML

## Deployment
- Ready for Hugging Face Spaces or Render

## License
MIT
