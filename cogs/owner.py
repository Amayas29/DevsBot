# -*- coding: utf-8 -*-

import asyncio
import discord
from   settings            import Settings
from   discord.ext         import commands


class Owner(commands.Cog):

    def __init__(self, bot):

        if not isinstance(bot, commands.Bot):
            print("Bot is not a discord Bot")
            exit(1)

        self.bot = bot
        self.settings = Settings()


    async def cog_check(self, context):
        return context.author.id in self.settings.owners


    @commands.command(name="shutdown")
    async def shutdown(self, context):
        """
        Make the bot shutdown
        """
        print("Shutdown ... TODO")


    @commands.command(name="setgame")
    async def set_game(self, context, game : str):
        """
        Change the game of the bot
        """
        print("Change game ... TODO")


def setup(bot):
    bot.add_cog(Owner(bot))