import os
import sqlite3
from json import dumps, loads

from flask import g
from werkzeug.security import check_password_hash, generate_password_hash

from lib.config import DATABASE_FILE, UPLOAD_FOLDER

database_object = None


def _get_db():
    global database_object
    db = database_object
    if db is None:
        db = database_object = sqlite3.connect(DATABASE_FILE, check_same_thread=False)

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

    for id, _ in users:
        if os.path.exists(os.path.join(UPLOAD_FOLDER, f"{id}.py")):
            active_users.append(id)

    return active_users


def get_admin_status(id: int):
    cur = _get_db().cursor()
    cur.execute("SELECT is_admin FROM users WHERE id = ?", (id,))
    admin_data = cur.fetchall()
    cur.close()

    return not (len(admin_data) == 0 or admin_data[0][0] == 0)


def get_username_by_id(id: int):
    cur = _get_db().cursor()
    cur.execute("SELECT username FROM users WHERE id = ?", (id,))
    data = cur.fetchall()

    if len(data) == 0:
        cur.close()
        return False

    return data[0][0]


def get_competition_result(userId: int) -> tuple[dict, dict]:
    cur = _get_db().cursor()
    cur.execute("SELECT win, lose FROM results WHERE userId = ?", (userId,))
    data = cur.fetchall()
    cur.close()

    if len(data) == 0:
        return dict(), dict()

    win, lose = map(str, data[0])

    try:
        win = loads(win)
    except:
        win = dict()

    try:
        lose = loads(lose)
    except:
        lose = dict()

    return win, lose


def get_all_results_with_usernames():
    cur = _get_db().cursor()
    cur.execute(
        "SELECT userId FROM results ORDER BY LENGTH (win) DESC, LENGTH (lose) ASC"
    )
    data = cur.fetchall()
    cur.close()

    results = dict()
    usernames = dict()

    for userId in data:
        userId = userId[0]

        u = get_username_by_id(userId)

        if u:
            results[userId] = get_competition_result(userId)
            usernames[userId] = u

    return results, usernames


def add_competition_result(userId: int, otherId: int, score: tuple):
    cur = _get_db().cursor()
    cur.execute("SELECT id FROM results WHERE userId = ?", (userId,))

    wins, loses = get_competition_result(userId)

    if score[0] > score[1]:
        wins[otherId] = score

    if score[0] < score[1]:
        loses[otherId] = score

    win_data = dumps(wins)
    lose_data = dumps(loses)

    if len(cur.fetchall()) == 0:
        cur.execute(
            "INSERT INTO results (userId, win, lose) VALUES (?, ?, ?)",
            (userId, win_data, lose_data),
        )
    else:
        cur.execute(
            "UPDATE results SET win = ?, lose = ? WHERE userId = ?",
            (win_data, lose_data, userId),
        )

    _get_db().commit()
    cur.close()


def reset_results():
    cur = _get_db().cursor()

    cur.execute("UPDATE results SET win = '', lose = ''")

    _get_db().commit()
    cur.close()
