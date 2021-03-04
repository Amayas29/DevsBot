import os
import discord
import dotenv
from   init.bot import Bot


dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = Bot()

bot.remove_command("help")

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

try:
    bot.run(TOKEN)
except Exception as e:
    print(f'Error when logging in: {e}')