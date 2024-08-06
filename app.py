from flask import Flask, render_template, redirect, url_for, request, session
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

from config_app import Config
from pdf_validator import validate_pdf


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


# class UploadCsvFlaskForm(FlaskForm):
#     """
#     Class to create a FlaskForm for uploading a CSV file
#     """
#     csv = FileField("Choose CSV File")
#     submit = SubmitField("Upload CSV File")


def create_app():
    """
    Function to create the Flask app
    
    Returns:
    app: Flask
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.initialise_app(app)


    def file_upload(upload_form):
        pdf = upload_form.pdf.data
        file_name = secure_filename(pdf.filename)
        if not file_name.endswith('.pdf'):
            return redirect(url_for('home', not_pdf=True))
        try:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            pdf.save(file_path)

            # Save the file path in a session to use across different requests
            session['file_path'] = file_path

            return redirect(url_for('home', success=True))
        except Exception as e:
            return str(e)


    def handle_pdf_input(input_form):
        keyword = input_form.keyword.data
        value = input_form.value.data

        pdf_file_path = session.get('file_path')
        found = False
        found, price_valid = validate_pdf(pdf_file_path, keyword, value)

        session['found'] = found
        session['price_valid'] = price_valid
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
        

    # def handle_csv_input(csv_form):
    #     csv = csv_form.csv.data

    # Render the home page
    @app.route('/', methods=['GET', 'POST'])
    @app.route('/home', methods=['GET', 'POST'])
    def home():
        upload_form = UploadPdfFlaskForm()
        input_form = InputDataFlaskForm()
        # csv_form = UploadCsvFlaskForm()

        # If a file has been uploaded
        if upload_form.validate_on_submit():
            return file_upload(upload_form)
        
        # If input data is submitted
        if input_form.validate_on_submit():
            return handle_pdf_input(input_form)
        
        # if csv_form.validate_on_submit():
        #     return handle_csv_input(csv_form)
        
        pdf_file_path = session.get('file_path')
        return render_template("index.html", 
                            upload_form=upload_form, 
                            input_form=input_form, 
                            # csv_form=csv_form,
                            success=request.args.get('success'),
                            data_submitted=request.args.get('data_submitted'),
                            validated=request.args.get('validated'), 
                            not_validated=request.args.get('not_validated'),
                            price_invalid=request.args.get('price_invalid'), 
                            price_valid=request.args.get('price_valid'),
                            not_pdf=request.args.get('not_pdf'),
                            # csv_form_submitted=request.args.get('csv_form_submitted'), # CSV
                            pdf_file_path=pdf_file_path)

    # Render the help page
    @app.route('/help')
    def help():
        return render_template("help.html")

    # Run the app
    app.run(debug=True)
    return app


if __name__ == "__main__":
    create_app()