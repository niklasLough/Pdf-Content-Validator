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
        text_instances = page.search_for(keyword.lower())
        for inst in text_instances:
            highlight = page.add_highlight_annot(inst)
            highlight.update()
        text_instances = page.search_for(value.lower())
        for inst in text_instances:
            highlight = page.add_highlight_annot(inst)
            highlight.update()

    # Save the document to a temporary file
    temp_file_path = file_path + '.highlight'
    doc.save(temp_file_path, garbage=4, deflate=True)
    doc.close()

    # Replace the original file with the temporary file
    os.replace(temp_file_path, file_path)
    return file_path
