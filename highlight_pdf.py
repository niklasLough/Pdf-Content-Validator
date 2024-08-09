import fitz  # Same as the PyMuPDF library
import os

def highlight_pdf(file_path, keyword, value):
    """
    Highlight the keyword and value in the PDF file
    
    Args:
    file_path: str: The path to the PDF file
    keyword: str: The keyword to be highlighted
    value: str: The value to be highlighted
    
    Returns:
    file_path: str: The path to the new highlighted PDF file
    """
    doc = fitz.open(file_path)
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        page = clear_highlights(page)

        # Extract text blocks from the page
        blocks = page.get_text("blocks")
        for block in blocks:
            text = block[4] # The text content is at the 5th index of the block tuple
            if keyword.lower() in text.lower() and value.lower() in text.lower():
                # Highlight the entire block (line) which contains both the keyword and value
                rect = fitz.Rect(block[:4])
                highlight = page.add_highlight_annot(rect)
                highlight.update()
    # Save the document to a temporary file
    temp_file_path = file_path + '.highlight'
    doc.save(temp_file_path, garbage=4, deflate=True)
    doc.close()

    # Replace the original file with the temporary file
    os.replace(temp_file_path, file_path)
    return file_path


def highlight_pdf_from_csv(file_path, keyword_value_list):
    """
    Highlight the keyword and value in the PDF file
    
    Args:
    file_path: str: The path to the PDF file
    keyword_value_list: list: A list of tuples containing the keyword and value to be highlighted
    
    Returns:
    file_path: str: The path to the new highlighted PDF file
    """
    doc = fitz.open(file_path)
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        page = clear_highlights(page)

        # Extract text blocks from the page
        blocks = page.get_text("blocks")
        for block in blocks:
            text = block[4] # The text content is at the 5th index of the block tuple
            for keyword, value in keyword_value_list:
                if keyword.lower() in text.lower() and value.lower() in text.lower():
                    # Highlight the entire block (line) which contains both the keyword and value
                    rect = fitz.Rect(block[:4])
                    highlight = page.add_highlight_annot(rect)
                    highlight.update()
    # Save the document to a temporary file
    temp_file_path = file_path + '.highlight'
    doc.save(temp_file_path, garbage=4, deflate=True)
    doc.close()

    # Replace the original file with the temporary file
    os.replace(temp_file_path, file_path)
    return file_path


def clear_highlights(page):
    """
    Clear all previous highlights in the PDF file
    
    Args:
    page: fitz.Page: The page to clear the highlights from
    """
    annotations = page.annots()
    if annotations:
        for annot in annotations:
            if annot.type[0] == 8:  # Type 8 means the annotations is a highlight
                page.delete_annot(annot)
    return page
