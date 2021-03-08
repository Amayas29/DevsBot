# -*- coding: utf-8 -*-

import discord
import json
from   init.bot       import Bot
from   discord.ext    import commands
from   init.settings  import Settings
from   utils.frontend import get_server_info_embed, get_user_info_embed, get_invite_embed, get_bot_info_embed


class Informations(commands.Cog):
    
    def __init__(self, bot):

        if not isinstance(bot, Bot):
            print("Bot is not a discord Bot")
            exit(1)

        self.description = "Les commandes d'informations"
        self.bot = bot
        self.settings = Settings()

    
    @commands.command(
        name="botinfo",
        help="",
        description="Affiche les informations et les détails sur bot"
    )
    async def info_bot(self, context):
        """
        Get informations about the bot
        """
        print("Info ... TODO")
        try:
            embed = get_bot_info_embed(self.settings.embeds["bot_info"], self.settings.config["bot_description"], self.settings.config["langages"], self.settings.config["version"], self.bot.user.avatar_url)
        except Exception as e:
            print(e)
            embed = None

        if embed != None:
            await context.send(embed = embed)


    @commands.command(
        name="info",
        help="<user> : Le membre cible",
        description="Affiche les informations d'un membre du serveur"
    )
    async def info(self, context, user : discord.Member):
        """
        Get the user info
        """
        print("My info ... TODO")
        try:
            with open("resources/users.json") as data:
                users : dict = json.load(data)

            embed = get_user_info_embed(self.settings.embeds["user_info"], user, users[str(user.id)], self.bot.user.avatar_url)
        except Exception as e:
            print(e)
            embed = None

        if embed != None:
            await context.send(embed = embed)
    

    @commands.command(
        name="serverinfo",
        help="",
        description="Affiche les informations du serveur"
    )
    async def server_info(self, context):
        """
        Get informations about the server
        """
        print("Info serveur ... TODO")
        try:
            server = context.guild
            description = self.settings.config["server_description"]
            embed = get_server_info_embed(self.settings.embeds["server_info"], server, description,  self.bot.user.avatar_url)

        except:
            embed = None

        if embed != None:
            await context.send(embed = embed)


    @commands.command(
        name="invite",
        help="",
        description="Donne le lien d'invitation pour rejoindre le serveur"
    )
    async def invite(self, context):
        """
        Get the invite link of the discord server
        """
        print("Invite ... TODO")
        try:
            embed = get_invite_embed(self.settings.embeds["invite"], context.guild.name, context.guild.icon_url, self.settings.invite_link, self.bot.user.avatar_url)
        except Exception as e:
            print(e)
            embed = None

        if embed != None:
            await context.send(embed = embed)

    
    # @commands.command(
    #     name="source", 
    #     help="", 
    #     description="Donne le lien pour accéder au code source du bot"
    # )
    # async def source(self, context):
    #     """
    #     Get the link to source code of the bot
    #     """
    #     print("Source ... TODO")


def setup(bot):
    bot.add_cog(Informations(bot))