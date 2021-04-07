from sqlite3 import connect
from os.path import isfile
import traceback

DB_PATH = "database/database.db"
BUILD_PATH = "database/build.sql"

cnx = connect(DB_PATH, check_same_thread=False)
cur = cnx.cursor()


def with_commit(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        commit()

    return inner


@with_commit
def build():
    if isfile(BUILD_PATH):
        return scriptexec(BUILD_PATH)
    return False


def commit():
    cnx.commit()


def close():
    cnx.close()


def field(command, *values):
    try:
        cur.execute(command, tuple(values))

        if (fetch := cur.fetchone()) is not None:
            return fetch[0]
    except:
        traceback.print_exc()

        return None


def record(command, *values):
    try:
        cur.execute(command, tuple(values))
        return cur.fetchone()
    except:
        traceback.print_exc()
        return None


def records(command, *values):
    try:
        cur.execute(command, tuple(values))
        return cur.fetchall()
    except:
        traceback.print_exc()
        return None


def column(command, *values):
    try:
        cur.execute(command, tuple(values))
        return [item[0] for item in cur.fetchall()]
    except:
        traceback.print_exc()
        return None


@with_commit
def execute(command, *values):
    try:
        cur.execute(command, tuple(values))
    except:
        traceback.print_exc()


def multiexec(command, valueset):
    try:
        cur.executemany(command, valueset)
    except:
        traceback.print_exc()


def scriptexec(path):
    try:
        with open(path, "r", encoding="utf-8") as script:
            cur.executescript(script.read())
            return True
    except:
        traceback.print_exc()
        return False
