# PDF Content Validator

## A Python web application written using Flask that allows users to upload PDF files, input data, and validate the content of the PDF against the inputs.

[![Python Badge](https://img.shields.io/badge/Python-3.6-blue?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)
[![Flask Badge](https://img.shields.io/badge/Flask-2.1.1-blue?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![pytest badge](https://img.shields.io/badge/pytest-white?style=for-the-badge&logo=pytest)](https://docs.pytest.org/en/latest/)


### Features
* Upload PDF File: Users can upload a PDF file to the server.
* Input Data: Users can input a keyword and a value to be searched and validated in the PDF.
* Validation: The application validates if the keyword and value are present on the same line in the PDF.
* Confirmation: The result of this validation is shown and the keyword and value occurences are highlighted in the PDF.
* Help Page: A help page can be used by the user to aid them.


### Prerequisites
* Python 3.6 or higher
* Flask
* Flask-WTF
* Werkzeug
* PDFPlumber
* PyMuPDF (Fitz)

### Installation
1. Clone the Repository
   * `git clone https://github.com/yourusername/pdf-validator-app.git`

2. Install the Requirements
    * `pip install -r requirements.txt`

### Running the Web Application

1. Run the Flask Application:
    * Open a terminal.
    * Navigate to the directory containing your app.py file.
    * Run the command: `  python app.py  `
    * The application will start, and you should see output indicating that it is running on http://127.0.0.1:5000.
2. Open the Web Interface:
    * Go to http://127.0.0.1:5000 on your preferred web browser
    * You will see the home page where you can upload a PDF file and input data for validation. The help page offers help to the user if needed.


### Access the API Endpoints using Postman (or another API development tool)

1. Run the Flask Application (as described above)
2. Open Postman:
    * If you haven't already, download and install Postman: https://www.postman.com/downloads/.
    * Open Postman.
3. Upload a PDF File:
    * Select POST as the HTTP method.
    * Enter the URL: http://127.0.0.1:5000/api/upload.
    * In the Body tab, select form-data.
    * Add a key named pdf, set the type to File from the dorop-down menu, and upload a PDF file from your system.
    * Click Send.
    * You should receive a JSON response showing if the upload was successful or not and the relevant data.
4. Validate PDF Content:
    * Select POST as the HTTP method.
    * Enter the URL: http://127.0.0.1:5000/api/validate.
    * In the Body tab, select raw and choose JSON as the format.
    * Enter the JSON payload containing the keyword and value, for example:`  {"keyword": "example_keyword”, “value": "example_value”}  `
    * Click Send.
    * You should receive a JSON response with the validation results.


### Unit Tests
Unit tests are provided to check the text extraction and validation works as expected. 
To run the tests, execute the following command in the directory containing your app.py file:
`pytest`
