"""
PDF processing module - extracts text and metadata from PDFs
"""
import PyPDF2
import os

def extract_text_from_pdf(filepath):
    """Extract all text from a PDF file"""
    try:
        text = ""
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += f"\n--- Page {page_num + 1} ---\n"
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return ""

def get_pdf_info(filepath):
    """Get metadata from PDF"""
    try:
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            info = {
                'pages': len(reader.pages),
                'title': reader.metadata.title if reader.metadata else 'N/A',
                'author': reader.metadata.author if reader.metadata else 'N/A'
            }
            return info
    except Exception as e:
        print(f"Error reading PDF info: {e}")
        return {}
