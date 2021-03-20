# -*- coding: utf-8 -*-

import json
import discord
from copy import deepcopy as dp
from database.users import get_warns

cache = {}
footer = {}
messages = {}
PATH = "resources/embeds/"
MESSAGES = "resources/messages.json"


def get_moderation_embed(action, user, moderator, reason, text, icon):

    global cache
    global footer

    try:

        if action not in cache:
            with open(f"{PATH}{action}.json", "r") as f:
                dict_embed = json.load(f)

            cache[action] = dict_embed

        dict_embed = dp(cache[action])

        if type(dict_embed["color"]) != int:
            dict_embed["color"] = int(dict_embed["color"], 16)

        if reason == "" or reason is None:
            reason = "NaN"

        dict_embed["description"] = dict_embed["description"].replace(
            "{user}", user.mention)

        fields = dict_embed["fields"]

        for field in fields:
            field["value"] = field["value"].replace(
                "{moderator}", moderator.mention)
            field["value"] = field["value"].replace("{reason}", reason)

        dict_embed["fields"] = fields

        if footer == {}:
            footer = {"text": text, "icon_url": icon}

        dict_embed["footer"] = footer

        return discord.Embed.from_dict(dict_embed)

    except:
        return None


def get_ban_embed(user, moderator, reason, text, icon):
    return get_moderation_embed("ban", user, moderator, reason, text, icon)


def get_unban_embed(user, moderator, reason, text, icon):
    return get_moderation_embed("unban", user, moderator, reason, text, icon)


def get_warn_embed(user, moderator, reason, text, icon):
    return get_moderation_embed("warn", user, moderator, reason, text, icon)


def get_kick_embed(user, moderator, reason, text, icon):
    return get_moderation_embed("kick", user, moderator, reason, text, icon)

def get_message(message, user, level=None, guild_id=None):

    global messages

    try:
        if messages == {}:
            with open(MESSAGES, "r") as f:
                messages = json.load(f)

        msg = dp(messages[message])
        msg = msg.replace("{user}", user.mention)

        if level is not None:
            msg = msg.replace("{level}", level)

        if guild_id is not None:
            msg = msg.replace("{warns}", str(get_warns(user.id, guild_id)))

        return msg
    except:
        return None

def get_warns_message(user, guild_id):
    return get_message("warns_message", user, guild_id=guild_id)

def get_muted_message(user):
    return get_message("muted_message", user)


def get_unmuted_message(user):
    return get_message("unmuted_message", user)


def get_nickname_message(user):
    return get_message("nickname_message", user)


# def get_rules_embed(dict, rules, server, server_icon, bot_icon):
#     try:
#         dict = dp(dict)

#         dict["author"]["name"] = server
#         dict["author"]["icon_url"] = str(server_icon)

#         if type(dict["color"]) != int:
#             dict["color"] = int(dict["color"], 16)

#         dict["fields"][0]["value"] = rules

#         dict["footer"]["text"] = settings.config["footer"]
#         dict["footer"]["icon_url"] = str(bot_icon)

#         return discord.Embed.from_dict(dict)

#     except:
#         return None


# def get_invite_embed(dict: dict, server, server_icon, link,
#                      bot_icon) -> discord.Embed:
#     try:
#         dict = dp(dict)

#         dict["author"]["name"] = server
#         dict["author"]["url"] = link
#         dict["author"]["icon_url"] = str(server_icon)

#         if type(dict["color"]) != int:
#             dict["color"] = int(dict["color"], 16)

#         dict["description"] = dict["description"].replace("{server}", server)

#         dict["fields"][0]["value"] = link

#         dict["footer"]["text"] = settings.config["footer"]
#         dict["footer"]["icon_url"] = str(bot_icon)

#         return discord.Embed.from_dict(dict)

#     except:
#         return None


# def get_bot_info_embed(dict: dict, description, langages, version,
#                        bot_icon) -> discord.Embed:
#     try:
#         dict = dp(dict)

#         if type(dict["color"]) != int:
#             dict["color"] = int(dict["color"], 16)

#         dict["description"] = dict["description"].replace(
#             "{bot_description}", description)

#         dict["thumbnail"]["url"] = str(bot_icon)

#         fields = dict["fields"]
#         for field in fields:
#             field["value"] = field["value"].replace("{langages}", langages)
#             field["value"] = field["value"].replace("{prefix}",
#                                                     settings.prefix)
#             field["value"] = field["value"].replace("{version}", version)
#         dict["fields"] = fields

