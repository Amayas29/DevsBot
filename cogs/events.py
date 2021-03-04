# -*- coding: utf-8 -*-

import asyncio
import discord
from   discord.ext import commands
from   settings    import Settings

class Events(commands.Cog):

    def __init__(self, bot):

        if not isinstance(bot, commands.Bot):
            print("Bot is not a discord Bot")
            exit(1)

        self.bot = bot
        self.settings = Settings()
    

    @commands.Cog.listener()
    async def on_command_error(self, context, error):
        """
        Treatment for commands errors
        """
        print("Erreur ... TODO", error)

    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """
        When the bor join a guild
        """
        print("Join ... TODO")


    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel_welcome = member.guild.get_channel(int(self.channels["welcome"]))
        await channel_welcome.send(f"Bienvenu mon bro {member.mention}")


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel_good_bye = member.guild.get_channel(int(self.channels["good_bye"]))
        await channel_good_bye.send(f"A dieu mon enfant {member.mention}")


    # @commands.Cog.listener()
    # async def on_reaction_add(self, reaction, user):
    #     await reaction.message.add_reaction(reaction.emoji)


    # @commands.Cog.listener()
    # async def on_typing(self, channel, user, when):
    #     await channel.send(f"{user.name} a commence a écrire dans ce channel le {when}")


    @commands.Cog.listener()
    async def on_command(self, context):
        """
        When a command is sent
        """
        print("Commande ... TODO")


def setup(bot):
    bot.add_cog(Events(bot))