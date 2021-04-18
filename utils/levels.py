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

    level, exp = get_level_exp(user_id, guild_id)

    if level == -1:
        return 0

    increment = increment if increment is not None else DEFAULT_INCREMENT

    if increment < 0:
        exp += increment
        set_exp(user_id, guild_id, exp)

        if exp < 0:
            if level <= 1:
                return 0

            set_level(user_id, guild_id, level - 1)
            set_exp(user_id, guild_id, 0)
            return -1

        return 0

    if diff <= COOLDOWN:
        return 0

    max_exp = 50 * level**2 - 50 * level + 200
    exp += increment

    if exp > max_exp:
        set_level(user_id, guild_id, level + 1)
        set_exp(user_id, guild_id, 0)
        return 1

    set_exp(user_id, guild_id, exp)
    return 0
