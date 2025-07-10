# text_extractor.py
# PDF text extraction and Named Entity Recognition utilities

import fitz  # PyMuPDF
import spacy
from typing import List, Dict
import streamlit as st

@st.cache_resource
def load_spacy_model():
    """Load spaCy model with caching for better performance"""
    try:
        # Try the transformer model first
        nlp = spacy.load("en_core_web_trf")
        return nlp
    except OSError:
        try:
            # Fallback to smaller model which should be available
            nlp = spacy.load("en_core_web_sm")
            st.warning("Using smaller spaCy model (en_core_web_sm) as the transformer model is not available.")
            return nlp
        except OSError:
            st.error("No spaCy models found. Please check the installation.")
            return None

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF file"""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def extract_named_entities(text: str) -> List[Dict]:
    """Extract named entities from text using spaCy"""
    if not text.strip():
        return []
    
    nlp = load_spacy_model()
    if nlp is None:
        return []
    
    try:
        # Process text in chunks if it's too long
        max_length = 1000000  # 1MB limit for spaCy
        if len(text) > max_length:
            text = text[:max_length]
        
        doc = nlp(text)
        entities = []
        
        for ent in doc.ents:
            entities.append({
                "text": ent.text.strip(),
                "label": ent.label_,
                "description": spacy.explain(ent.label_)
            })
        
        return entities
    except Exception as e:
        raise Exception(f"Error extracting entities: {str(e)}")
