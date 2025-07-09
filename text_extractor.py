# text_extractor.py
# PDF text extraction and Named Entity Recognition utilities

import fitz  # PyMuPDF
import spacy
from collections import defaultdict
from typing import List, Tuple

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts and returns the full text from a PDF file using PyMuPDF.
    """
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

def extract_named_entities(text: str) -> List[Tuple[str, str]]:
    """
    Extracts named entities from text using SpaCy's en_core_web_trf model.
    Returns a list of (entity_text, entity_label) tuples, filtered for duplicates/overlaps.
    Also prints the number of entities per label type.
    """
    nlp = spacy.load("en_core_web_trf")
    doc = nlp(text)
    seen = set()
    entities = []
    label_counts = defaultdict(int)
    for ent in doc.ents:
        key = (ent.text.strip(), ent.label_)
        if key not in seen:
            seen.add(key)
            entities.append(key)
            label_counts[ent.label_] += 1
    print("Entity counts by label:")
    for label, count in label_counts.items():
        print(f"  {label}: {count}")
    return entities
