import pymupdf

def highlight_pdf(file_path, keyword, value):
    highlighted_file =pymupdf.open(file_path)
    for page in highlighted_file:
        text = page.get_text()
        if keyword in text and value in text:
            page.add_highlight_annot((0, 0, 0), text.find(keyword), text.find(value), text.find(value) + len(value))

    return highlighted_file