import os

import discord
from bot import Bot
from settings import load_settings
import settings

import dotenv


dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")

load_settings()

bot = Bot(
    command_prefix=settings.prefix, prefix=settings.prefix,
)

bot.remove_command("help")

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

try:
    bot.run(TOKEN)
except Exception as e:
    print(f'Error when logging in: {e}')