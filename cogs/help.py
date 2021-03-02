# -*- coding: utf-8 -*-

import asyncio
import discord
from   discord.ext import commands


class Help(commands.Cog):

    def __init__(self, bot):

        if not isinstance(bot, commands.Bot):
            print("Bot is not a discord Bot")
            exit(1)

        self.bot = bot

    
    @commands.command(name="help", aliases=["aide"])
    async def help(self, context):
        """
        List all commands from evry Cog
        """
        print("help ... TODO")


def setup(bot):
    bot.add_cog(Help(bot))