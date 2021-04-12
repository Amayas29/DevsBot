from .database import execute, field, record


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


def get_birth_date(user_id, guild_id):
    try:
        user_id = int(user_id)
        guild_id = int(guild_id)
    except:
        return

    return field("SELECT BirthDay FROM Users WHERE UserID = ? AND ServerID = ?", user_id, guild_id)
