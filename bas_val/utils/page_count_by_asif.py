import os
import shutil
from docx2pdf import convert
import fitz  # PyMuPDF

def counting_pages(pdf_path):
    try:
        # Open PDF using fitz
        doc = fitz.open(pdf_path)
        
        # Count the number of pages
        num_pages = len(doc)
        
        return num_pages
    except Exception as e:
        print(f"Error counting pages: {e}")
        return None

def convert_and_count_pages(docx_path):
    try:
        # Create an 'upload' folder if it doesn't exist
        upload_folder = os.path.join(os.path.dirname(docx_path), "upload")
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        # Convert DOCX to PDF
        convert(docx_path)
        
        # Move the converted PDF to the 'upload' folder
        pdf_path = os.path.join(os.path.dirname(docx_path), os.path.basename(docx_path).replace(".docx", ".pdf"))
        shutil.move(pdf_path, os.path.join(upload_folder, os.path.basename(pdf_path)))
        
        # PDF path after moving
        pdf_path = os.path.join(upload_folder, os.path.basename(pdf_path))
        
        # Count pages of the converted PDF from the 'upload' folder
        num_pages = counting_pages(pdf_path)
        
        return num_pages
    except Exception as e:
        print(f"Error converting or counting pages: {e}")
        return None

# Example usage:
#docx_path = "/Users/asif/vscode/LegoIO/static/B-JET CV_Template_14th.docx"

# num_pages = convert_and_count_pages(docx_path)
# if num_pages is not None:
#     print(f"Number of pages in the converted PDF: {num_pages}")
