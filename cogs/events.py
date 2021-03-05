# -*- coding: utf-8 -*-

import asyncio
import discord
from   discord.ext    import commands
from   init.settings  import Settings
from   utils.frontend import get_welcome_embed, get_file_welcome

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
    async def on_member_join(self, member):
        print("Yes")
        server : discord.Guild = member.guild

        try:
            embed = get_welcome_embed(self.settings.embeds["welcome"], member, server.name, server.member_count)
        except:
            embed = None

        if embed != None:
            try:
                welcome_channel = self.bot.get_channel(self.settings.channels["welcome"]) 
                file = await get_file_welcome(member)
                await welcome_channel.send(embed = embed, file=file)
            except:   
               pass  


    # @commands.Cog.listener()
    # async def on_member_remove(self, member):
    #     channel_good_bye = member.guild.get_channel(int(self.channels["good_bye"]))
    #     await channel_good_bye.send(f"A dieu mon enfant {member.mention}")


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