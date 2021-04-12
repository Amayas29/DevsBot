# -*- coding: utf-8 -*-

import traceback
from init.bot import Bot
from discord.ext import commands
from database.servers import create_server, refresh_data
from database.users import add_user, remove_user
from utils.frontend import generate_file_welcome, get_welcome_embed, get_goodbye_embed


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
        print("Guild Join ... TODO")
        server = create_server()

        if server is None:
            return

        try:
            self.bot.servers[str(guild.id)] = server
            refresh_data(self.bot.servers)
        except:
            traceback.print_exc()

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
            traceback.print_exc()

    @commands.Cog.listener()
    async def on_member_join(self, member):

        for role in member.roles:
            if role.is_integration() or role.is_bot_managed():
                return

        file = await generate_file_welcome(member)
        server = self.bot.servers[str(member.guild.id)]
        welcome_chan = self.bot.get_channel(server["channels"]["welcome"])
        if welcome_chan is not None:
            await welcome_chan.send(embed=get_welcome_embed(member, member.guild, self.bot.config["footer"], self.bot.config["icon"]), file=file)

        add_user(member.id, member.guild.id)
        print("Member Join ... TODO")

    @commands.Cog.listener()
    async def on_member_remove(self, member):

        for role in member.roles:
            if role.is_integration() or role.is_bot_managed():
                return

        remove_user(member.id, member.guild.id)

        server = self.bot.servers[str(member.guild.id)]
        goodbye_chan = self.bot.get_channel(server["channels"]["good_bye"])
        if goodbye_chan is not None:
            await goodbye_chan.send(embed=get_goodbye_embed(member, member.guild,
                                                            self.bot.config["footer"], self.bot.config["icon"]))

        print("Removing Member ... TODO")

    # @commands.Cog.listener()
    # async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):

    #     await add_reaction_verification(self.bot, payload)

    # @commands.Cog.listener()
    # async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
    #     pass


def setup(bot):
    bot.add_cog(Events(bot))
