import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session, url_for

from lib.db import check_password, create_user
from lib.utils import allowed_file, get_upload_path, login_required

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("secret_key")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if check_password(username, password):
            session["user"] = username
            return redirect(url_for("upload"))

        flash("Invalid credentials")
        return redirect(request.url)

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if create_user(username, password):
            session["user"] = username
            return redirect(url_for("upload"))

        flash("User already exists")
        return redirect(request.url)

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
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

    return render_template("upload.html")


@app.route("/table")
def table():
    return render_template("table.html", users={})
