import os

class Config:
    """
    Class to store the configuration of the Flask app
    """
    SECRET_KEY = 'shhhhh'
    UPLOAD_FOLDER = os.path.join('static', 'Files')

    @staticmethod
    def initialise_app(app):
        # Ensure the upload folder exists
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])