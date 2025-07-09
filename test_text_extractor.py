from text_extractor import extract_text_from_pdf, extract_named_entities

pdf_text = extract_text_from_pdf("sample_docs/startup_overview.pdf")
entities = extract_named_entities(pdf_text)

print("Extracted Text Sample:", pdf_text[:500])
print("\nNamed Entities:")
for ent, label in entities:
    print(f"{label}: {ent}")
