# import os
# import pytest
# import io
# from app import create_app

# @pytest.fixture
# def app():
#     app = create_app()
#     app.config.from_object('config_app.TestConfig')
#     with app.app_context():
#         yield app

# @pytest.fixture
# def client(app):
#     return app.test_client()

# def test_api_upload(client):
#     # Prepare the file to upload
#     data = {
#         'pdf': (io.BytesIO(b'%PDF-1.4\n...'), 'test.pdf')  # Replace with valid PDF content
#     }

#     # Perform the API request
#     response = client.post('/api/upload', content_type='multipart/form-data', data=data)
    
#     # Assert the response
#     assert response.status_code == 200
#     assert b'File uploaded successfully' in response.data

# def test_api_validate(client):
#     # First, upload a PDF file
#     data = {
#         'pdf': (io.BytesIO(b'%PDF-1.4\n...'), 'test.pdf')  # Replace with valid PDF content
#     }
#     client.post('/api/upload', content_type='multipart/form-data', data=data)

#     # Now, validate the PDF with keyword and value
#     data = {
#         'keyword': 'example_keyword',
#         'value': 'example_value'
#     }
#     response = client.post('/api/validate', json=data)
    
#     # Assert the response
#     assert response.status_code == 200
#     response_json = response.get_json()
#     assert 'found' in response_json
#     assert 'price_valid' in response_json

# def test_csv_api_upload_and_validate(client):
#     # Prepare the files to upload
#     pdf_data = {
#         'pdf': (io.BytesIO(b'%PDF-1.4\n...'), 'test.pdf')  # Replace with valid PDF content
#     }
#     csv_data = {
#         'csv': (io.BytesIO(b'keyword,value\nexample_keyword,example_value\n'), 'test.csv')  # Replace with valid CSV content
#     }

#     # Upload the PDF file
#     client.post('/api/upload', content_type='multipart/form-data', data=pdf_data)
    
#     # Upload the CSV file and validate
#     response = client.post('/api/csv', content_type='multipart/form-data', data={**pdf_data, **csv_data})
    
#     # Assert the response
#     assert response.status_code == 200
#     response_json = response.get_json()
#     assert 'message' in response_json
#     assert 'results' in response_json
