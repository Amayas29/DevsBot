# -*- coding: utf-8 -*-

import discord
from init.bot import Bot
from discord.ext import commands
from utils.frontend import get_bot_info_embed, get_server_info_embed, get_user_info_embed, get_invite_embed, get_source_embed
from database.servers import refresh_data
import traceback


class Informations(commands.Cog):

    def __init__(self, bot):

        if not isinstance(bot, Bot):
            print("Bot is not a discord Bot")
            exit(1)

        self.description = "Les commandes d'informations"
        self.bot = bot

    @commands.command(
        name="botinfo",
        help="",
        description="Affiche les informations et les détails sur bot")
    async def info_bot(self, context):
        """
        Get informations about the bot
        """
        print("Info ... TODO")
        try:
            embed = get_bot_info_embed(self.bot.config["bot_description"], self.bot.config["languages"], self.bot.servers[str(
                context.guild.id)]["prefix"], self.bot.config["version"], self.bot.config["footer"], self.bot.config["icon"])

        except:
            embed = None

        if embed != None:
            await context.send(embed=embed)

    @commands.command(
        name="info",
        help="<user> : Le membre cible",
        description="Affiche les informations d'un membre du serveur")
    async def info(self, context, user: discord.Member):
        """
        Get the user info
        """
        print("My info ... TODO")
        try:
            embed = get_user_info_embed(user, self.bot.servers[str(context.guild.id)]["ignored_roles_display"], self.bot.servers[str(
                context.guild.id)]["ignored_roles_levels"], self.bot.config["footer"], self.bot.config["icon"])

        except:
            embed = None

        if embed != None:
            await context.send(embed=embed)

    @ commands.command(name="serverinfo",
                       help="",
                       description="Affiche les informations du serveur")
    async def server_info(self, context):
        """
        Get informations about the server
        """
        print("Info serveur ... TODO")
        try:
            embed = get_server_info_embed(
                context.guild, self.bot.servers[str(
                    context.guild.id)]["description"],
                self.bot.config["footer"], self.bot.config["icon"])

        except:
            embed = None

        if embed != None:
            await context.send(embed=embed)

    @commands.command(
        name="invite",
        help="",
        description="Donne le lien d'invitation pour rejoindre le serveur")
    async def invite(self, context):
        """
        Get the invite link of the discord server
        """
        print("Invite ... TODO")
        try:
            invite_link = self.bot.servers[str(
                context.guild.id)]["invite_link"]

            if invite_link is None:
                invite_link = await context.channel.create_invite()
                self.bot.servers[str(context.guild.id)
                                 ]["invite_link"] = str(invite_link)
                refresh_data(self.bot.servers)

            embed = get_invite_embed(
                context.guild, str(invite_link), self.bot.config["footer"], self.bot.config["icon"])

        except:
            traceback.print_exc()

            embed = None

        if embed != None:
            await context.send(embed=embed)

    @commands.command(
        name="source",
        help="",
        description="Donne le lien pour accéder au code source du bot"
    )
    async def source(self, context):
        """
        Get the link to source code of the bot
        """
        print("Source ... TODO")
        try:
            embed = get_source_embed(
                self.bot.config["name"], self.bot.config["source"], self.bot.config["author"]["name"],
                self.bot.config["author"]["github"], self.bot.config["footer"], self.bot.config["icon"])

        except:
            embed = None

        if embed != None:
            await context.send(embed=embed)


def setup(bot):
    bot.add_cog(Informations(bot))