#         return discord.Embed.from_dict(dict)

#     except:
#         return None


# def get_welcome_goodbye_embed(dict: dict, user: discord.User, server: str,
#                               member_count: int, bot_icon):

#     try:
#         dict = dp(dict)

#         if type(dict["color"]) != int:
#             dict["color"] = int(dict["color"], 16)

#         dict["description"] = dict["description"].replace(
#             "{user}", user.mention)
#         dict["description"] = dict["description"].replace("{server}", server)

#         fields = dict["fields"]
#         for field in fields:
#             field["value"] = field["value"].replace("{member_count}",
#                                                     str(member_count))

#         dict["footer"]["text"] = settings.config["footer"]
#         dict["footer"]["icon_url"] = str(bot_icon)

#         return discord.Embed.from_dict(dict)

#     except:
#         return None


# def get_server_info_embed(dict: dict, server, description: str,
#                           bot_icon) -> discord.Embed:
#     try:

#         dict = dp(dict)

#         dict["author"]["name"] = server.name
#         dict["author"]["icon_url"] = str(server.icon_url)

#         number_txt_channels = len(server.text_channels)
#         number_voc_channels = len(server.voice_channels)
#         member_count = server.member_count
#         owner = server.owner.name
#         created_at = server.created_at.strftime("%d-%m-%Y")

#         if type(dict["color"]) != int:
#             dict["color"] = int(dict["color"], 16)

#         dict["description"] = dict["description"].replace(
#             "{server}", server.name)
#         dict["description"] = dict["description"].replace(
#             "{description}", description)

#         fields = dict["fields"]
#         for field in fields:
#             field["value"] = field["value"].replace("{member_count}",
#                                                     str(member_count))
#             field["value"] = field["value"].replace("{number_txt_channels}",
#                                                     str(number_txt_channels))
#             field["value"] = field["value"].replace("{number_voc_channels}",
#                                                     str(number_voc_channels))
#             field["value"] = field["value"].replace("{created_at}", created_at)
#             field["value"] = field["value"].replace("{owner}", owner)

#         dict["fields"] = fields

#         dict["footer"]["text"] = settings.config["footer"]
#         dict["footer"]["icon_url"] = str(bot_icon)

#         return discord.Embed.from_dict(dict)

#     except:
#         return None


# def get_user_info_embed(dict, user, user_dict, bot_icon):
#     try:
#         dict = dp(dict)
#         joined = user.joined_at.strftime("%d-%m-%Y")
#         created = user.created_at.strftime("%d-%m-%Y")
#         roles = user.roles

#         roles = roles[::-1]

#         level = None
#         max_role = None
#         for role in roles:
#             if max_role == None and role.id not in settings.ignored_roles_display:
#                 max_role = role
#             if level == None and role.id in settings.ignored_roles_levels:
#                 level = "Max"
#                 exp = "Max"

#         warns = user_dict["warns"]
#         if level == None:
#             level = user_dict["level"]
#             exp = user_dict["exp"]
#         birth_date = user_dict["birth_date"]
#         icon_url = user.avatar_url
#         author = dict["author"]
#         author["name"] = author["name"].replace("{name}", user.name)
#         author["icon_url"] = author["icon_url"].replace(
#             "{icon_url}", str(icon_url))
#         dict["author"] = author

#         if type(dict["color"]) != int:
#             dict["color"] = int(dict["color"], 16)

#         dict["description"] = dict["description"].replace(
#             "{user}", user.mention)

#         fields = dict["fields"]
#         for field in fields:
#             field["value"] = field["value"].replace("{joined}", joined)
#             field["value"] = field["value"].replace("{created}", created)
#             field["value"] = field["value"].replace("{roles}",
#                                                     max_role.mention)
#             field["value"] = field["value"].replace("{warns}", str(warns))
#             field["value"] = field["value"].replace("{level}", str(level))
#             field["value"] = field["value"].replace("{exp}", str(exp))
#             field["value"] = field["value"].replace("{birth_date}",
#                                                     str(birth_date))

#         dict["fields"] = fields
#         dict["footer"]["text"] = settings.config["footer"]
#         dict["footer"]["icon_url"] = str(bot_icon)

#         return discord.Embed.from_dict(dict)

#     except Exception as e:
#         print(e)
#         return None


# async def get_file_welcome(user: discord.User):

#     try:
#         welcome_settings = settings.images_generator["welcome"]

