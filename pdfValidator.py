#Program to validate the presence of specific elements within a PDF file
import re
import pdfplumber
# from pdfminer.high_level import extract_text

def extract_pdf_text(pdf_file):
    pdf_list = []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            
            # Extract text from the page
            text = page.extract_text()
            if text:
                # print("\n",text)
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
    # print(pdf_list)
    return pdf_list  # Correctly return the list of lines


def validate_price(pdf_list):
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
    
    print("Total price", total_price)
    print("Total listed price", total_listed_price)
    if int(total_listed_price) == int(total_price):       
        print("hello")
        return True
    return False

    
def validate_pdf(file_path, keyword, value):
    pdf_list = extract_pdf_text(file_path)
    # If the PDF is a booking confirmation then validate price sum
    price_validated = None #TODO Try if its None
    if "Confirmation" in pdf_list[0] or "Buchungsbestätigung" in pdf_list[0]:
        price_validated = validate_price(pdf_list)

    # Check if the keyword and value are present in the same line in the PDF 
    found = False
    for line in pdf_list:
        if keyword.lower() in line.lower() and value.lower() in line.lower():
            found = True
            break

    return found, price_validated
    
    # # Return the correct results to the app
    # if found and price_validated:
    #     return True, True
    # elif found:
    #     return True, False
    # elif price_validated:
    #     return False, True
    # return False, False

    





# def extract_pdf_text(pdf_file):
#     # Extract text from a PDF file using pdfminer
#     text = extract_text(pdf_file)
#     return text

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