# -*- coding: utf-8 -*-

import discord
from init.bot import Bot
from discord.ext import commands
from database.servers import create_server, refresh_data
from database.users import add_user, remove_user


class Events(commands.Cog):

    def __init__(self, bot):

        if not isinstance(bot, Bot):
            print("Bot is not a discord Bot")
            exit(1)

        self.bot = bot

    # @commands.Cog.listener()
    # async def on_command_error(self, context, error):
    #     """
    #     Treatment for commands errors
    #     """
    #     if context.command == None:
    #         return

    #     # help = self.bot.get_command("help")

    #     # if help is None:
    #     #     return

    #     # await help(context, context.command.name)
    #     print("Erreur ... TODO", error)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """
        When the bot join a guild
        """
        print("GUild Join ... TODO")
        server = create_server()

        if server is None:
            return

        try:
            self.bot.servers[str(guild.id)] = server
            refresh_data(self.bot.servers)
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        """
        When the bot left a guild
        """
        print("Guild left ... TODO")
        try:
            self.bot.servers.pop(str(guild.id))
            refresh_data(self.bot.servers)
        except:
            pass

    @commands.Cog.listener()
    async def on_member_join(self, member):

        for role in member.roles:
            if role.is_integration() or role.is_bot_managed():
                return

        add_user(member.id, member.guild.id)
        print("Member Join ... TODO")

        # server: discord.Guild = member.guild

        # try:
        #     embed = get_welcome_goodbye_embed(
        #         self.settings.embeds["welcome"], member, server.name, server.member_count, self.bot.user.avatar_url)
        # except:
        #     embed = None

        # if embed != None:
        #     try:
        #         welcome_channel = self.bot.get_channel(
        #             self.settings.channels["welcome"])
        #         file = await get_file_welcome(member)
        #         await welcome_channel.send(embed=embed, file=file)
        #     except:
        #         pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):

        for role in member.roles:
            if role.is_integration() or role.is_bot_managed():
                return

        remove_user(member.id, member.guild.id)

        print("Removing Member ... TODO")
        # server: discord.Guild = member.guild

        # await delete_reactions(member)

        # try:
        #     embed = get_welcome_goodbye_embed(
        #         self.settings.embeds["good_bye"], member, server.name, server.member_count, self.bot.user.avatar_url)
        # except:
        #     embed = None

        # if embed != None:
        #     try:
        #         welcome_channel = self.bot.get_channel(
        #             self.settings.channels["good_bye"])
        #         await welcome_channel.send(embed=embed)
        #     except:
        #         pass

    # @commands.Cog.listener()
    # async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):

    #     await add_reaction_verification(self.bot, payload)

    # @commands.Cog.listener()
    # async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
    #     pass


def setup(bot):
    bot.add_cog(Events(bot))
