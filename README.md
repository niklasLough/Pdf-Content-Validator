# PDF Content Validator

## A Python web application wriiten using Flask that allows users to upload PDF files, input data, and validate the content of the PDF against the provided inputs.


### Features
- Upload PDF File: Users can upload a PDF file to the server.
- Input Data: Users can input a keyword and a value to be searched and validated in the PDF.
- Validation: The application validates if the keyword and value are present on the same line in the PDF.
- Confirmation: The result of this validation is shown and the keyword and value occurences are highlighted in the PDF.
- Help Page: A help page can be used by the user to aid them.


### Prerequisites
- Python 3.6 or higher
- Flask
- Flask-WTF
- Werkzeug
- PyPDF2 (or another PDF manipulation library)
- PDFPlumber
- PyMuPDF

### Installation
1. Clone the Repository
- `git clone https://github.com/yourusername/pdf-validator-app.git`
- `cd pdf-validator-app`

2. Install the Requirements
- `pip install -r requirements.txt`

### Running the Application
To run the application, execute the following command:
`python3 app.py`

### Unit Tests
Unit tests are provided to check the code works as expected. To run the tests, execute the following command:
`pytest`
