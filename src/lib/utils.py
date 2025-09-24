import os
from functools import wraps

from flask import redirect, session, url_for
from werkzeug.utils import secure_filename

from lib.config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from lib.db import get_admin_status


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_upload_path(filename):
    filename = secure_filename(filename)
    return os.path.join(UPLOAD_FOLDER, filename)


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not get_admin_status(session.get("user", "")):
            return redirect(url_for("profile"))

        return f(*args, **kwargs)

    return wrapper
