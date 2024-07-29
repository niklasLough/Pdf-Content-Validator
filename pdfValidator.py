#Program to validate the presence of specific elements within a PDF file

#Importing necessary libraries
import re
import PyPDF2 # For splitting, merging, cropping, and transforming the pages of PDF files
from pdfminer.high_level import extract_text as pdfminer_extract_text # For extracting information from PDF documents


# Function to extract text from a PDF file
def extract_pdf_text(pdf_file):
    # Extract text from a PDF file using pdfminer
    text = pdfminer_extract_text(pdf_file)
    return text


def validate_pdf(file_path):
    text = extract_pdf_text(file_path)
    print(text)
    return text 
    # Here we will return the relevant information about the validity of the inputs
    # Will have to put in more arguments later, such as the key values they are looking for
    # The prompt for this will appear after the user has uploaded a file

