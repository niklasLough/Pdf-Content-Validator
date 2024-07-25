# File to import a PDF file from the user
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField

# def upload_pdf():
#     filename = "ResConfirmFr1.pdf"
#     # Upload a PDF file
#     print("Upload a PDF file")
#     # Functionality
#     return filename

class UploadFileFlaskForm(FlaskForm):
    pdf = FileField("Choose File")
    submit = SubmitField("Upload File")

def upload_pdf():
    app = Flask(__name__)
    @app.route('/', methods=['GET', 'POST'])
    @app.route('/home', methods=['GET', 'POST'])

    def home():
        form = UploadFileFlaskForm()
        return render_template("index.html", form=form)
    
    app.run(debug=True) 

if __name__ == "__main__":
    upload_pdf()