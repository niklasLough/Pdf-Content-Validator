from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
import os
from wtforms import FileField, SubmitField, StringField
from wtforms.validators import InputRequired

from config_app import Config
from pdf_validator import validate_pdf
from highlight_pdf import highlight_pdf


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

def create_app():
    """
    Create the Flask app with the necessary routes and configurations
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.initialise_app(app)

    def save_pdf_file(pdf, upload_folder):
        """
        Save the uploaded PDF file to the upload folder
        
        Args:
        pdf: FileStorage: The uploaded PDF file
        upload_folder: str: The path to the upload folder
        """
        file_name = secure_filename(pdf.filename)
        if not file_name.endswith('.pdf'):
            raise ValueError("File is not a PDF")
        file_path = os.path.join(upload_folder, file_name)
        pdf.save(file_path)
        return file_path

    def handle_pdf_upload(upload_form, redirect_endpoint):
        """
        Handle the PDF upload process
        
        Args:
        upload_form: FlaskForm: The form for uploading PDF files
        redirect_endpoint: str: The endpoint to redirect after upload
        
        Returns:
        Response: The redirection response or None
        """
        if upload_form.validate_on_submit():
            try:
                file_path = save_pdf_file(upload_form.pdf.data, app.config['UPLOAD_FOLDER'])
                session['file_path'] = file_path
                return redirect(url_for(redirect_endpoint, success=True))
            except ValueError:
                return redirect(url_for(redirect_endpoint, not_pdf=True))
            except Exception as e:
                return str(e)
        return None

    @app.route('/', methods=['GET', 'POST'])
    @app.route('/home', methods=['GET', 'POST'])
    def home():
        """
        Home page for the web app
        """
        upload_form = UploadPdfFlaskForm()
        input_form = InputDataFlaskForm()

        upload_response = handle_pdf_upload(upload_form, 'home')
        if upload_response:
            return upload_response

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
            return redirect(url_for('home', success=True, validated=found, price_valid=price_valid))

        pdf_file_path = session.get('file_path')
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
    def csv():
        """
        Page to upload a CSV with keywords and values to be validated
        """
        upload_form = UploadPdfFlaskForm()

        upload_response = handle_pdf_upload(upload_form, 'csv')
        if upload_response:
            return upload_response

        return render_template("csv.html",
                            upload_form=upload_form,
                            success=request.args.get('success'),
                            not_pdf=request.args.get('not_pdf'))


    @app.route('/api/upload', methods=['POST'])
    def api_upload():
        """
        Upload a PDF file via an API endpoint

        Returns:
        Appropriate JSON responses for successes and errors
        """
        if 'pdf' not in request.files:
            return jsonify({'error': 'No file included in the request'}), 400 #Error code 400 for bad request
        file = request.files['pdf']
        if file.filename == '': #Checking for an empty filename
            return jsonify({'error': 'No selected file'}), 400
        try:
            file_path = save_pdf_file(file, app.config['UPLOAD_FOLDER'])
            session['file_path'] = file_path
            return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200 # Success code 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500 #Error code 500 for internal server error


    @app.route('/api/validate', methods=['POST'])
    def api_validate():
        """
        API endpoint which validates the PDF file

        Returns:
        Appropriate JSON responses for successes and errors
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

    return app


if __name__ == "__main__":
    # Run the Flask app when the script is executed
    create_app().run(debug=True)
