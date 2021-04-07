import os
import dotenv
from init.bot import Bot
from database.database import build, close
import traceback

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = Bot()

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

if build() == False:
    exit(1)

try:
    bot.run(TOKEN)
except:
    traceback.print_exc()


close()
