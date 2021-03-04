# -*- coding: utf-8 -*-

import asyncio
import discord
from   discord.ext   import commands
from   init.settings import Settings


class Informations(commands.Cog):
    
    def __init__(self, bot):

        if not isinstance(bot, commands.Bot):
            print("Bot is not a discord Bot")
            exit(1)

        self.bot = bot
        self.settings = Settings()

    
    @commands.command(name="info", aliases=["botinfo"])
    async def info(self, context):
        """
        Get informations about the bot
        """
        print("Info ... TODO")


    @commands.command(name="serverInfo", aliases=["serveurInfo"])
    async def server_info(self, context):
        """
        Get informations about the server
        """
        print("Info serveur ... TODO")


    @commands.command(name="invite")
    async def invite(self, context):
        """
        Get the invite link of the discord server
        """
        print("Invite ... TODO")

    
    @commands.command(name="source")
    async def source(self, context):
        """
        Get the link to source code of the bot
        """
        print("Source ... TODO")


def setup(bot):
    bot.add_cog(Informations(bot))