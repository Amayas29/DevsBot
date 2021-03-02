import os
import discord
from discord.ext.commands.core import command

from utils import default
from bot import Bot

config = default.config()

bot = Bot(
    command_prefix=config["prefix"], prefix=config["prefix"]
)

bot.remove_command("help")

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

try:
    bot.run(config["token"])
except Exception as e:
    print(f'Error when logging in: {e}')