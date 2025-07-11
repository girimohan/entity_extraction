import streamlit as st
st.set_page_config(
    page_title="Entity Extraction Tool",
    page_icon="🐨",
    layout="centered"
)

# Streamlit UI for Smart Entity Extraction and Document Clustering
import pandas as pd
import os
import tempfile
import spacy
import subprocess

# Ensure spaCy transformer model is installed
try:
    spacy.load("en_core_web_trf")
except OSError:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_trf"], check=True)

from text_extractor import extract_text_from_pdf, extract_named_entities

# Main app
st.title("🐨 Smart Entity Extraction and Document Clustering")
st.markdown("Upload PDF files to extract named entities and analyze your documents.")

# File uploader
uploaded_files = st.file_uploader(
    "Choose PDF files", 
    type="pdf", 
    accept_multiple_files=True,
    help="Upload one or more PDF files to extract entities"
)

if uploaded_files:
    st.markdown(f"### Processing {len(uploaded_files)} file(s)...")
    
    for uploaded_file in uploaded_files:
        with st.expander(f"📄 {uploaded_file.name}"):
            try:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.getbuffer())
                    tmp_file_path = tmp_file.name
                
                # Extract text and entities
                with st.spinner("Extracting text and entities..."):
                    text = extract_text_from_pdf(tmp_file_path)
                    entities = extract_named_entities(text)
                
                # Display results
                if entities:
                    st.subheader("📊 Extracted Entities")
                    df = pd.DataFrame(entities)
                    st.dataframe(df, use_container_width=True)
                    
                    # Show entity counts
                    if not df.empty:
                        entity_counts = df['label'].value_counts()
                        st.subheader("📈 Entity Distribution")
                        st.bar_chart(entity_counts)
                    
                    # Download option
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="💾 Download as CSV",
                        data=csv,
                        file_name=f"{uploaded_file.name}_entities.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No entities found in this document.")
                
                # Clean up temporary file
                os.unlink(tmp_file_path)
                
            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                
else:
    st.info("👆 Upload PDF files above to get started!")
    
    # Show example
    with st.expander("ℹ️ About this tool"):
        st.markdown("""
        This tool extracts named entities from PDF documents using Natural Language Processing (NLP).
        
        **Supported entity types:**
        - PERSON: People's names
        - ORG: Organizations, companies
        - GPE: Countries, cities, states
        - MONEY: Monetary values
        - DATE: Dates and times
        - And many more!
        
        **How to use:**
        1. Upload one or more PDF files
        2. View extracted entities in a table
        3. Download results as CSV
        """)
