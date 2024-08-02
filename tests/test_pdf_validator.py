import pytest
from unittest.mock import patch, MagicMock
from pdf_validator import extract_pdf_text, validate_price, validate_pdf

@pytest.fixture
def mock_pdf():
    """Fixture to create a mock PDF."""
    mock_pdf = MagicMock()
    mock_page = MagicMock()
    mock_page.extract_text.return_value = "This is a sample text\nPrix total 1.234,56\nGast 123,45\nClient 234,56"
    mock_page.extract_tables.return_value = []
    mock_pdf.pages = [mock_page, mock_page]
    return mock_pdf

@patch('pdfplumber.open')
def test_extract_pdf_text(mock_open, mock_pdf):
    mock_open.return_value.__enter__.return_value = mock_pdf
    result = extract_pdf_text("dummy.pdf")
    assert result == ['This is a sample text', 'Prix total 1.234,56', 'Gast 123,45', 'Client 234,56']

def test_validate_price():
    pdf_list = [
        "This is a sample text",
        "Prix total 1.234,56",
        "Gast 123,45",
        "Client 234,56"
    ]
    assert validate_price(pdf_list) is True

@patch('pdf_validator.extract_pdf_text')
@patch('pdf_validator.validate_price')
def test_validate_pdf_with_mocks(mock_validate_price, mock_extract_pdf_text):
    mock_extract_pdf_text.return_value = [
        "This is a sample text",
        "Confirmation",
        "Prix total 1.234,56",
        "Gast 123,45",
        "Client 234,56"
    ]
    mock_validate_price.return_value = True

    found, price_validated = validate_pdf("dummy.pdf", "sample", "text")
    assert found is True
    assert price_validated is True

    found, price_validated = validate_pdf("dummy.pdf", "missing", "text")
    assert found is False
    assert price_validated is True
