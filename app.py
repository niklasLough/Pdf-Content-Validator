from flask import Flask, render_template, redirect, url_for, request
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


def app():
    """
    Function to create the Flask app
    
    Returns:
    app: Flask
    """

    # Create the Flask app
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.initialise_app(app)

    @app.route('/', methods=['GET', 'POST'])
    @app.route('/home', methods=['GET', 'POST'])

    # Function to render the home page
    def home():
        upload_form = UploadFileFlaskForm()

        if upload_form.validate_on_submit():
            pdf = upload_form.pdf.data
            file_name = secure_filename(pdf.filename) # Secure the filename to be then saved
            
            try:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                pdf.save(file_path) # Save the PDF file to the upload folder

                text = validate_pdf(file_path)

                return redirect(url_for('home', success=True)) # Redirect to the home route
            except Exception as e:
                return redirect(url_for('home', error=True))
        
        return render_template("index.html", upload_form=upload_form, success=request.args.get('success'), error=request.args.get('error'))

    app.run(debug=True)

if __name__ == "__main__":
    app()
