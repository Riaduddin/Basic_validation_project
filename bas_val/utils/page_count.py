import fitz
from docx2pdf import convert
from docx import Document
from bas_val.logger import logging
import sys
from bas_val.exception import bas_val_Exception

# def count_pages(docx_path):
#     try:
#         doc = Document(docx_path)
#         sections = doc.sections
#         num_pages = 0
       
#         for section in sections:
#             print("sections :",section.page_height)

#             num_pages += section.page_height // 16833.6  # Assuming default page height is 1440 twips

#         return num_pages
#     except Exception as e:
#         print(f"Error counting pages: {e}")
#         return None

# def counting_page(file_path):

#     doc = fitz.open(convert(file_path))
#     num_page=0
#     text_area=list()
#     for i in range(len(doc)): 
#         # Select the first page of the PDF
#         page = doc[i]

#         # Loop through all the text blocks on the page and add up their areas
#         total_area = 0
#         for block in page.get_text_blocks():
#             rect = fitz.Rect(block[:4])
#             total_area += rect.width * rect.height

#         # Calculate the area of the page
#         page_area = page.rect.width * page.rect.height
    
#         # Calculate the percentage of the page covered by text
#         text_coverage = total_area/page_area * 100
#         if text_coverage>=75:
#             num_page+=1
#         else:
#             num_page+=.5
#         text_area.append(text_coverage)
#     return num_page

# def counting_pages(pdf_path):
#     try:
#         # Open PDF using fitz
#         doc = fitz.open(pdf_path)
        
#         # Count the number of pages
#         num_pages = len(doc)
        
#         return num_pages
#     except Exception as e:
#         print(f"Error counting pages: {e}")
#         return None

# def convert_and_count_pages(docx_path):
#     try:
#         # Convert DOCX to PDF
#         convert(docx_path)
        
#         # Assuming the PDF has the same name as DOCX but with .pdf extension
#         pdf_path = docx_path.replace(".docx", ".pdf")
        
#         # Count pages of the converted PDF
#         num_pages = counting_pages(pdf_path)
        
#         return num_pages
#     except Exception as e:
#         print(f"Error converting or counting pages: {e}")
#         return None

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
        print(docx_path)
        logging.info("Entering the convert and count pages")
        # Create an 'upload' folder if it doesn't exist
        upload_folder = os.path.join(os.getcwd(), "upload")
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        logging.info('Created upload folders')
        #pdf_filename = os.path.join(os.path.dirname(docx_path), os.path.basename(docx_path).replace(".docx", ".pdf"))
        #print('pdf filename: ',pdf_filename)
        # pdf_path=os.path.join(upload_folder,pdf_filename)
        # print('1st_pdf_path:',pdf_path)
        # Convert DOCX to PDF
        logging.info("Start Converting the pdf")
        convert(input_path=docx_path)
        
        # Move the converted PDF to the 'upload' folder
        # pdf_path = os.path.join(os.path.dirname(docx_path), os.path.basename(docx_path).replace(".docx", ".pdf"))
        # print('1st_pdf_path:',pdf_path)
        #shutil.move(pdf_path, os.path.join(upload_folder, os.path.basename(pdf_path)))
        
        # PDF path after moving
        # pdf_path = os.path.join(upload_folder, os.path.basename(pdf_path))
        # print('2nd_pdf_path:',pdf_path)
        
        # Count pages of the converted PDF from the 'upload' folder
        logging.info("Counting the page")
        num_pages = counting_pages(pdf_path)
        logging.info("Exiting from the convert and count pages")
        return num_pages
    except Exception as e:
        #print(f"Error converting or counting pages: {e}")
        return bas_val_Exception(sys,e)