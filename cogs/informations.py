# -*- coding: utf-8 -*-

import asyncio
import discord
import json
from   discord.ext    import commands
from   init.settings  import Settings
from   utils.frontend import get_server_info_embed, get_user_info_embed


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


    @commands.command(name="info")
    async def info(self, context, user : discord.Member):
        """
        Get the user info
        """
        print("My info ... TODO")
        try:
            with open("resources/users.json") as data:
                users : dict = json.load(data)

            embed = get_user_info_embed(self.settings.embeds["user_info"], user, users[str(user.id)])
        except:
            embed = None

        if embed != None:
            await context.send(embed = embed)
    

    @commands.command(name="serverinfo", aliases=["serveurInfo"])
    async def server_info(self, context):
        """
        Get informations about the server
        """
        try:
            server = context.guild
            description = self.settings.config["server_description"]
            embed = get_server_info_embed(self.settings.embeds["server_info"], server, description)

        except:
            embed = None

        if embed != None:
            await context.send(embed = embed)

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