#         asset = user.avatar_url_as(size=welcome_settings["size"])

#         data = BytesIO(await asset.read())
#         im = Image.open(data)

#         im = im.resize((welcome_settings["width"], welcome_settings["height"]))
#         bigsize = (im.size[0] * 3, im.size[1] * 3)
#         mask = Image.new('L', bigsize, 0)
#         draw = ImageDraw.Draw(mask)
#         draw.ellipse((0, 0) + bigsize, fill=255)

#         mask = mask.resize(im.size, Image.ANTIALIAS)
#         im.putalpha(mask)

#         background = Image.open(welcome_settings["path"])
#         background.paste(im, (welcome_settings["x"], welcome_settings["y"]),
#                          im)

#         background.save('__image_generator__.png')

#         return discord.File("__image_generator__.png")

#     except:
#         return None


# def get_level_embed(dict, user, bot_icon):
#     try:
#         dict = dp(dict)

#         with open("resources/users.json") as data:
#             users = json.load(data)

#         user_dict = users[str(user.id)]

#         if type(dict["color"]) != int:
#             dict["color"] = int(dict["color"], 16)

#         dict["description"] = dict["description"].replace(
#             "{user}", user.mention)

#         icon_url = user.avatar_url
#         author = dict["author"]
#         author["name"] = author["name"].replace("{name}", user.name)
#         author["icon_url"] = author["icon_url"].replace(
#             "{icon_url}", str(icon_url))
#         dict["author"] = author

#         level = user_dict["level"]
#         exp = user_dict["exp"]

#         if level == None or exp == None:
#             level = "Max"
#             exp = "Max"
#             max_exp = ""

#         else:
#             max_exp = 50 * level**2 - 50 * level + 200
#             max_exp = " / " + str(max_exp)

#         fields = dict["fields"]
#         for field in fields:
#             field["value"] = field["value"].replace("{level}", str(level))
#             field["value"] = field["value"].replace("{exp}",
#                                                     str(exp) + str(max_exp))

#         dict["fields"] = fields
#         dict["footer"]["text"] = settings.config["footer"]
#         dict["footer"]["icon_url"] = str(bot_icon)

#         return discord.Embed.from_dict(dict)

#     except:
#         return None


# def get_file_rank(user):

#     try:

#         with open("resources/users.json") as data:
#             users = json.load(data)

#         user_info = users[str(user.id)]

#         level = user_info["level"]
#         exp = user_info["exp"]

#         rank = settings.images_generator["rank"]

#         background = Image.open(rank["path"])

#         draw = ImageDraw.Draw(background)

#         max = background.size[0]

#         if exp == None:
#             exp = background.size[0]

#         else:
#             max_exp = 50 * level**2 - 50 * level + 200
#             exp = 100 * (exp / max_exp)

#         exp = max * exp / 100

#         if rank["color"] == []:
#             rank["color"] = ["28, 149, 228"]

#         color = random.choice(rank["color"])
#         color = tuple(map(int, color.split(",")))
#         draw.rectangle(((0, 0), (exp, background.size[1])),
#                        fill=color,
#                        width=background.size[1])

#         background.save("__rank__.png")

#         return discord.File("__rank__.png")

#     except Exception as e:
#         return None


# async def get_top_embed(dict, bot: commands.Bot):
#     try:
#         tops = get_top_users()
#         dict = dp(dict)

#         if type(dict["color"]) != int:
#             dict["color"] = int(dict["color"], 16)

#         field = dict["fields"][0]

#         dict["fields"] = []

#         nb = 0
#         for elem in tops:
#             nb += 1

#             if nb > 10:
#                 break

#             user = await bot.fetch_user(elem[0])
#             new = dp(field)
#             new["name"] = new["name"].replace("{rank}", str(nb))
#             new["name"] = new["name"].replace("{user}", user.name)

#             level = elem[1][0]
#             exp = elem[1][1]

#             max_exp = 50 * level**2 - 50 * level + 200

#             new["value"] = new["value"].replace("{level}", str(level))
#             new["value"] = new["value"].replace(
#                 "{exp}",
#                 str(exp) + " / " + str(max_exp))

#             dict["fields"].append(new)

#         dict["footer"]["text"] = settings.config["footer"]
#         dict["footer"]["icon_url"] = str(bot.user.avatar_url)

#         return discord.Embed.from_dict(dict)
#     except Exception as e:
#         print(e)
#         return None


