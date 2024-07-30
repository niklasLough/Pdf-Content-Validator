from flask import Flask, render_template, redirect, url_for, request, session
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

from configApp import Config
from pdfValidator import validate_pdf

class UploadFileFlaskForm(FlaskForm):
    """
    Class to create a FlaskForm for uploading a PDF file
    """
    pdf = FileField("Choose File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

class InputDataFlaskForm(FlaskForm):
    """
    Class to create a FlaskForm for inputting data
    """
    keyword = StringField("Keyword", validators=[InputRequired()])
    value = StringField("Value", validators=[InputRequired()])
    submit = SubmitField("Submit Input")

def create_app():
    """
    Function to create the Flask app
    
    Returns:
    app: Flask
    """

    app = Flask(__name__)
    app.config.from_object(Config)
    Config.initialise_app(app)

    @app.route('/', methods=['GET', 'POST'])
    @app.route('/home', methods=['GET', 'POST'])
    def home():
        upload_form = UploadFileFlaskForm()
        input_form = InputDataFlaskForm()

        # If a file is uploaded
        if upload_form.validate_on_submit():
            pdf = upload_form.pdf.data
            file_name = secure_filename(pdf.filename)
            try:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                pdf.save(file_path)

                # Save the file path in a session to use across different requests
                session['file_path'] = file_path

                return redirect(url_for('home', success=True))
            except Exception as e:
                return str(e)
        
        # If input data is submitted
        if input_form.validate_on_submit():
            # Get the user input
            keyword = input_form.keyword.data
            value = input_form.value.data

            # Get the file path from the session
            pdf_file_path = session.get('file_path')
            validate_pdf(pdf_file_path, keyword, value)
            return redirect(url_for('home', success=request.args.get('success'), data_submitted=True))

        return render_template("index.html", upload_form=upload_form, input_form=input_form, success=request.args.get('success'), data_submitted=request.args.get('data_submitted'))

    @app.route('/help')
    def help():
        return render_template("help.html")

    app.run(debug=True)
    return app

if __name__ == "__main__":
    create_app()
