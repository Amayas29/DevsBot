from .database import execute, field, record


def add_user(user_id, guild_id):
    execute("INSERT INTO Users (UserID, ServerID) Values (?, ?)", user_id, guild_id)


def remove_user(user_id, guild_id):
    execute("DELETE FROM Users WHERE UserID = ? AND ServerID = ?", user_id, guild_id)


def add_warn(user_id, guild_id):
    execute("UPDATE Users SET Warns = Warns + 1 WHERE UserID = ? AND ServerID = ?",
            user_id, guild_id)


def get_warns(user_id, guild_id):
    return field("SELECT Warns FROM Users WHERE UserID = ? AND ServerID = ?", user_id, guild_id)


def get_level_exp(user_id, guild_id):
    return record("SELECT UserLevel, UserXP FROM Users WHERE UserID = ? AND ServerID = ?", user_id, guild_id)


def get_birth_date(user_id, guild_id):
    return field("SELECT BirthDay FROM Users WHERE UserID = ? AND ServerID = ?", user_id, guild_id)
