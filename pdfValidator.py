#Program to validate the presence of specific elements within a PDF file

#Importing necessary libraries
import re
import PyPDF2 # For splitting, merging, cropping, and transforming the pages of PDF files
from pdfminer.high_level import extract_text as pdfminer_extract_text # For extracting information from PDF documents

#Importing other files
from importPdf import upload_pdf # For importing a PDF file from the user

# Function to extract text from a PDF file
def extract_pdf_text(pdf_file):
    # Extract text from a PDF file using pdfminer
    text = pdfminer_extract_text(pdf_file)
    text = extract_pdf_text(pdf_file)
    return text


def main():
    pdf_file = upload_pdf() 
    text = extract_pdf_text(pdf_file)
    print(text)
    return

if __name__ == "__main__":
    main()
