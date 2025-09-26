import os
import sqlite3

from flask import g
from werkzeug.security import check_password_hash, generate_password_hash

from lib.config import DATABASE_FILE, UPLOAD_FOLDER


def _get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_FILE)
    return db


def create_user(username: str, password: str):
    cur = _get_db().cursor()
    cur.execute("SELECT id FROM users WHERE username = ?", (username,))

    if len(cur.fetchall()) != 0:
        cur.close()
        return -1

    cur.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, generate_password_hash(password)),
    )

    _get_db().commit()

    cur.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_id = cur.fetchall()[0][0]
    cur.close()

    return user_id


def check_password(username: str, password: str):
    cur = _get_db().cursor()
    cur.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    data = cur.fetchall()
    cur.close()

    if len(data) == 0 or not check_password_hash(data[0][1], password):
        return -1

    return data[0][0]


def get_all_active_users():
    cur = _get_db().cursor()
    cur.execute("SELECT id, username FROM users ORDER BY id ASC")
    users = cur.fetchall()
    cur.close()

    active_users = list()

    for id, username in users:
        if os.path.exists(os.path.join(UPLOAD_FOLDER, f"{id}.py")):
            active_users.append((id, username))

    return active_users


def get_admin_status(id: str):
    cur = _get_db().cursor()
    cur.execute("SELECT is_admin FROM users WHERE id = ?", (id,))
    admin_data = cur.fetchall()
    cur.close()

    if len(admin_data) == 0 or admin_data[0][0] == 0:
        return False

    return True
