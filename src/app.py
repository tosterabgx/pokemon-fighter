import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request
from werkzeug.utils import secure_filename

from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER

load_dotenv()

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = os.getenv("secret_key")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file selected")
            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            flash("No file selected")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename("name.py")
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return redirect(request.url)

    return render_template("index.html")


@app.route("/table/")
def table():
    return render_template("table.html", users={})
