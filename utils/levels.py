# -*- coding: utf-8 -*-

from os import EX_CANTCREAT
import discord
import json
from   discord.ext   import commands
from   init.settings import Settings
from   datetime      import datetime
from   math          import floor


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
                    "birth_date" : "NaN",
                    "old_message": None
                }

        all_users = users_dict

        with open("resources/users.json", "w") as file:
            json.dump(users_dict, file ,indent=4)

    except:
        pass


def set_exp(user, exp):

    for role in user.roles:
        if role.id in setting.ignored_roles_levels or role.is_integration() or role.is_bot_managed():
            return

    global all_users

    try:
        if all_users == {} or str(user.id) not in all_users:
            with open("resources/users.json") as data:
                all_users = json.load(data)

        if str(user.id) not in all_users:
            all_users[str(user.id)] = {
                "level" : 1,
                "exp" : exp,
                "warns" : 0,
                "birth_date" : "NaN",
                "old_message" : datetime.now()
            }

        else:
            old_message = all_users[str(user.id)]["old_message"]
            now = datetime.now()

            if old_message == None:
                old_message = now
            else:
                old_message = datetime.strptime(old_message, "%d-%m-%Y %H:%M:%S")

            diff = floor(((now - old_message).total_seconds() / 60))

            if diff >= setting.min_time:
                all_users[str(user.id)]["exp"] += exp

            all_users[str(user.id)]["old_message"] = now.strftime("%d-%m-%Y %H:%M:%S")

        with open("resources/users.json", "w") as file:
            json.dump(all_users, file ,indent=4)

    except Exception as e:
        pass


def level_up(user):

    for role in user.roles:
        if role.id in setting.ignored_roles_levels or role.is_integration() or role.is_bot_managed():
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