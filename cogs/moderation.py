# -*- coding: utf-8 -*-

import re
import discord
import json
from   discord import embeds
from   discord.ext    import commands
from   init.settings  import Settings
from   utils.frontend import get_ban_unban_embed, get_warn_embed


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
    async def ban(self, context: commands.Context, member: discord.User, *reason):
        """
        Bans a user from the server.
        """
        reason = " ".join(reason)

        await context.guild.ban(member, reason = reason)

        try:
            embed = get_ban_unban_embed(self.settings.embeds["ban"], member, context.author, reason)
        except:
            embed = None
            
        if embed != None:
            try:
                ban_channel = self.bot.get_channel(self.settings.channels["ban_warn"]) 
                await ban_channel.send(embed = embed)
            
            except:   
                await context.send(embed = embed)        

    @ban.error
    async def ban_error(self, context, error):
        print(type(error))
        await context.send("Error ... in progress")


    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, context: commands.Context, member_id: int, *reason):
        """
        Unbans a user from the server.
        """
        print("Yes unban ...")
        reason = " ".join(reason)

        banned_users = await context.guild.bans()
        find = False
        for ban in banned_users:
            if ban.user.id == member_id:
                find = True
                break
        
        if not find:
            return
        
        await context.guild.unban(ban.user, reason = reason)

        embed = get_ban_unban_embed(self.settings.embeds["unban"], ban.user, context.author, reason)
        if embed != None:
            try:
                ban_channel = self.bot.get_channel(self.settings.channels["ban_warn"]) 
                await ban_channel.send(embed = embed)
            
            except:   
                await context.send(embed = embed)
    

    @commands.command(name="warn")
    @commands.has_permissions(manage_roles=True, ban_members=True)
    async def warn(self, context, member: discord.Member, *reason):
        """
        Warns a user in his private messages.
        """
        print("Warn ... TODO")
        reason = " ".join(reason)
 
        try:
            with open("resources/users.json") as data:
                users : dict = json.load(data)

            warn_user = users[str(member.id)]
            warn_user["warns"] += 1

            with open("resources/users.json", "w") as file:
                json.dump(users, file ,indent=4)
        except:
            pass

        try:
            embed = get_warn_embed(self.settings.embeds["warn"], member, context.author, reason)
        except:
            embed = None
            
        if embed != None:
            try:
                ban_channel = self.bot.get_channel(self.settings.channels["ban_warn"]) 
                await ban_channel.send(embed = embed)
            
            except:   
                await context.send(embed = embed)    

    
    @commands.command(name="warns")
    @commands.has_permissions(manage_roles=True, ban_members=True)
    async def warns(self, context, member: discord.Member, *args):
        """
        Shows the number of warns a user has
        """
        print("Warns ... TODO")


    @commands.command(name="purge", aliases=["clean", "clear"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, context, number: int):
        """
        Delete a number of messages.
        """
        print("purge ... TODO")
        deleted = await context.channel.purge(limit = number + 1)
        await context.send(f"Deleted {len(deleted) - 1} message(s)", delete_after = 5)

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
