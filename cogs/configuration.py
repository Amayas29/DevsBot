# -*- coding: utf-8 -*-

import discord
from init.bot import Bot
from discord.ext import commands
from database.servers import refresh_data


class Configuration(commands.Cog):

    def __init__(self, bot):

        if not isinstance(bot, Bot):
            print("Bot is not a discord Bot")
            exit(1)

        self.description = "Les commandes de modération, elles fonctionnent si seulement si vous êtes modérateur"
        self.bot = bot

    async def cog_check(self, context: commands.Context):
        try:

            if context.author == context.guild.owner:
                return True

            for role in context.author.roles:
                if role.id in self.bot.servers[str(context.guild.id)]["moderators_roles"]:
                    return True
            return False
        except:
            return False

    @commands.command(
        name="prefix",
        help="<prefix> : Le nouveau prefix du bot",
        description="Changer le prefix du bot"
    )
    async def prefix(self, context, prefix):
        """
            Change the bot prefix
        """
        print("prefix ... TODO")
        server = self.bot.servers[str(context.guild.id)]
        server["prefix"] = prefix
        refresh_data(self.bot.servers)

    @commands.command(
        name="description",
        help="<description> La description du serveur",
        description="Permet de changer la description du serveur"
    )
    async def description(self, context, *, description):
        """
            Change the description of the server
        """
        print("Description ... TODO")

        description = "".join(description)
        self.bot.servers[str(context.guild.id)]["description"] = description
        refresh_data(self.bot.servers)

    @commands.command(
        name="setrules",
        help="<rules> Les regles du serveur",
        description="Permet de changer les regles du serveur"
    )
    async def set_rules(self, context, *, rules):
        """
            Change the rules of the server
        """
        print("Description ... TODO")

        rules = "".join(rules)
        self.bot.servers[str(context.guild.id)]["rules"] = rules
        refresh_data(self.bot.servers)

    @commands.command(
        name="chan",
        help="<type> Le type de channel à enregistrer",
        description="Enregistrer le salon avec son type"
    )
    async def chan(self, context, *, type):
        type = "".join(type)

        if type == "":
            await context.message.add_reaction("❌")
            return

        channels = self.bot.servers[str(context.guild.id)]["channels"]

        if type not in channels:
            await context.message.add_reaction("❌")
            return

        self.bot.servers[str(context.guild.id)
                         ]["channels"][type] = context.channel.id

        refresh_data(self.bot.servers)

        await context.message.add_reaction("✅")

    @commands.command(
        name="mode_role",
        help="<role> Le rôle a ajouter au roles de moderations",
        description="Ajout un role à la liste des roles de moderations"
    )
    async def moderation_role(self, context, role: discord.Role):

        if role.id in self.bot.servers[str(context.guild.id)
                                       ]["moderators_roles"]:
            return

        self.bot.servers[str(context.guild.id)
                         ]["moderators_roles"].append(role.id)
        refresh_data(self.bot.servers)

    @commands.command(
        name="mute_role",
        help="<role> Le rôle de muet",
        description="Selectionne le muted role du serveur"
    )
    async def muted_role(self, context, role: discord.Role):

        self.bot.servers[str(context.guild.id)
                         ]["muted_role"] = role.id
        refresh_data(self.bot.servers)

    @commands.command(
        name="hide_role",
        help="<role> Le rôle a ajouter à la liste",
        description="Ajout un role à la liste des roles ignores à l'affichage"
    )
    async def hide_role(self, context, role: discord.Role):

        if role.id in self.bot.servers[str(context.guild.id)
                                       ]["ignored_roles_display"]:
            return

        self.bot.servers[str(context.guild.id)
                         ]["ignored_roles_display"].append(role.id)
        refresh_data(self.bot.servers)

    @commands.command(
        name="not_level",
        help="<role> Le rôle a ajouter à la liste",
        description="Ajout un role à la liste des roles ignores du systeme de niveau"
    )
    async def moderation_role(self, context, role: discord.Role):

        if role.id in self.bot.servers[str(context.guild.id)
                                       ]["ignored_roles_levels"]:
            return

        self.bot.servers[str(context.guild.id)
                         ]["ignored_roles_levels"].append(role.id)
        refresh_data(self.bot.servers)

    @commands.command(
        name="init_role",
        help="<role> Le rôle a ajouter à la liste intiale",
        description="Ajout un role à la liste des roles initiales"
    )
    async def init_role(self, context, role: discord.role):

        if role.id in self.bot.servers[str(context.guild.id)
                                       ]["initial_roles"]:
            return

        self.bot.servers[str(context.guild.id)
                         ]["initial_roles"].append(role.id)

        refresh_data(self.bot.servers)


def setup(bot):
    bot.add_cog(Configuration(bot))
