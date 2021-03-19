from sqlite3 import connect
from os.path import isfile

DB_PATH = "database/db.db"
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
        scriptexec(BUILD_PATH)


def commit():
    cnx.commit()


def close():
    cnx.close()


def field(command, *values):
    cur.execute(command, tuple(values))

    if (fetch := cur.fetchone()) is not None:
        return fetch[0]


def record(command, *values):
    cur.execute(command, tuple(values))
    return cur.fetchone()


def records(command, *values):
    cur.execute(command, tuple(values))
    return cur.fetchall()


def column(command, *values):
    cur.execute(command, tuple(values))
    return [item[0] for item in cur.fetchall()]


@with_commit
def execute(command, *values):
    cur.execute(command, tuple(values))


def multiexec(command, valueset):
    cur.executemany(command, valueset)


def scriptexec(path):
    with open(path, "r", encoding="utf-8") as script:
        cur.executescript(script.read())


build()
execute("DELETE FROM RANK")
print(records("SELECT * FROM RANK"))
close()