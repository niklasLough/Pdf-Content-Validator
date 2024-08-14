# PDF Content Validator

### Overview
The PDF Content Validator is a Python web application built with Flask. It enables users to upload PDF files, input search data, and validate of those keywords and values appear on the same line within the PDF. It also allows users to upload a CSV file of keyword-value pairs along with a PDF to validate at once. Lastly this app includes additional validation to check if the costs listed by customers match the total price on a contract. Note that this last feature was tailored specifically for PDF documents used by the company where this application was initially developed during an internship.

[![Python Badge](https://img.shields.io/badge/Python-3.6-blue?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)
[![Flask Badge](https://img.shields.io/badge/Flask-2.1.1-blue?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![pytest badge](https://img.shields.io/badge/pytest-white?style=for-the-badge&logo=pytest)](https://docs.pytest.org/en/latest/)


### Features

- **PDF Upload**: Upload a PDF file to the server.
- **Data Input**: Enter a keyword and a value to search and validate in the PDF.
- **Validation**: Checks if the keyword and value are present on the same line within the PDF.
- **Display Results**: Displays validation results and highlights occurrences of keywords and values in the PDF.
- **Help Page**: Provides assistance to users on how to use the application.


### Prerequisites
* Python 3.6 or higher
* Flask
* Flask-WTF
* Werkzeug
* PDFPlumber
* PyMuPDF (Fitz)

### Installation
1. **Clone the Repository**
   * `git clone https://github.com/yourusername/pdf-validator-app.git`

2. **Install the Requirements**
    * `pip install -r requirements.txt`

### Running the Web Application

1. **Run the Flask Application**:
    * Open a terminal.
    * Navigate to the directory containing your app.py file.
    * Run the command: `  python app.py  `
    * The application will start, and you should see output indicating that it is running on http://127.0.0.1:5000.
2. **Open the Web Interface**:
    * Go to http://127.0.0.1:5000 on your preferred web browser
    * You will see the home page where you can upload a PDF file and input data for validation. The help page offers help to the user if needed.


### Access the API Endpoints using Postman (or another API development tool)
If you haven't already, download and install Postman: https://www.postman.com/downloads/ (or another tool).


1. **Upload a PDF File**

   - **Method**: POST
   - **URL**: [http://127.0.0.1:5000/api/upload](http://127.0.0.1:5000/api/upload)
   - **Body**: Form-data
     - Key: `pdf` (Type: File)
   - **Response**: JSON informing of the success or failure of the pdf file upload.

2. **Validate PDF Content**

   - **Method**: POST
   - **URL**: [http://127.0.0.1:5000/api/validate](http://127.0.0.1:5000/api/validate)
   - **Body**: Raw JSON
     - Example:
       ```json
       {
         "keyword": "example_keyword",
         "value": "example_value"
       }
       ```
   - **Response**: JSON with results of the validation.

3. **Validate with Keyword-Value Pairs from CSV**

   - **Method**: POST
   - **URL**: [http://127.0.0.1:5000/api/upload](http://127.0.0.1:5000/api/upload)
   - **Body**: Form-data
     - Key: `pdf` (Type: File)
     - Key: `csv` (Type: File)
   - **Response**: JSON with validation results for each keyword-value pair.

  
If there are issues with the files (for example missing files), you will receive an error message in the JSON response.


### Unit Tests
Unit tests are provided to check the text extraction and validation works as expected. 
To run the tests, execute the following command in the directory containing your app.py file:
`python3 -m pytest`


### Notes
- For some structures in the same line within some PDFs the highlight feature might not work. However the validation feature is still robust and works for all structures.
- Integration tests haven't been made for the API endpoints.
