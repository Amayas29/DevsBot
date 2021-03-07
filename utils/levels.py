# -*- coding: utf-8 -*-

import discord
import json
from   discord.ext   import commands
from   init.settings import Settings


def update_users(remove, *users):
    try:

        with open("resources/users.json") as data:
            users_dict : dict = json.load(data)

        for user in users:
            if remove:
                users_dict.pop(str(user.id))

            elif str(user.id) not in users_dict:

                users_dict[str(user.id)] = {
                    "level" : 0,
                    "exp" : 0,
                    "warns" : 0,
                    "birth_date" : "NaN"
                }

        with open("resources/users.json", "w") as file:
            json.dump(users_dict, file ,indent=4)

    except:
        pass