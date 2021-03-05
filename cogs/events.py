# -*- coding: utf-8 -*-

import asyncio
import discord
import json
from discord import user
from   discord.ext    import commands
from   init.settings  import Settings
from   utils.frontend import get_welcome_goodbye_embed, get_file_welcome

class Events(commands.Cog):

    def __init__(self, bot):

        if not isinstance(bot, commands.Bot):
            print("Bot is not a discord Bot")
            exit(1)

        self.bot = bot
        self.settings = Settings()
    

    @commands.Cog.listener()
    async def on_command_error(self, context: commands.Context, error):
        """
        Treatment for commands errors
        """
        if context.command != None and hasattr(context.command, "on_error"):
            return

        print("Erreur ... TODO", error)

    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """
        When the bot join a guild
        """
        print("Join ... TODO")


    @commands.Cog.listener()
    async def on_member_join(self, member: discord.User):

        try:
            with open("resources/users.json") as data:
                users : dict = json.load(data)
        except:
            pass

        users[str(member.id)] = {
            "level" : "0",
            "exp" : 0,
            "warns" : 0,
            "birth_date" : "NaN"
        }

        try:
            with open("resources/users.json", "w") as file:
                json.dump(users, file ,indent=4)
        except:
            pass
        

        server : discord.Guild = member.guild

        try:
            embed = get_welcome_goodbye_embed(self.settings.embeds["welcome"], member, server.name, server.member_count)
        except:
            embed = None

        if embed != None:
            try:
                welcome_channel = self.bot.get_channel(self.settings.channels["welcome"]) 
                file = await get_file_welcome(member)
                await welcome_channel.send(embed = embed, file=file)
            except:   
               pass  


    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        try:
            with open("resources/users.json") as data:
                users : dict = json.load(data)
        except:
            pass

        users.pop(str(member.id))

        try:
            with open("resources/users.json", "w") as file:
                json.dump(users, file ,indent=4)
        except:
            pass
        

        server : discord.Guild = member.guild

        try:
            embed = get_welcome_goodbye_embed(self.settings.embeds["good_bye"], member, server.name, server.member_count)
        except:
            embed = None

        if embed != None:
            try:
                welcome_channel = self.bot.get_channel(self.settings.channels["good_bye"]) 
                await welcome_channel.send(embed = embed)
            except:   
               pass 


    # @commands.Cog.listener()
    # async def on_command(self, context):
    #     """
    #     When a command is sent
    #     """
    #     print("Commande ... TODO")


def setup(bot):
    bot.add_cog(Events(bot))