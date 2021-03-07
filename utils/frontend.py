# -*- coding: utf-8 -*-

import discord
from   init.settings import Settings
from   PIL           import Image, ImageDraw, ImageOps
from   io            import BytesIO
from   copy          import deepcopy as dp


settings = Settings()


def get_ban_unban_embed(dict: dict, banned_user: discord.User, moderator: discord.User, reason: str) -> discord.Embed :
    try:
        dict = dp(dict)

        if reason == "" or reason is None:
            reason = "NaN"

        if type(dict["color"]) != int:
            dict["color"] = int(dict["color"], 16)

        dict["description"] = dict["description"].replace("{banned_user}", banned_user.mention)

        fields = dict["fields"]
        for field in fields:
            field["value"] = field["value"].replace("{reason}", reason)
            field["value"] = field["value"].replace("{moderator}", moderator.mention)
        dict["fields"] = fields

        dict["footer"]["text"] = settings.config["footer"]

        return discord.Embed.from_dict(dict)

    except:
        return None


def get_welcome_goodbye_embed(dict: dict, user: discord.User, server: str, member_count: int):

    try:
        dict = dp(dict)
        
        if type(dict["color"]) != int:
            dict["color"] = int(dict["color"], 16)
        
        dict["description"] = dict["description"].replace("{user}", user.mention)
        dict["description"] = dict["description"].replace("{server}", server)

        fields = dict["fields"]
        for field in fields:
            field["value"] = field["value"].replace("{member_count}", str(member_count))

        dict["footer"]["text"] = settings.config["footer"]

        return discord.Embed.from_dict(dict)
        
    except:
        return None


def get_warn_embed(dict: dict, warn_user: discord.User, moderator: discord.User, reason: str) -> discord.Embed :
    try:
        dict = dp(dict)

        if reason == "" or reason is None:
            reason = "NaN"

        if type(dict["color"]) != int:
            dict["color"] = int(dict["color"], 16)

        dict["description"] = dict["description"].replace("{warn_user}", warn_user.mention)

        fields = dict["fields"]
        for field in fields:
            field["value"] = field["value"].replace("{reason}", reason)
            field["value"] = field["value"].replace("{moderator}", moderator.mention)
        
        dict["fields"] = fields
        dict["footer"]["text"] = settings.config["footer"]

        return discord.Embed.from_dict(dict)

    except:
        return None


def get_server_info_embed(dict: dict, server, description: str) -> discord.Embed :
    try:
        number_txt_channels = len(server.text_channels)
        number_voc_channels = len(server.voice_channels)
        member_count = server.member_count
        owner = server.owner.name
        created_at = server.created_at.strftime("%d-%m-%Y") 
        dict = dp(dict)

        if type(dict["color"]) != int:
            dict["color"] = int(dict["color"], 16)

        dict["description"] = dict["description"].replace("{server}", server.name)
        dict["description"] = dict["description"].replace("{description}", description)

        fields = dict["fields"]
        for field in fields:
            field["value"] = field["value"].replace("{member_count}", str(member_count))
            field["value"] = field["value"].replace("{number_txt_channels}", str(number_txt_channels))
            field["value"] = field["value"].replace("{number_voc_channels}", str(number_voc_channels))
            field["value"] = field["value"].replace("{created_at}", created_at)
            field["value"] = field["value"].replace("{owner}", owner)
            
        dict["fields"] = fields
        dict["footer"]["text"] = settings.config["footer"]

        return discord.Embed.from_dict(dict)

    except:
        return None


def get_user_info_embed(dict, user, user_dict):
    try:
        dict = dp(dict)
        joined = user.joined_at.strftime("%d-%m-%Y") 
        created = user.created_at.strftime("%d-%m-%Y")
        roles = user.roles

        roles = roles[::-1]

        level = None
        max_role = None
        for role in roles:
            if max_role == None and role.id not in settings.ignored_roles_display:
                max_role = role
            if level == None and role.id in settings.ignored_roles_levels:
                level = "Max"
                exp = "Max"

        warns = user_dict["warns"]
        if level == None:
            level = user_dict["level"]
            exp = user_dict["exp"]
        birth_date = user_dict["birth_date"]
        icon_url = user.avatar_url
        author = dict["author"]
        author["name"] = author["name"].replace("{name}", user.name)
        author["icon_url"] = author["icon_url"].replace("{icon_url}", str(icon_url))
        dict["author"] = author

        if type(dict["color"]) != int:
            dict["color"] = int(dict["color"], 16)

        dict["description"] = dict["description"].replace("{user}", user.mention)

        fields = dict["fields"]
        for field in fields:
            field["value"] = field["value"].replace("{joined}", joined)
            field["value"] = field["value"].replace("{created}", created)
            field["value"] = field["value"].replace("{roles}", max_role.mention)
            field["value"] = field["value"].replace("{warns}", str(warns))
            field["value"] = field["value"].replace("{level}", str(level))
            field["value"] = field["value"].replace("{exp}", str(exp))
            field["value"] = field["value"].replace("{birth_date}", str(birth_date))

        dict["fields"] = fields
        dict["footer"]["text"] = settings.config["footer"]

        return discord.Embed.from_dict(dict)

    except Exception as e:
        print(e)
        return None


async def get_file_welcome(user: discord.User):

    try:
        welcome_settings = settings.images_generator["welcome"]

        asset = user.avatar_url_as(size=welcome_settings["size"])

        data = BytesIO(await asset.read())
        im = Image.open(data)

        im = im.resize((welcome_settings["width"], welcome_settings["height"]))
        bigsize = (im.size[0] * 3, im.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + bigsize, fill=255)

        mask = mask.resize(im.size, Image.ANTIALIAS)
        im.putalpha(mask)

        background = Image.open(welcome_settings["path"])
        background.paste(im, (welcome_settings["x"], welcome_settings["y"]), im)

        background.save('__image_generator__.png')

        return discord.File("__image_generator__.png")

    except:
        return None
