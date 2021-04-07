# -*- coding: utf-8 -*-

import json
import discord
from copy import deepcopy as dp
from database.users import get_warns, get_level_exp, get_birth_date
import traceback

cache = {}
footer = {}
messages = {}
PATH = "resources/embeds/"
MESSAGES = "resources/messages.json"


def get_embed(embed_name, **kwargs):
    global cache
    global footer

    try:

        if embed_name not in cache:
            with open(f"{PATH}{embed_name}.json", "r") as f:
                dict_embed = json.load(f)

            cache[embed_name] = dict_embed

        dict_embed = dp(cache[embed_name])

        if dict_embed["color"] is not None and type(dict_embed["color"]) != int:
            dict_embed["color"] = int(dict_embed["color"], 16)

        for key, value in kwargs.items():

            for atr in dict_embed:

                if type(dict_embed[atr]) == str:
                    dict_embed[atr] = dict_embed[atr].replace(
                        "{" + key + "}", value)

                elif type(dict_embed[atr]) == dict:
                    for sub_atr in dict_embed[atr]:
                        if type(dict_embed[atr][sub_atr]) == str:
                            dict_embed[atr][sub_atr] = dict_embed[atr][sub_atr].replace(
                                "{" + key + "}", value)

                elif type(dict_embed[atr]) == list:
                    for field in dict_embed[atr]:
                        if type(field) == dict:
                            for atr in field:
                                if type(field[atr]) == str:
                                    field[atr] = field[atr].replace(
                                        "{" + key + "}", value)
                else:
                    continue

        return discord.Embed.from_dict(dict_embed)
    except:
        traceback.print_exc()
        return None


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
            warns = get_warns(user.id, guild_id)
            if warns is None:
                warns = 0
            msg = msg.replace("{warns}", str(warns))

        return msg
    except:
        traceback.print_exc()
        return None


def get_ban_embed(user, moderator, reason, text, icon_url):
    if reason == "" or reason is None:
        reason = "NaN"
    return get_embed("ban", user=user.mention, moderator=moderator.mention, reason=reason, text=text, icon_url=icon_url)


def get_unban_embed(user, moderator, reason, text, icon_url):
    if reason == "" or reason is None:
        reason = "NaN"
    return get_embed("unban", user=user.mention, moderator=moderator.mention, reason=reason, text=text, icon_url=icon_url)


def get_warn_embed(user, moderator, reason, text, icon_url):
    if reason == "" or reason is None:
        reason = "NaN"
    return get_embed("warn", user=user.mention, moderator=moderator.mention, reason=reason, text=text, icon_url=icon_url)


def get_kick_embed(user, moderator, reason, text, icon_url):
    if reason == "" or reason is None:
        reason = "NaN"
    return get_embed("kick", user=user.mention, moderator=moderator.mention, reason=reason, text=text, icon_url=icon_url)


def get_warns_message(user, guild_id):
    return get_message("warns_message", user, guild_id=guild_id)


def get_muted_message(user):
    return get_message("muted_message", user)


def get_unmuted_message(user):
    return get_message("unmuted_message", user)


def get_nickname_message(user):
    return get_message("nickname_message", user)


def get_poll_embed(user, question, options, text, icon_url):
    return get_embed("poll", user_name=user.name, user_icon=str(user.avatar_url),
                     question=question, options=options, text=text, icon_url=icon_url)


def get_bot_info_embed(bot_description, languages, prefix, version, text, icon_url):
    return get_embed("botinfo", bot_description=bot_description, languages=languages,
                     prefix=prefix, version=version, text=text, icon_url=icon_url)


def get_server_info_embed(server, description, text, icon_url):

    number_txt_channels = str(len(server.text_channels))
    number_voc_channels = str(len(server.voice_channels))
    created_at = server.created_at.strftime("%d-%m-%Y")

    return get_embed("serverinfo", server=server.name, description=description, member_count=str(server.member_count),
                     number_txt_channels=number_txt_channels, number_voc_channels=number_voc_channels,
                     created_at=created_at, owner=server.owner.name, server_icon=str(
                         server.icon_url),
                     text=text, icon_url=icon_url)


def get_user_info_embed(user, ignored_roles_display, ignored_roles_levels, text, icon_url):

    joined = user.joined_at.strftime("%d-%m-%Y")
    created = user.created_at.strftime("%d-%m-%Y")
    roles = user.roles
    roles = roles[::-1]

    level = None
    max_role = None
    for role in roles:
        if role.id not in ignored_roles_display:
            max_role = role
            if level == None and role.id in ignored_roles_levels:
                level = "Max"
                exp = "Max"
            break

    if max_role is None:
        max_role = "NaN"

    if level != "Max":
        level_exp = get_level_exp(user.id, user.guild.id)
        level = level_exp[0]
        exp = level_exp[1]

    warns = get_warns(user.id, user.guild.id)
    if warns is None:
        warns = 0

    birth_date = get_birth_date(user.id, user.guild.id)
    if birth_date is None:
        birth_date = "NaN"

    return get_embed("userinfo", user_name=user.name, user_icon=str(user.avatar_url), user=user.mention,
                     joined=joined, created=created, max_role=str(max_role),
                     warns=str(warns), level=str(level), exp=str(exp), birth_date=birth_date,
                     text=text, icon_url=icon_url)


def get_invite_embed(server, invite_link, text, icon_url):
    return get_embed("invite", server=server.name, invite_link=invite_link,
                     server_icon=str(server.icon_url), text=text, icon_url=icon_url)


def get_source_embed(bot_name, source_link, author_name, author_link, text, icon_url):
    return get_embed("source", bot_name=bot_name, source_link=source_link, author_name=author_name,
                     author_link=author_link, text=text, icon_url=icon_url)


def get_rules_embed(rules, text, icon_url):
    return get_embed("rules", rules=rules, text=text, icon_url=icon_url)

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
