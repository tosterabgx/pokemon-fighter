import os
from functools import wraps

from flask import redirect, session, url_for
from werkzeug.utils import secure_filename

from lib.base import Pokemon, Trainer
from lib.config import UPLOAD_FOLDER
from lib.db import get_admin_status


def get_trainer_class(code: str):
    sandbox = {"Trainer": Trainer}

    safe_builtins = dict(__builtins__)

    blacklist = {
        "open",
        "input",
        "exec",
        "eval",
        "compile",
        "help",
        "dir",
        "globals",
        "locals",
        "vars",
        "quit",
        "exit",
        "__import__",
    }

    for name in blacklist:
        safe_builtins.pop(name, None)

    try:
        exec(code, {"__builtins__": safe_builtins}, sandbox)
    except Exception as e:
        raise e
        return None

    if "SmartTrainer" not in sandbox:
        return None

    trainer_class = sandbox["SmartTrainer"]

    try:
        trainer = trainer_class()

        trainer.add(Pokemon("test"))

        trainer.best_team(1)[0]
    except Exception as e:
        return None

    return trainer_class


def get_upload_path(filename):
    filename = secure_filename(filename)
    return os.path.join(UPLOAD_FOLDER, filename)


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not get_admin_status(session.get("user_id", "")):
            return redirect(url_for("profile"))

        return f(*args, **kwargs)

    return wrapper
