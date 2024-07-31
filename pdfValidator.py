#Program to validate the presence of specific elements within a PDF file

#Importing necessary libraries
import re
import PyPDF2 # For splitting, merging, cropping, and transforming the pages of PDF files
from pdfminer.high_level import extract_pages, extract_text # For extracting information from PDF documents
import tabula # For extracting tables from PDF files


def test_extract_pdf_text(pdf_file):
    # Extract text using pdfminer
    text = extract_text(pdf_file)

    table_text = tabula.read_pdf(pdf_file, pages='all', multiple_tables=True)

    text += table_text
    
    # with pdfplumber.open(pdf_file) as pdf:
    #     # Iterate through pages
    #     for page_number, page in enumerate(pdf.pages):
    #         # Extract tables
    #         tables = page.extract_tables()
    #         for table in tables:
    #             for row in table:
    #                 print(row)
    return text

# Function to extract text from a PDF file
def extract_pdf_text(pdf_file):
    # Extract text from a PDF file using pdfminer
    text = extract_text(pdf_file)
    print(text)
    return text


def validate_pdf(file_path, keyword, value):
    pdf_text = extract_pdf_text(file_path)
    
    # Convert to lowercase so search isn't case sensitive
    pdf_text_lower = pdf_text.lower()
    keyword_lower = keyword.lower()
    value_lower = value.lower()
    
    keyword_found = keyword_lower in pdf_text_lower
    value_found = value_lower in pdf_text_lower
    
    return keyword_found and value_found
    

