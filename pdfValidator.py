#Program to validate the presence of specific elements within a PDF file

import re
import PyPDF2 # For splitting, merging, cropping, and transforming the pages of PDF files
from pdfminer.high_level import extract_text as pdfminer_extract_text # For extracting information from PDF documents

# Function to upload a PDF file to the application
def upload_pdf():
    # Upload a PDF file
    print("Upload a PDF file")
    # Functionality


# Function to extract text from a PDF file
def extract_pdf_text(pdf_file):
    # Extract text from a PDF file using pdfminer
    text = pdfminer_extract_text(pdf_file)
    return text


def main(): 
    text = extract_pdf_text("ResConfirmFr1.pdf")
    print(text)
    return

if __name__ == "__main__":
    main()
















# from PyPDF2 import PdfReader

# pdf_reader = PdfReader("ReservationConfirmationFr1.pdf")

# page_content = {}

# for index, pdf_page in enumerate(pdf_reader.pages):
#     page_content[index+1] = pdf_page.extract_text()

# print(page_content)



