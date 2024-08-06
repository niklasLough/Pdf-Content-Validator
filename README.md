# PDF Content Validator

## A Python web application written using Flask that allows users to upload PDF files, input data, and validate the content of the PDF against the provided inputs.

[![Python Badge](https://img.shields.io/badge/Python-3.6-blue?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)
[![Flask Badge](https://img.shields.io/badge/Flask-2.1.1-blue?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![pytest badge](https://img.shields.io/badge/pytest-white?style=for-the-badge&logo=pytest)](https://docs.pytest.org/en/latest/)


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
- PyMuPDF (Fitz)

### Installation
1. Clone the Repository
- `git clone https://github.com/yourusername/pdf-validator-app.git`
- `cd pdf-validator-app`

2. Install the Requirements
- `pip install -r requirements.txt`

### Running the Application
To run the web application, execute the following command:
`python3 app.py`

### Accessing the application through api endpoints

Using Postman to Access the api_upload Endpoint
1. Open Postman.
2. Create a new request.
3. Set the request type to POST.
4. Enter the URL: "your-machine"/api/upload.
5. Go to the Body tab.
6. Select form-data.
7. Add a key for the file:
- Key: pdf
- Type: File
- Value: Choose your PDF file from your local machine.
8. Send the request.

Using Postman to Access the api_validate Endpoint
1. Create a new request 
- Request type should still be set to POST.
2. Enter the URL: "your-machine"/api/validate.
3. Go to the Body tab.
4. Select raw and choose JSON from the dropdown menu.
5. Enter your JSON into the body:
´´´{
    "keyword": "your_keyword",
    "value": "your_value"
}´´´
6. Send the request.


Note: "your-machine" will look something like "http://127.0.0.1:5000"

### Unit Tests
Unit tests are provided to check the code works as expected. To run the tests, execute the following command:
`pytest`
