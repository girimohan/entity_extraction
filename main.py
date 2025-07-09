# main.py
# Core logic for Smart Entity Extraction and Document Clustering System

import fitz  # PyMuPDF
import spacy
from typing import List, Dict

# PDF Text Extraction Utility
def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Named Entity Recognition Utility
def extract_entities(text: str, model: str = "en_core_web_trf") -> List[Dict]:
    nlp = spacy.load(model)
    doc = nlp(text)
    entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
    return entities

if __name__ == "__main__":
    # Example usage
    pdf_path = "examples/sample.pdf"
    text = extract_text_from_pdf(pdf_path)
    entities = extract_entities(text)
    print(entities)
