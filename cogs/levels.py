# -*- coding: utf-8 -*-

import asyncio
from re import I
import discord
from discord import file
from   discord.ext      import commands
from   init.settings    import Settings
from   utils.frontend import get_file_rank

class LevelSystem(commands.Cog):

    def __init__(self, bot):

        if not isinstance(bot, commands.Bot):
            print("Bot is not a discord Bot")
            exit(1)

        self.bot = bot
        self.settings = Settings()


    @commands.command(name="rank")
    async def rank(self, context):
        file = get_file_rank(context.author)
        await context.send(file=file)


def setup(bot):
    bot.add_cog(LevelSystem(bot))