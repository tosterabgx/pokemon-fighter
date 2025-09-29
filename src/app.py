import os

from dotenv import load_dotenv
from flask import Flask, render_template, session

from api import api_blueprint
from lib.config import NUMBER_OF_ROUNDS
from lib.db import get_admin_status, get_all_results_with_usernames
from lib.utils import login_required

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("secret_key")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.jinja_env.auto_reload = True

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
    return render_template(
        "profile.html", is_admin=get_admin_status(session["user_id"])
    )


@app.route("/table/")
def table():
    results, usernames = get_all_results_with_usernames()

    return render_template(
        "table.html",
        usernames=usernames,
        results=results,
        default_value=[NUMBER_OF_ROUNDS] * 2,
    )
