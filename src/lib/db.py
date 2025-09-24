import json
import os

from werkzeug.security import check_password_hash, generate_password_hash

from lib.config import DATABASE_FILE


def _load():
    if not os.path.exists(DATABASE_FILE):
        return {"users": dict()}

    with open(DATABASE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data):
    with open(DATABASE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def create_user(username: str, password: str):
    db = _load()
    if username in db["users"].keys():
        return False

    db["users"][username] = {
        "password": generate_password_hash(password),
        "won": [],
        "lost": [],
        "is_admin": False,
        "has_uploaded_trainer": False,
    }
    _save(db)
    return True


def check_password(username: str, password: str):
    db = _load()

    if username not in db["users"].keys():
        return False

    return check_password_hash(db["users"][username]["password"], password)


def get_all_active_users():
    db = _load()

    return dict(
        (username, data)
        for username, data in db["users"].items()
        if data["has_uploaded_trainer"]
    )


def get_admin_status(username: str):
    db = _load()

    if username not in db["users"].keys():
        return False

    return db["users"][username]["is_admin"]


def update_trainer_status(username: str):
    db = _load()

    if username not in db["users"].keys():
        return False

    db["users"][username]["has_uploaded_trainer"] = True
    _save(db)
    return True


def add_won(username: str, id: int):
    db = _load()

    if username not in db["users"].keys():
        return False

    db["users"][username]["won"].append(id)

    _save(db)
    return True


def add_lost(username: str, id: int):
    db = _load()

    if username not in db["users"].keys():
        return False

    db["users"][username]["lost"].append(id)

    _save(db)
    return True
