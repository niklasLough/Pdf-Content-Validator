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


def validate_pdf(file_path, keyword, value):
    pdf_text = extract_pdf_text(file_path)
    # print(pdf_text)
    # print(keyword)
    # print(value)
    # print("Hello from pdfValidator.py")

    # Check if the keyword and value are present in the PDF text
    keyword_found = False
    value_found = False
    myList = re.split('\n', pdf_text)
    print(myList)
    for line in myList:
        for word in line.split():
            if keyword.lower() == word.lower():
                keyword_found = True 
            if value.lower() == word.lower():
                value_found = True
    if keyword_found and value_found:
        print("The keyword and value are present in the PDF file")
        return True
    

