import os

from dotenv import load_dotenv
from flask import Flask, render_template, session

from api import api_blueprint
from lib.db import get_admin_status, get_all_active_users
from lib.utils import login_required

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("secret_key")

app.register_blueprint(api_blueprint)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/login/")
def login():
    return render_template("login.html")


@app.get("/register/")
def register():
    return render_template("register.html")


@app.get("/profile/")
@login_required
def profile():
    return render_template("profile.html", is_admin=get_admin_status(session["user"]))


@app.route("/table/")
def table():
    return render_template("table.html", users=get_all_active_users().items())
