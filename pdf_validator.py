#Program to validate the presence of specific elements within a PDF file
import re
import pdfplumber

def extract_pdf_text(pdf_file):
    """
    Extract text from a PDF file
    
    Args:
    pdf_file: str: The path to the PDF file
    
    Returns:
    pdf_list: list: A list of lines of text extracted from the PDF file
    """
    pdf_list = []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            
            # Extract text from the page
            text = page.extract_text()
            if text:
                page_list = re.split('\n', text)
                pdf_list.extend(page_list)

            # Extract text tables on the page
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    for row in table:
                        # Replace None values with empty strings to allow joining
                        row = [cell if cell is not None else "" for cell in row]
                        row_text = " ".join(row)
                        pdf_list.append(row_text)

    return pdf_list


def validate_price(pdf_list):
    """
    Validate the total price in the PDF file if it is a booking confirmation
    Note: This is only relevant for users from the company I was interned at

    Args:
    pdf_list: list: A list of lines of text extracted from the PDF file

    Returns:
    bool: True if the total price is correct, False otherwise
    """
    total_listed_price = 0
    
    for line in pdf_list:
        if "Prix total" in line or "Gesamtpreis" in line:
            total_price = re.findall(r'\d{1,3}(?:\.\d{3})*,\d{2}', line)
            if total_price:
                total_price = total_price[0].replace('.', '').replace(',', '')

        if "Gast" in line or "Client" in line:
            client_price = re.findall(r'\d{1,3}(?:\.\d{3})*,\d{2}', line)
            if client_price:
                client_price = client_price[0].replace('.', '').replace(',', '')
                total_listed_price += int(client_price)

    if int(total_listed_price) == int(total_price):       
        return True
    return False

    
def validate_pdf(file_path, keyword, value):
    """
    Validate the presence of the keyword and value on the same line in the PDF file

    Args:
    file_path: str: The path to the PDF file
    keyword: str: The keyword to be validated
    value: str: The value to be validated

    Returns:
    bool: True if the keyword and value are present on the same line in the PDF file, False otherwise
    """
    pdf_list = extract_pdf_text(file_path)
    price_validated = None
    # If the PDF is a booking confirmation then validate price sum
    if "Conﬁrmation" in pdf_list[0] or "Confirmation" in pdf_list[0] or "Buchungsbestätigung" in pdf_list[0]:
        price_validated = validate_price(pdf_list)

    # Check if the keyword and value are present in the same line in the PDF 
    found = False
    for line in pdf_list:
        if keyword.lower() in line.lower() and value.lower() in line.lower():
            found = True
            break

    return found, price_validated
