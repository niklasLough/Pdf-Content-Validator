from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os 
from wtforms.validators import InputRequired

# Function to upload a PDF file
def upload_pdf():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['UPLOAD_FOLDER'] = os.path.join('static', 'Files')

    # Ensure the upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    class UploadFileFlaskForm(FlaskForm):
        pdf = FileField("Choose File", validators=[InputRequired()])
        submit = SubmitField("Upload File")

    @app.route('/', methods=['GET', 'POST'])
    @app.route('/home', methods=['GET', 'POST'])
    def home():
        form = UploadFileFlaskForm()
        if form.validate_on_submit():
            pdf = form.pdf.data
            file_name = secure_filename(pdf.filename) # Secure the filename to be then saved
            try:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                pdf.save(file_path) # Save the file
                return redirect(url_for('home', success=True)) # Redirect to the home route
            except Exception as e:
                return str(e)
        return render_template("index.html", form=form, success=request.args.get('success'))

    app.run(debug=True)

if __name__ == "__main__":
    upload_pdf()
