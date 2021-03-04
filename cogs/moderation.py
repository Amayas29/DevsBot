# -*- coding: utf-8 -*-

import asyncio
import discord
from   discord.ext   import commands
from   init.settings import Settings


class Moderation(commands.Cog):

    def __init__(self, bot):

        if not isinstance(bot, commands.Bot):
            print("Bot is not a discord Bot")
            exit(1)

        self.bot = bot
        self.settings = Settings()


    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, context, member: discord.Member, *args):
        """
        Kick a user out of the server.
        """
        print("kick ... TODO")

    
    @commands.command(name="nick")
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, context, member: discord.Member, *, name: str):
        """
        Change the nickname of a user on a server.
        """
        print("nick ... TODO")


    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, context, member: discord.Member, *args):
        """
        Bans a user from the server.
        """
        print("ban ... TODO")


    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, context, member_id, *args):
        """
        Unbans a user from the server.
        """
        print("Unban ... TODO")
    

    @commands.command(name="warn")
    @commands.has_permissions(manage_roles=True, ban_members=True)
    async def warn(self, context, member: discord.Member, *args):
        """
        Warns a user in his private messages.
        """
        print("Warn ... TODO")

    
    @commands.command(name="warns")
    @commands.has_permissions(manage_roles=True, ban_members=True)
    async def warns(self, context, member: discord.Member, *args):
        """
        Shows the number of warns a user has
        """
        print("Warns ... TODO")


    @commands.command(name="purge")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, context, number):
        """
        Delete a number of messages.
        """
        print("purge ... TODO")

    
    @commands.command()
    @commands.has_permissions(mute_members = True)
    async def mute(self, context, user:discord.Member):
        """
        Mutes a user from the current server
        """
        print("Mute ... TODO")

    
    @commands.command()
    @commands.has_permissions(mute_members = True)
    async def unmute(self, context, user:discord.Member):
        """
        Unmutes a user from the current server
        """
        print("Unmute ... TODO")


    @commands.command(name="rules")
    @commands.has_permissions(manage_channels=True)
    async def rules(self, context, user:discord.Member=None):
        """
        Send the rules
        """
        print("Rules ... TODO")
    

def setup(bot):
    bot.add_cog(Moderation(bot))
