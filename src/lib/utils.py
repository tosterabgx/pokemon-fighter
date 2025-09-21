import os

from werkzeug.utils import secure_filename

from lib.config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_upload_path(filename):
    filename = secure_filename(filename)
    return os.path.join(UPLOAD_FOLDER, filename)
