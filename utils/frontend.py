import re
import discord
from   init.settings import Settings
from   PIL           import Image, ImageDraw, ImageOps
from   io            import BytesIO
from  copy           import deepcopy as dp


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
