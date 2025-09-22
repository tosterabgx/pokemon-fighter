import json
import os

from lib.config import DATABASE_FILE


def _load():
    if not os.path.exists(DATABASE_FILE):
        return {"users": dict()}

    with open(os.path.join("..", DATABASE_FILE), "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data):
    with open(os.path.join("..", DATABASE_FILE), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def create_user(username: str, password_hash: str):
    db = _load()
    if username in db["users"].keys():
        return

    db["users"][username] = password_hash
    _save(db)


def get_password(username: str):
    db = _load()
    return db["users"].get(username, "\x00")
