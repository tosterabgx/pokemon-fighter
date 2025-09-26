from flask import Blueprint, flash, redirect, request, session, url_for

from lib.battle import do_battle_all
from lib.db import check_password, create_user, get_all_active_users
from lib.utils import admin_required, get_upload_path, login_required, validate_trainer

api_blueprint = Blueprint("api", __name__)


@api_blueprint.post("/api/login")
def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    user_id = check_password(username, password)

    if user_id == -1:
        flash("Invalid credentials")
        return redirect(url_for("login"))

    session["user_id"] = user_id
    return redirect(url_for("profile"))


@api_blueprint.post("/api/register")
def register():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    user_id = create_user(username, password)

    if user_id == -1:
        flash("User already exists")
        return redirect(url_for("register"))

    session["user_id"] = user_id
    return redirect(url_for("profile"))


@api_blueprint.get("/api/logout")
def logout():
    session.clear()
    return redirect("/")


@api_blueprint.post("/api/upload")
@login_required
def upload():
    if "file" not in request.files:
        flash("No file selected")
        return redirect(url_for("profile"))

    file = request.files["file"]

    if not file or file.filename == "":
        flash("No file selected")
        return redirect(url_for("profile"))

    result = validate_trainer(file.read())

    if isinstance(result, str):
        flash(result)
        return redirect(url_for("profile"))

    file.seek(0)
    file.save(get_upload_path(f"{session['user_id']}.py"))

    return redirect(url_for("profile"))


@api_blueprint.post("/api/battle_all")
@admin_required
def battle_all():
    usernames, results = do_battle_all(get_all_active_users())

    if usernames:
        summary = ", ".join(
            f"{u}: {len(results[u]['won'])}W/{len(results[u]['lost'])}L"
            for u in sorted(usernames)
        )
    else:
        summary = "no trainers found"

    flash(f"Tournament complete: {summary}")

    return redirect(url_for("profile"))
