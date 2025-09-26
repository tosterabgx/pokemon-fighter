import os
from functools import wraps

from flask import redirect, session, url_for
from werkzeug.utils import secure_filename

from lib.base import Pokemon, Trainer
from lib.config import EXEC_BLACKLIST, UPLOAD_FOLDER
from lib.db import get_admin_status


def get_trainer(id):
    sandbox = {"Trainer": Trainer, "Pokemon": Pokemon}
    with open(get_upload_path(f"{id}.py")) as f:
        code = f.read()

    exec(code, locals=sandbox)

    return sandbox["SmartTrainer"]()


def validate_trainer(code) -> str | Trainer:
    try:
        code_string = str(code)
    except:
        return "File has unreadable bytes"

    safe_builtins = dict(__builtins__)

    for word in EXEC_BLACKLIST:
        safe_builtins.pop(word, None)

        if f"{word} " in code_string or f"{word}(" in code_string.replace(" ", ""):
            return f"Forbidden command"

    sandbox = {"Trainer": Trainer, "Pokemon": Pokemon}

    try:
        exec(code, {"__builtins__": safe_builtins}, sandbox)
    except Exception as e:
        return "Failed to run code"

    if "SmartTrainer" not in sandbox:
        return "Class SmartTrainer is not found"

    try:
        exec(
            "t = SmartTrainer()\nt.add(Pokemon('test1'))\nt.box = []\nt.add(Pokemon('test2'))\nt.add(Pokemon('test3'))\nassert len(t.best_team(2)) == 2\nassert len(t.box) == 0",
            safe_builtins,
            sandbox,
        )
    except AssertionError:
        return "Cheating detected"
    except Exception as e:
        return "Class SmartTrainer is lacking functionality"

    return sandbox["SmartTrainer"]


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
