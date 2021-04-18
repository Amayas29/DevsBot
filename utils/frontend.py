# -*- coding: utf-8 -*-

from io import BytesIO
import json
import yaml
import discord
from copy import deepcopy as dp
from database.users import get_warns, get_level_exp, get_birth_date
import traceback
from pathlib import Path
from PIL import Image, ImageDraw
import random

embeds_cache = {}
messages_cache = {}
images_cache = {}
gifs_cache = {}

root_dir = str(Path(__file__).parent.parent)

EMBEDS_PATH = f"{root_dir}/resources/embeds/"
MESSAGES_PATH = f"{root_dir}/resources/messages.json"
IMAGES_PATH = f"{root_dir}/resources/images"
GIFS_PATH = f"{root_dir}/resources/gifs.yaml"


def get_embed(embed_name, **kwargs):

    global embeds_cache

    try:

        if embed_name not in embeds_cache:
            with open(f"{EMBEDS_PATH}{embed_name}.json", "r") as f:
                dict_embed = json.load(f)

            embeds_cache[embed_name] = dict_embed

        dict_embed = dp(embeds_cache[embed_name])

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

    global messages_cache

    try:
        if message not in messages_cache:
            with open(MESSAGES_PATH, "r") as f:
                messages_cache = json.load(f)

        msg = dp(messages_cache[message])
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


def get_images_settings(name):

    global images_cache

    try:
        if name not in images_cache:

            with open(f"{IMAGES_PATH}/{name}.yaml", "r") as f:
                welcome_settings = yaml.load(f, Loader=yaml.FullLoader)

            images_cache[name] = welcome_settings

        return images_cache[name]

    except:
        traceback.print_exc()
        return None


def get_gifs(name):

    global gifs_cache

    try:
        if name not in gifs_cache:
            with open(GIFS_PATH, "r") as f:
                gifs_cache = yaml.load(f, Loader=yaml.FullLoader)

        return gifs_cache[name]

    except:
        traceback.print_exc()
        return None


async def generate_file_welcome(user: discord.User):

    try:

        welcome_settings = get_images_settings("welcome_settings")

        asset = user.avatar_url_as(size=welcome_settings["size"])

        data = BytesIO(await asset.read())
        im = Image.open(data)

        im = im.resize(
            (welcome_settings["width"], welcome_settings["height"]))
        bigsize = (im.size[0] * 3, im.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)

        mask = mask.resize(im.size, Image.ANTIALIAS)
        im.putalpha(mask)

        background = Image.open(welcome_settings["path"])
        background.paste(
            im, (welcome_settings["x"], welcome_settings["y"]), im)

        background.save('__welcome__.png')

        return discord.File("__welcome__.png")

    except:
        traceback.print_exc()
        return None


def generate_file_rank(user, server):

    try:
        rank_settings = get_images_settings("rank_settings")

        background = Image.open(rank_settings["path"])
        draw = ImageDraw.Draw(background)
        max = background.size[0]

        level, exp = get_level_exp(user.id, server.id)

        if level == -1:
            exp = max

        else:
            max_exp = 50 * level**2 - 50 * level + 200
            exp = 100 * (exp / max_exp)

        exp = max * exp / 100

        if rank_settings["color"] == []:
            rank_settings["color"] = ["28, 149, 228"]

        color = random.choice(rank_settings["color"])
        color = tuple(map(int, color.split(",")))
        draw.rectangle(((0, 0), (exp, background.size[1])),
                       fill=color,
                       width=background.size[1])

        background.save("__rank__.png")

        return discord.File("__rank__.png")

    except:
        traceback.print_exc()
        return None


def get_head_image():
    coin_settings = get_images_settings("flip_coin_settings")
    return discord.File(coin_settings["head"])


def get_tail_image():
    coin_settings = get_images_settings("flip_coin_settings")
    return discord.File(coin_settings["tail"])


def get_welcome_embed(user, server, text, icon_url):
    return get_embed("welcome", user=user.mention, server=server.name, member_count=str(server.member_count), text=text, icon_url=icon_url)


def get_goodbye_embed(user, server, text, icon_url):
    return get_embed("goodbye", user=user.mention, member_count=str(server.member_count), text=text, icon_url=icon_url)


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


def get_help_cmd_embed(cmd, bot_name, name_aliases, syntaxe, help, text, icon_url):
    return get_embed("helpcmd", cmd=cmd, bot_name=bot_name, name_aliases=name_aliases, syntaxe=syntaxe, help=help, text=text, icon_url=icon_url)


def get_help_all_embed(bot_name, cogs_dict, text, icon_url):
    embed = get_embed("help", bot_name=bot_name, text=text, icon_url=icon_url)

    for name, value in cogs_dict.items():
        embed.add_field(name=f"**{name}**", value=value, inline=False)

    return embed


def get_rank_embed(user, level, exp, text, icon_url):

    if level == -1:
        level = "Max"
        exp = "Max"
        max_exp = ""

    else:
        max_exp = 50 * level**2 - 50 * level + 200
        max_exp = " / " + str(max_exp)

    exp = f"{str(exp)}{str(max_exp)}"

    return get_embed("rank", user_name=user.name, user_icon=str(user.avatar_url), user=user.mention, level=str(level), exp=exp, text=text, icon_url=icon_url)


def get_top_embed(users_dict, text, icon_url):

    embed = get_embed("top", text=text, icon_url=icon_url)

    rank = 1
    for user, l_xp in users_dict.items():
        embed.add_field(name=f"{rank} - {user}",
                        value=f"Niveau {l_xp[0]}, Exp {l_xp[1]}", inline=False)
        rank += 1

    return embed


def get_warns_message(user, guild_id):
    return get_message("warns_message", user, guild_id=guild_id)


def get_muted_message(user):
    return get_message("muted_message", user)


def get_unmuted_message(user):
    return get_message("unmuted_message", user)


def get_nickname_message(user):
    return get_message("nickname_message", user)


def get_levelup_message(user, level):
    return get_message("level_up_message", user, level=level)
