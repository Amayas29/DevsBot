# -*- coding: utf-8 -*-

import asyncio
import discord
from   discord.ext import commands


class Events(commands.Cog):

    def __init__(self, bot):

        if not isinstance(bot, commands.Bot):
            print("Bot is not a discord Bot")
            exit(1)

        self.bot = bot

    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        """
        Treatment for commands errors
        """
        print("Erreur ... TODO")

    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """
        When the bor join a guild
        """
        print("Join ... TODO")

    
    @commands.Cog.listener()
    async def on_command(self, ctx):
        """
        When a command is sent
        """
        print("Commande ... TODO")


def setup(bot):
    bot.add_cog(Events(bot))