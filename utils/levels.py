# -*- coding: utf-8 -*-

import json
from   init.settings import Settings
from   datetime      import date, datetime
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


def get_top_users():

    global all_users
    
    try:

        with open("resources/users.json") as data:
            all_users = json.load(data)

        tops = {}
        for user, values in all_users.items():

            if values["level"] == None or values["exp"] == None:
                continue
        
            tops[user] = [values["level"], values["exp"]]

        tops = list(sorted(tops.items(), key=lambda item: item[1], reverse=True))
        return tops
        
    except Exception as e:
        print(e)
        return []

def get_price(user):
    
    global all_users

    try:
        if all_users == {} or str(user.id) not in all_users:
            with open("resources/users.json") as data:
                all_users = json.load(data)

        if str(user.id) not in all_users:
            return 0

        level = all_users[str(user.id)]["level"]

        if level == None:
            return 5564800000

        return 50000 * level
    except:
        pass


def get_users_birthday():

    global all_users

    liste = []
    try:
        with open("resources/users.json") as data:
            all_users = json.load(data)

        now = datetime.strftime(datetime.now(), "%d-%m-%Y")
        now = datetime.strptime(now, "%d-%m-%Y")
        for user, values in all_users.items():
            try:
                birthdate = datetime.strptime(values["birth_date"], "%d-%m-%Y")
               
                if birthdate.month == now.month and birthdate.day == now.day:
                    age = floor((now - birthdate).total_seconds() / 31536000)
                    liste.append((user, age))
            except:
                continue

        return liste
    except:
        return []