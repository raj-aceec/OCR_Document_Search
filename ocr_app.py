import streamlit as st
import pytesseract
from pytesseract import image_to_string
from PIL import Image
import json
import os

# Path for Tesseract OCR executable (if running locally)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  

# Directory to store extracted text
EXTRACTED_TEXT_PATH = "extracted_text"
if not os.path.exists(EXTRACTED_TEXT_PATH):
    os.makedirs(EXTRACTED_TEXT_PATH)

def save_extracted_text(extracted_text):
    with open(f"{EXTRACTED_TEXT_PATH}/extracted_output.json", "w", encoding='utf-8') as f:
        json.dump(extracted_text, f, ensure_ascii=False, indent=4)

def ocr_process(image):
    # Perform OCR using Tesseract
    extracted_text = image_to_string(image, lang='eng+hin')  # Supports both English and Hindi
    return extracted_text

def search_keywords(extracted_text, keyword):
    # Basic keyword search
    results = []
    lines = extracted_text.split('\n')
    for idx, line in enumerate(lines):
        if keyword.lower() in line.lower():
            results.append((idx + 1, line))
    return results

def main():
    st.title("OCR and Document Search Application")
    st.write("Upload an image containing Hindi and English text for OCR processing and keyword search.")

    # Image Upload
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        st.write("Extracting text...")
        
        # Extract text from image
        extracted_text = ocr_process(image)
        st.write("Extracted Text:")
        st.write(extracted_text)
        
        # Save extracted text to file
        save_extracted_text({"extracted_text": extracted_text})
        
        # Keyword Search
        st.write("### Search for Keywords in Extracted Text")
        keyword = st.text_input("Enter keyword")
        
        if keyword:
            results = search_keywords(extracted_text, keyword)
            if results:
                st.write(f"Found {len(results)} matching line(s):")
                for line_num, line in results:
                    st.write(f"Line {line_num}: {line}")
            else:
                st.write("No matches found.")

if __name__ == "__main__":
    main()
