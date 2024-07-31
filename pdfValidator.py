#Program to validate the presence of specific elements within a PDF file

#Importing necessary libraries
import re
# import PyPDF2 # For splitting, merging, cropping, and transforming the pages of PDF files
from pdfminer.high_level import extract_pages, extract_text # For extracting information from PDF documents
import pdfplumber

import pdfplumber

def test_extract_pdf_text(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        for page_number, page in enumerate(pdf.pages):
            print(f"\n--- Page {page_number + 1} ---")

            # Extract and print text
            text = page.extract_text()
            if text:
                print("\nText:")
                print(text)
                list = re.split('\n', text)
            print(text)
            # return list


def extract_pdf_text(pdf_file):
    # Extract text from a PDF file using pdfminer
    text = extract_text(pdf_file)
    # print(text)
    return text


def validate_pdf(file_path, keyword, value):
    test_extract_pdf_text(file_path)
    pdf_text = extract_pdf_text(file_path)
    # extract_pdf_elements(file_path)
    
    # Check if the keyword and value are present in the PDF text
    keyword_found = False
    value_found = False
    myList = re.split('\n', pdf_text)
    # print(myList)
    for line in myList:
        if keyword.lower() in line.lower():
            keyword_found = True 
        if value.lower() in line.lower():
            value_found = True
    if keyword_found and value_found:
        # print("The keyword and value are present in the PDF file")
        return True
    else:
        return False
    







# def test_extract_pdf_text(pdf_file):
#     # Extract text using pdfminer
#     text = extract_text(pdf_file)

#     # Debug print the extracted text
#     print("Extracted Text:")
#     print(text)
    
#     with pdfplumber.open(pdf_file) as pdf:
#         for page_number, page in enumerate(pdf.pages):
#             print(f"\nPage {page_number + 1}")
            
#             # Extract and print raw table data
#             tables = page.extract_tables()
#             if tables:
#                 print("Tables found:")
#                 for table_index, table in enumerate(tables):
#                     print(f"\nTable {table_index + 1}")
#                     for row in table:
#                         print(row)
#             else:
#                 print("No tables found on this page.")

#     return text



# def extract_tables_with_camelot(pdf_file):
#     # Use PdfReader to read the PDF file
#     reader = PdfReader(pdf_file)
#     number_of_pages = len(reader.pages)
    
#     # Extract tables using camelot
#     tables = camelot.read_pdf(pdf_file, pages='all', flavor='stream')
#     for table_index, table in enumerate(tables):
#         print(f"\nTable {table_index + 1}")
#         print(table.df)  # Prints the DataFrame of the table