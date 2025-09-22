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

    db["users"][username] = generate_password_hash(password)
    _save(db)
    return True


def check_password(username: str, password: str):
    db = _load()

    if username not in db["users"].keys():
        return False

    return check_password_hash(db["users"][username], password)
