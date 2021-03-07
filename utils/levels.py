# -*- coding: utf-8 -*-

from io import SEEK_CUR
import discord
import json
from   discord.ext   import commands
from   init.settings import Settings


setting = Settings()
all_users = {}

def update_users(remove, *users):
    try:

        global all_users

        with open("resources/users.json") as data:
            users_dict = json.load(data)

        for user in users:
            if remove:
                users_dict.pop(str(user.id))

            elif str(user.id) not in users_dict:

                users_dict[str(user.id)] = {
                    "level" : 1,
                    "exp" : 0,
                    "warns" : 0,
                    "birth_date" : "NaN"
                }

        all_users = users_dict

        with open("resources/users.json", "w") as file:
            json.dump(users_dict, file ,indent=4)

    except:
        pass


def set_exp(user, exp):

    for role in user.roles:
        if role in setting.ignored_roles_levels or role.is_integration() or role.is_bot_managed():
            return

    global all_users

    try:
        if all_users == {} or str(user.id) not in all_users:
            with open("resources/users.json") as data:
                all_users = json.load(data)

        if str(user.id) not in all_users:
            all_users[str(user.id)] = {
                "level" : 1,
                "exp" : 0,
                "warns" : 0,
                "birth_date" : "NaN"
            }

        else:
            all_users[str(user.id)]["exp"] += exp

            with open("resources/users.json", "w") as file:
                json.dump(all_users, file ,indent=4)

    except:
        pass


def level_up(user):

    for role in user.roles:
        if role in setting.ignored_roles_levels or role.is_integration() or role.is_bot_managed():
            return False, -1

    global all_users

    try:
        if all_users == {} or str(user.id) not in all_users:
            with open("resources/users.json") as data:
                all_users = json.load(data)


        if str(user.id) not in all_users:
            return False

        id = str(user.id)
        user = all_users[id]

        level = user["level"]
        exp = user["exp"]

        max_exp = 50 * level ** 2 - 50 * level + 200

        if exp > max_exp:
            user["level"] += 1
            user["exp"] = 0
            all_users[id] = user

            # TODO set level role ...
            with open("resources/users.json", "w") as file:
                json.dump(all_users, file ,indent=4)

            return True, user["level"]

        return False,  user["level"]

    except:
        return False, -1