# def get_poll_embed(dict, user, question, options, bot_icon):
#     try:
#         dict = dp(dict)

#         icon_url = user.avatar_url
#         author = dict["author"]
#         author["name"] = author["name"].replace("{name}", user.name)
#         author["icon_url"] = author["icon_url"].replace(
#             "{icon_url}", str(icon_url))
#         dict["author"] = author

#         if type(dict["color"]) != int:
#             dict["color"] = int(dict["color"], 16)

#         dict["description"] = dict["description"].replace(
#             "{question}", question)

#         dict["fields"][0]["value"] = options

#         dict["footer"]["text"] = settings.config["footer"]
#         dict["footer"]["icon_url"] = str(bot_icon)

#         return discord.Embed.from_dict(dict)

#     except Exception as e:
#         print(e)
#         return None


# def get_help_all_embed(dict, bot):

#     try:

#         dict = dp(dict)

#         dict["description"] = dict["description"].replace(
#             "{bot_name}", settings.config["name"])

#         if type(dict["color"]) != int:
#             dict["color"] = int(dict["color"], 16)

#         field = dict["fields"][0]

#         dict["fields"] = []

#         cogs = [c for c in bot.cogs.keys()]
#         cogs.remove("Events")

#         for cog in cogs:

#             cogbot = bot.get_cog(cog)
#             list_commands = f"\n*Description générale : {cogbot.description}*\n\n"

#             for cmd in cogbot.walk_commands():

#                 if cmd.hidden or cmd.parent != None:
#                     continue

#                 list_commands += f"**{cmd.name}** - *{cmd.description}* \n"

#             if cog != cogs[-1]:
#                 list_commands += "\n  \n**   **\n"

#             cog_name = cog
#             new = dp(field)
#             new["name"] = new["name"].replace("{cog}", cog_name)
#             new["value"] = new["value"].replace("{list_commands}",
#                                                 list_commands)

#             dict["fields"].append(new)

#         dict["thumbnail"]["url"] = str(bot.user.avatar_url)

#         dict["footer"]["text"] = settings.config["footer"]
#         dict["footer"]["icon_url"] = str(bot.user.avatar_url)

#         return discord.Embed.from_dict(dict)

#     except Exception as e:
#         print(e)
#         return None


# def get_help_cmd_embed(dict, cmd, bot_icon):
#     try:
#         dict = dp(dict)

#         name_aliases = "|".join([str(cmd), *cmd.aliases])

#         params = []

#         for key, value in cmd.params.items():
#             if key not in ("self", "context"):
#                 params.append(f"[{key}]" if "None" in
#                               str(value) else f"<{key}>")

#         params = " ".join(params)

#         dict["title"] = dict["title"].replace("{cmd}", cmd.name)
#         dict["description"] = dict["description"].replace(
#             "{bot_name}", settings.config["name"])

#         if type(dict["color"]) != int:
#             dict["color"] = int(dict["color"], 16)

#         syntaxe = f"`{settings.prefix}{name_aliases}"
#         if params != "":
#             syntaxe += f" {params}"
#         syntaxe += "`"

#         fields = dict["fields"]
#         for field in fields:
#             field["value"] = field["value"].replace("{name_aliases}",
#                                                     f"`{name_aliases}`")
#             field["value"] = field["value"].replace("{syntaxe}", syntaxe)
#             field["value"] = field["value"].replace(
#                 "{help}", f"{cmd.description}\n\n{cmd.help}")

#         dict["fields"] = fields

#         dict["thumbnail"]["url"] = str(bot_icon)

#         dict["footer"]["text"] = settings.config["footer"]
#         dict["footer"]["icon_url"] = str(bot_icon)

#         return discord.Embed.from_dict(dict)

#     except Exception as e:
#         return None


# def get_birthday_embed(dict, user, age, bot_icon):
#     try:
#         dict = dp(dict)

#         dict["author"]["name"] = user.name
#         dict["author"]["icon_url"] = str(user.avatar_url)

#         if type(dict["color"]) != int:
#             dict["color"] = int(dict["color"], 16)

#         dict["description"] = dict["description"].replace(
#             "{user}", user.mention)

#         for field in dict["fields"]:
#             field["value"] = field["value"].replace("{age}", str(age))

#         dict["footer"]["text"] = settings.config["footer"]
#         dict["footer"]["icon_url"] = str(bot_icon)

#         return discord.Embed.from_dict(dict)

#     except:
#         return None
