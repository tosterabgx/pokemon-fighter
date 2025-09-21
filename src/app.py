import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request

from lib.utils import allowed_file, get_upload_path

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("secret_key")


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
            file.save(get_upload_path(file.filename))
            return redirect(request.url)

    return render_template("index.html")


@app.route("/table/")
def table():
    return render_template("table.html", users={})
