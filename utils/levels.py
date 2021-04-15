# -*- coding: utf-8 -*-
from database.users import *
from math import floor
from datetime import datetime

COOLDOWN = 1
DEFAULT_INCREMENT = 5


def update_user(user_id, guild_id, increment=None):
    old_message = get_old_message(user_id, guild_id)

    now = datetime.now()

    diff = float("inf")
    if old_message is not None:
        diff = floor(((now - old_message).total_seconds() / 60))

    set_old_message(user_id, guild_id, now)

    if diff <= COOLDOWN:
        return False

    level, exp = get_level_exp(user_id, guild_id)

    if level == -1:
        return False

    exp += increment if increment is not None else DEFAULT_INCREMENT

    max_exp = 50 * level**2 - 50 * level + 200

    if exp > max_exp:
        set_level(user_id, guild_id, level + 1)
        set_exp(user_id, guild_id, 0)
        return True

    set_exp(user_id, guild_id, exp)
    return False
