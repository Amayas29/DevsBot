from .database import execute, field, record, records
from datetime import datetime
from dateutil.relativedelta import relativedelta


def add_user(user_id, guild_id):
    try:
        user_id = int(user_id)
        guild_id = int(guild_id)
    except:
        return

    execute("INSERT OR IGNORE INTO Users (UserID, ServerID) Values (?, ?)",
            user_id, guild_id)


def remove_user(user_id, guild_id):
    try:
        user_id = int(user_id)
        guild_id = int(guild_id)
    except:
        return

    execute("DELETE FROM Users WHERE UserID = ? AND ServerID = ?", user_id, guild_id)


def add_warn(user_id, guild_id):
    try:
        user_id = int(user_id)
        guild_id = int(guild_id)
    except:
        return

    execute("UPDATE Users SET Warns = Warns + 1 WHERE UserID = ? AND ServerID = ?",
            user_id, guild_id)


def get_warns(user_id, guild_id):
    try:
        user_id = int(user_id)
        guild_id = int(guild_id)
    except:
        return

    return field("SELECT Warns FROM Users WHERE UserID = ? AND ServerID = ?", user_id, guild_id)


def get_level_exp(user_id, guild_id):
    try:
        user_id = int(user_id)
        guild_id = int(guild_id)
    except:
        return

    return record("SELECT UserLevel, UserXP FROM Users WHERE UserID = ? AND ServerID = ?", user_id, guild_id)


def set_exp(user_id, guild_id, new_exp):
    try:
        user_id = int(user_id)
        guild_id = int(guild_id)
        new_exp = int(new_exp)
    except:
        return

    if new_exp < 0:
        new_exp = 0

    execute("UPDATE Users SET UserXP = ? WHERE UserID = ? AND ServerID = ?",
            new_exp, user_id, guild_id)


def set_level(user_id, guild_id, new_level):
    try:
        user_id = int(user_id)
        guild_id = int(guild_id)
        new_level = int(new_level)
    except:
        return

    execute("UPDATE Users SET UserLevel = ? WHERE UserID = ? AND ServerID = ?",
            new_level, user_id, guild_id)


def set_birth_date(user_id, guild_id, birthdate):
    try:
        user_id = int(user_id)
        guild_id = int(guild_id)
        datetime.strptime(birthdate, "%d-%m-%Y")
    except:
        return

    execute("UPDATE Users SET BirthDate = ? WHERE UserID = ? AND ServerID = ?",
            birthdate, user_id, guild_id)


def get_birth_date(user_id, guild_id):
    try:
        user_id = int(user_id)
        guild_id = int(guild_id)
    except:
        return

    return field("SELECT BirthDate FROM Users WHERE UserID = ? AND ServerID = ?", user_id, guild_id)


def remove_users_guild(guild_id):
    try:
        guild_id = int(guild_id)
    except:
        return

    execute("DELETE FROM Users WHERE ServerID = ?", guild_id)


def get_exp_level_guild(guild_id):
    try:
        guild_id = int(guild_id)
    except:
        return

    return records("SELECT UserID, UserLevel, UserXP FROM Users WHERE ServerID = ?", guild_id)


def get_old_message(user_id, guild_id):
    try:
        user_id = int(user_id)
        guild_id = int(guild_id)
    except:
        return

    old_message = field(
        "SELECT OldMessage FROM Users WHERE UserID = ? AND ServerID = ?", user_id, guild_id)

    if old_message is not None:
        old_message = datetime.strptime(old_message, "%d-%m-%Y %H:%M:%S")

    return old_message


def set_old_message(user_id, guild_id, old_message):
    try:
        user_id = int(user_id)
        guild_id = int(guild_id)
    except:
        return

    if type(old_message) != datetime:
        return

    old_message = old_message.strftime("%d-%m-%Y %H:%M:%S")
    execute("UPDATE Users SET OldMessage = ? WHERE UserID = ? AND ServerID = ?",
            old_message, user_id, guild_id)


def get_users_birthdate(guild_id):
    try:
        guild_id = int(guild_id)
    except:
        return

    now = datetime.now()
    now_day_month = now.strftime("%d-%m")

    users = records(
        "SELECT UserID, BirthDate FROM Users WHERE ServerID = ?", guild_id)

    users_birthdate = []

    for user in users:
        if user[1] is None:
            continue

        birthdate = datetime.strptime(user[1], "%d-%m-%Y")
        day_month = birthdate.strftime("%d-%m")

        if day_month == now_day_month:
            users_birthdate.append(
                (user[0], relativedelta(now, birthdate).years))

    return users_birthdate
