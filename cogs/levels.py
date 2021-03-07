# -*- coding: utf-8 -*-

import asyncio
import discord
from   discord.ext   import commands
from   init.settings import Settings


class LevelSystem(commands.Cog):

    def __init__(self, bot):

        if not isinstance(bot, commands.Bot):
            print("Bot is not a discord Bot")
            exit(1)

        self.bot = bot
        self.settings = Settings()


def setup(bot):
    bot.add_cog(LevelSystem(bot))