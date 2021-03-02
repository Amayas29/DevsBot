# -*- coding: utf-8 -*-

import asyncio
import discord
from   discord.ext import commands


class Owner(commands.Cog):

    def __init__(self, bot):

        if not isinstance(bot, commands.Bot):
            print("Bot is not a discord Bot")
            exit(1)

        self.bot = bot


    @commands.command(name="shutdown")
    @commands.is_owner()
    async def shutdown(self, context):
        """
        Make the bot shutdown
        """
        print("Shutdown ... TODO")


    @commands.command(name="setgame")
    @commands.is_owner()
    async def set_game(self, ctx, game : str):
        """
        Change the game of the bot
        """
        print("Change game ... TODO")


def setup(bot):
    bot.add_cog(Owner(bot))