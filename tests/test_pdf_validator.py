import pytest
import fitz
from unittest.mock import patch, MagicMock
from pdf_validator import extract_pdf_text, validate_price, validate_pdf

@pytest.fixture
# Fixtures set up a pre-defined context for tests
def mock_pdf():
    """Create a mock PDF to then test with."""
    mock_pdf = MagicMock() # Fixture to create a mock PDF
    mock_page = MagicMock()
    mock_page.extract_text.return_value = "This is sample text\nPrix total 300,00\nGast 200,00\nClient 100,00"
    mock_page.extract_tables.return_value = []
    mock_pdf.pages = [mock_page, mock_page] # Mock PDF with two identical pages
    return mock_pdf

@patch('pdfplumber.open')
def test_extract_pdf_text(mock_open, mock_pdf):
    mock_open.return_value.__enter__.return_value = mock_pdf # Mock the pdfplumber.open function to return the mock PDF
    result = extract_pdf_text("dummy.pdf")
    assert result == ['This is sample text', 'Prix total 300,00', 'Gast 200,00', 'Client 100,00',
                    'This is sample text', 'Prix total 300,00', 'Gast 200,00', 'Client 100,00']
                    # The result should be the text from both pages combined

def test_validate_price():
    pdf_list = [
        "This is sample text",
        "Prix total 300,00",
        "Gast 200,00",
        "Client 100,00"
    ]
    assert validate_price(pdf_list) is True

@patch('pdf_validator.extract_pdf_text')
@patch('pdf_validator.validate_price')
def test_validate_pdf_with_mocks(mock_validate_price, mock_extract_pdf_text):
    mock_extract_pdf_text.return_value = [
        "Confirmation",
        "This is sample text",
        "Prix total 300,00",
        "Gast 200,00",
        "Client 100,00"
    ]
    mock_validate_price.return_value = True

    found, price_validated = validate_pdf("dummy.pdf", "sample", "text")
    assert found is True
    assert price_validated is True

    found, price_validated = validate_pdf("dummy.pdf", "simple", "text")
    assert found is False
    assert price_validated is True
