from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
import os
import csv
from wtforms import FileField, SubmitField, StringField
from wtforms.validators import InputRequired
from flasgger import Swagger

from config_app import Config
from pdf_validator import validate_pdf
from highlight_pdf import highlight_pdf, highlight_pdf_from_csv


class UploadPdfFlaskForm(FlaskForm):
    """
    Class to create a FlaskForm for uploading a PDF file
    """
    pdf = FileField("Choose PDF File", validators=[InputRequired()])
    submit = SubmitField("Upload PDF File")


class InputDataFlaskForm(FlaskForm):
    """
    Class to create a FlaskForm for inputting data
    """
    keyword = StringField("Keyword", validators=[InputRequired()])
    value = StringField("Value", validators=[InputRequired()])
    submit = SubmitField("Submit Input")


class UploadCsvFlaskForm(FlaskForm):
    """
    Class to create a FlaskForm for uploading a CSV file
    """
    csv_file = FileField("Choose CSV File", validators=[InputRequired()])
    submit = SubmitField("Upload CSV File")


def create_app():
    """
    Create the Flask app and initialise routes and configurations
    """
    app = Flask(__name__)
    swagger = Swagger(app)
    app.config.from_object(Config)
    Config.initialise_app(app)


    def save_file(file, upload_folder, valid_extension):
        file_name = secure_filename(file.filename)
        if not file_name.endswith(f'.{valid_extension}'):
            raise ValueError(f"File is not a {valid_extension.upper()}")
        # Construct the full path where the file will be saved
        file_path = os.path.join(upload_folder, file_name) 
        file.save(file_path)
        return file_path
    

    @app.route('/', methods=['GET', 'POST'])
    @app.route('/home', methods=['GET', 'POST'])
    def home():
        """
        Home page for the web app
        """
        upload_form = UploadPdfFlaskForm()
        input_form = InputDataFlaskForm()

        # If the user uploads a PDF file
        if upload_form.validate_on_submit():
            try:
                file_path = save_file(upload_form.pdf.data, app.config['UPLOAD_FOLDER'], 'pdf')
                session['file_path'] = file_path
                return redirect(url_for('home', success=True))
            except ValueError:
                return redirect(url_for('home', not_pdf=True))
            except Exception as e:
                return str(e)
        
        # If the user submits a keyword and value
        if input_form.validate_on_submit():
            keyword = input_form.keyword.data
            value = input_form.value.data
            pdf_file_path = session.get('file_path')
            if not pdf_file_path:
                return redirect(url_for('home', no_file=True))
            
            found, price_valid = validate_pdf(pdf_file_path, keyword, value)
            highlight_pdf(pdf_file_path, keyword, value)
            session['found'] = found
            session['price_valid'] = price_valid

            # Redirect to the home page with the appropriate message
            if found and price_valid:
                return redirect(url_for('home', success=True, validated=True, price_valid=True))
            elif found and price_valid is None:
                return redirect(url_for('home', success=True, validated=True))
            elif not found and price_valid is None:
                return redirect(url_for('home', success=True, not_validated=True))
            elif found and price_valid is False:
                return redirect(url_for('home', success=True, validated=True, price_invalid=True))
            elif not found and price_valid:
                return redirect(url_for('home', success=True, not_validated=True, price_valid=True))
            else:
                return redirect(url_for('home', success=True, not_validated=True, price_invalid=True))
        
        pdf_file_path = session.get('file_path') 
        # Return the home page with the appropriate request arguments
        return render_template("index.html", 
                            upload_form=upload_form, 
                            input_form=input_form, 
                            success=request.args.get('success'),
                            data_submitted=request.args.get('data_submitted'),
                            validated=request.args.get('validated'), 
                            not_validated=request.args.get('not_validated'),
                            price_invalid=request.args.get('price_invalid'), 
                            price_valid=request.args.get('price_valid'),
                            not_pdf=request.args.get('not_pdf'),
                            no_file=request.args.get('no_file'),
                            pdf_file_path=pdf_file_path)


    @app.route('/help')
    def help():
        """
        Help page for the web app
        """
        return render_template("help.html")
    

    @app.route('/csv', methods=['GET', 'POST'])
    def csv_file():
        """
        Page to upload a CSV with keywords and values to be validated
        """
        # Clear previous results if they exist at start of the session
        if 'results' in session:
            session.pop('results')
            
        upload_pdf_form = UploadPdfFlaskForm()
        upload_csv_form = UploadCsvFlaskForm()

        if upload_pdf_form.validate_on_submit():
            try:
                pdf_path = save_file(upload_pdf_form.pdf.data, app.config['UPLOAD_FOLDER'], 'pdf')
                session['pdf_path'] = pdf_path
                # Clear previous path if it exists
                if session.get('csv_path'):
                    session.pop('csv_path')
                return redirect(url_for('csv_file', pdf_success=True))
            except ValueError:
                return redirect(url_for('csv_file', not_pdf=True))
            except Exception as e:
                return str(e)
        
        if upload_csv_form.validate_on_submit():
            try:
                csv_file = upload_csv_form.csv_file.data
                csv_path = save_file(csv_file, app.config['UPLOAD_FOLDER'], 'csv')
                session['csv_path'] = csv_path
                if session.get('results'):
                    session.pop('results')
                return redirect(url_for('csv_file', csv_success=True))
            except ValueError:
                return redirect(url_for('csv_file', not_csv=True))
            except Exception as e:
                return str(e)

        
        csv_path = session.get('csv_path')
        pdf_path = session.get('pdf_path')
        if csv_path and pdf_path:
            # Read the CSV file and validate the PDF file
            with open(csv_path, 'r') as csv_file_reader:
                reader = csv.reader(csv_file_reader)
                keyword_value_list = [line for line in reader]
            # Validate the PDF file using the keyword-value pairs    
            pdf_file_path = session.get('pdf_path')
            results = []
            for keyword, value in keyword_value_list:
                found, price_valid = validate_pdf(pdf_file_path, keyword, value)
                results.append((keyword, value, found, price_valid))
            session['results'] = results
            highlight_pdf_from_csv(pdf_file_path, keyword_value_list)

        pdf_file_path = session.get('pdf_path')
        results = session.get('results')
        return render_template("csv_file.html",
                            upload_pdf_form=upload_pdf_form,
                            upload_csv_form=upload_csv_form,
                            results=results,
                            pdf_success=request.args.get('pdf_success'),
                            csv_success=request.args.get('csv_success'),
                            not_pdf=request.args.get('not_pdf'),
                            not_csv=request.args.get('not_csv'),
                            pdf_file_path=pdf_file_path)


    @app.route('/api/upload', methods=['POST'])
    def api_upload():
        """
        Upload a PDF file via an API endpoint
        ---
        consumes:
          - multipart/form-data
        parameters:
          - in: formData
            name: pdf
            type: file
            required: true
            description: The PDF file to upload
        responses:
          200:
            description: File uploaded successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: File uploaded successfully
                file_path:
                  type: string
          400:
            description: No file or invalid file included in the request
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: No file included in the request
          500:
            description: Internal server error
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: An error occurred
        """
        if 'pdf' not in request.files:
            return jsonify({'error': 'No file included in the request'}), 400
        file = request.files['pdf']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        try:
            file_path = save_file(file, app.config['UPLOAD_FOLDER'], 'pdf')
            session['file_path'] = file_path
            return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500


    @app.route('/api/validate', methods=['POST'])
    def api_validate():
        """
        API endpoint which validates the PDF file
        ---
        consumes:
          - application/json
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                keyword:
                  type: string
                value:
                  type: string
        responses:
          200:
            description: Keyword and value found in the PDF
          400:
            description: Keyword and value are required
        """
        data = request.get_json()
        if not data or 'keyword' not in data or 'value' not in data:
            return jsonify({'error': 'Keyword and value are required'}), 400

        keyword = data['keyword']
        value = data['value']
        pdf_file_path = session.get('file_path')

        if not pdf_file_path:
            return jsonify({'error': 'No PDF file uploaded'}), 400

        found, price_valid = validate_pdf(pdf_file_path, keyword, value)
        return jsonify({'found': found, 'price_valid': price_valid}), 200



    @app.route('/api/csv', methods=['POST'])
    def csv_api_upload_and_validate():
        """
        Upload a CSV and PDF file via an API endpoint and validate the PDF content using the CSV file.
        ---
        consumes:
          - multipart/form-data
        parameters:
          - in: formData
            name: csv
            type: file
            required: true
            description: The CSV file containing keyword-value pairs for validation
          - in: formData
            name: pdf
            type: file
            required: true
            description: The PDF file to be validated using the CSV data
        responses:
          200:
            description: Files uploaded and validated successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Files uploaded and validated successfully
                results:
                  type: array
                  items:
                    type: object
                    properties:
                      keyword:
                        type: string
                        example: "example_keyword"
                      value:
                        type: string
                        example: "example_value"
                      found:
                        type: boolean
                        example: true
                      price_valid:
                        type: boolean
                        example: false
          400:
            description: Both CSV and PDF files are required or invalid files
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: Both CSV and PDF files are required
          500:
            description: Internal server error
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: An error occurred
        """
        if 'csv' not in request.files or 'pdf' not in request.files:
            return jsonify({'error': 'Both CSV and PDF files are required'}), 400
        
        csv_file = request.files['csv']
        pdf_file = request.files['pdf']
        if csv_file.filename == '' or pdf_file.filename == '':
            return jsonify({'error': 'Both CSV and PDF files must be selected'}), 400

        try:
            csv_path = save_file(csv_file, app.config['UPLOAD_FOLDER'], 'csv')
            pdf_path = save_file(pdf_file, app.config['UPLOAD_FOLDER'], 'pdf')

            # Read the CSV file and validate keyword-value pairs
            keyword_value_list = []
            with open(csv_path, 'r') as csv_file_reader:
                reader = csv.reader(csv_file_reader)
                keyword_value_list = [line for line in reader]
            results = []
            for keyword, value in keyword_value_list:
                found, price_valid = validate_pdf(pdf_path, keyword, value)
                results.append({
                    'keyword': keyword,
                    'value': value,
                    'found': found,
                    'price_valid': price_valid
                })

            return jsonify({
                'message': 'Files uploaded and validated successfully',
                'results': results
            }), 200 # Success code 200

        except ValueError as e:
            return jsonify({'error': str(e)}), 400 # Error code 400 for bad request
        except Exception as e:
            return jsonify({'error': str(e)}), 500 # Error code 500 for internal server error

    # Return the Flask app from create_app function
    return app 


if __name__ == "__main__":
    # Run the Flask app when the script is executed by user
    create_app().run(debug=True)
