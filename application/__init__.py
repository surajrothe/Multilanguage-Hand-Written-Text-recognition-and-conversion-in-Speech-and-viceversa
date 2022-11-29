from flask import Flask
from flask_dropzone import Dropzone
from flask_session import Session
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '374b042381a0a4bc9d7f6f64eab0b0d723d57a12145663f6cbe943847699'

# Sessions
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)  


dir_path = os.path.dirname(os.path.realpath(__file__))

app.config.update(
        UPLOADED_PATH = os.path.join(dir_path, "static/uploaded_files/"),
        DROPZONE_ALLOWED_FILE_TYPE = "image",
        DROPZONE_MAX_FILE_SIZE = 3,
        DROPZONE_MAX_FILES = 1,
        AUDIO_FILE_UPLOAD = os.path.join(dir_path, 'static/audio_files/')


)

app.config['DROPZONE_REDIRECT_VIEW'] = 'decoded'
dropzone = Dropzone(app)

from application import routes
