import streamlit as st
import pyttsx3
import pdfplumber
import os
from pathlib import Path
import re

# Function to slugify the filename
def slugify(filename):
    # Remove non-alphanumeric characters, replace spaces with hyphens, and make lowercase
    filename = re.sub(r'[^\w\s-]', '', filename).strip().lower()
    return re.sub(r'[-\s]+', '-', filename)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to convert text to speech and save it as an audiobook
def convert_text_to_speech(text, output_file):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Adjust speaking rate here
    engine.save_to_file(text, output_file)
    engine.runAndWait()

# Streamlit app
st.title("PDF to Audiobook Converter")
# st.subheader("Generate an Audibook file from PDF.") # Use this or the following
st.markdown("##### Generate an Audibook file from PDF.")

# Step 1: File uploader for PDF
uploaded_pdf = st.file_uploader("Upload a PDF file", type="pdf")

# Step 2: Button to generate audiobook
if uploaded_pdf is not None:
    # Extract filename and slugify it to create the output filename
    pdf_filename = uploaded_pdf.name
    slugified_name = slugify(Path(pdf_filename).stem)  # Get the slugified name without extension
    output_mp3_filename = f"{slugified_name}.mp3"

    if st.button("Generate Audiobook"):
        with st.spinner('Converting PDF to audiobook...'):
            # Step 3: Extract text from the uploaded PDF
            text = extract_text_from_pdf(uploaded_pdf)

            # Step 4: Convert text to audiobook with slugified output file name
            convert_text_to_speech(text, output_mp3_filename)

            # Step 5: Display download button after audiobook is created
            if Path(output_mp3_filename).exists():
                st.success(f"Audiobook '{output_mp3_filename}' generated successfully!")
                st.audio(output_mp3_filename, format='audio/mp3')
                with open(output_mp3_filename, "rb") as file:
                    btn = st.download_button(
                        label="Download Audiobook",
                        data=file,
                        file_name=output_mp3_filename,
                        mime="audio/mpeg"
                    )
            else:
                st.error("Failed to generate audiobook.")
