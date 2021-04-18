# -*- coding: utf-8 -*-

import discord
from init.bot import Bot
from discord.ext import commands
from utils.frontend import get_ban_embed, get_unban_embed, get_warn_embed, get_kick_embed, get_warns_message, get_muted_message, get_unmuted_message, get_nickname_message, get_rules_embed
from database.users import add_warn
from database.servers import refresh_data
import traceback


class Moderation(commands.Cog):

    def __init__(self, bot):

        if not isinstance(bot, Bot):
            print("Bot is not a discord Bot")
            exit(1)

        self.description = "Les commandes de modération, elles fonctionnent si seulement si vous êtes modérateur"
        self.bot = bot

    async def cog_check(self, context):
        try:
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
        name='kick',
        help="<member> : Le membre a expulsé.\n[reason] : La raison du kick",
        description="Expulser un membre du serveur")
    @commands.has_permissions(kick_members=True)
    async def kick(self, context, member: discord.Member, *, reason=None):
        """
        Kick a user out of the server.
        """
        print("kick ... TODO")
        if reason != None:
            reason = "".join(reason)

        await context.guild.kick(member, reason=reason)

        try:
            embed = get_kick_embed(member,
                                   context.author, reason,
                                   self.bot.config["footer"], self.bot.config["icon"])
        except:
            traceback.print_exc()
            embed = None

        if embed != None:
            try:
                ban_channel = self.bot.get_channel(
                    self.bot.servers[str(context.guild.id)]["channels"]["kick"])

                await ban_channel.send(embed=embed)

            except:
                await context.send(embed=embed)

    @commands.command(
        name="nick",
        help="<member> : Le membre cible.\n<name> : Le nouveau surnom",
        description="Changer le surnom d'un membre dans le serveur")
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, context, member: discord.Member, *, name):
        """
        Change the nickname of a user on a server.
        """
        print("nick ... TODO")
        name = "".join(name)
        await member.edit(nick=name)

        nickname_message = get_nickname_message(member)

        if nickname_message == None:
            return

        await context.send(nickname_message)

    @commands.command(
        name="ban",
        help="<member> : Le membre a bannir.\n[reason] : La raison du ban",
        description="Bannir un membre du serveur")
    @commands.has_permissions(ban_members=True)
    async def ban(self, context, member: discord.Member, *, reason=None):
        """
        Bans a user from the server.
        """
        if reason != None:
            reason = "".join(reason)

        await context.guild.ban(member, reason=reason)

        try:
            embed = get_ban_embed(member,
                                  context.author, reason,
                                  self.bot.config["footer"], self.bot.config["icon"])
        except:
            embed = None

        if embed != None:
            try:
                ban_channel = self.bot.get_channel(
                    self.bot.servers[str(context.guild.id)]["channels"]["ban_warn"])

                await ban_channel.send(embed=embed)

            except:
                await context.send(embed=embed)

    @commands.command(
        name="unban",
        help="<member_id> : L'identifiant du membre a pardonné.\n[reason] : La raison du unban",
        description="Pardonner à un membre")
    @commands.has_permissions(ban_members=True)
    async def unban(self, context, member_id: int, *, reason=None):
        """
        Unbans a user from the server.
        """
        print("Yes unban ...")
        if reason != None:
            reason = "".join(reason)

        banned_users = await context.guild.bans()
        find = False
        for ban in banned_users:
            if ban.user.id == member_id:
                find = True
                break

        if not find:
            return

        await context.guild.unban(ban.user, reason=reason)

        try:
            embed = get_unban_embed(ban.user,
                                    context.author, reason,
                                    self.bot.config["footer"], self.bot.config["icon"])
        except:
            embed = None

        if embed != None:
            try:
                ban_channel = self.bot.get_channel(
                    self.bot.servers[str(context.guild.id)]["channels"]["ban_warn"])

                await ban_channel.send(embed=embed)

            except:
                await context.send(embed=embed)

    @commands.command(
        name="warn",
        help="<member> : Le membre a avertir.\n[reason] : La raison du warn",
        description="Avertir un membre du serveur")
    @commands.has_permissions(manage_roles=True, ban_members=True)
    async def warn(self, context, member: discord.Member, *, reason=None):
        """
        Warns a user in his private messages.
        """
        print("Warn ... TODO")
        if reason != None:
            reason = "".join(reason)

        add_warn(member.id, member.guild.id)

        try:
            embed = get_warn_embed(member,
                                   context.author, reason,
                                   self.bot.config["footer"], self.bot.config["icon"])
        except:
            embed = None

        if embed != None:
            try:
                warn_channel = self.bot.get_channel(
                    self.bot.servers[str(context.guild.id)]["channels"]["ban_warn"])

                await warn_channel.send(embed=embed)

            except:
                traceback.print_exc()
                await context.send(embed=embed)

    @commands.command(
        name="warns",
        help="<member> : Le membre cible",
        description="Affiche le nombre cumulé d'avertissement d'un membre")
    @commands.has_permissions(manage_roles=True, ban_members=True)
    async def warns(self, context, member: discord.Member):
        """
        Shows the number of warns a user has
        """
        warns_message = get_warns_message(member, context.guild.id)
        if warns_message == None:
            return

        await context.send(warns_message)

    @commands.command(
        name="clear",
        aliases=["clean", "purge"],
        help="<number> : Le nombre de message à supprimer",
        description="Supprimer un nombre de messages dans un salon")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, context, number: int):
        """
        Delete a number of messages.
        """
        print("clear ... TODO")
        deleted = await context.channel.purge(limit=number + 1)
        await context.send(f"Deleted {len(deleted) - 1} message(s)",
                           delete_after=5)

    @commands.command(name="mute",
                      help="<member> : Le membre cible",
                      description="Mettre un membre Muet")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, context, member: discord.Member):
        """
        Mutes a user from the current server
        """
        print("Mute ... TODO")
        try:
            muted_role = context.guild.get_role(
                self.bot.servers[str(context.guild.id)]["muted_role"])

            await member.add_roles(muted_role)
            muted_message = get_muted_message(member)

            if muted_message == None:
                return

            await context.send(muted_message)
        except:
            traceback.print_exc()

    @commands.command(name="unmute",
                      help="<member> : Le membre cible",
                      description="Enleve le Muet pour un membre")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, context, member: discord.Member):
        """
        Unmutes a user from the current server
        """
        print("Unmute ... TODO")

        try:
            muted_role = context.guild.get_role(
                self.bot.servers[str(context.guild.id)]["muted_role"])

            await member.remove_roles(muted_role)
            unmuted_message = get_unmuted_message(member)

            if unmuted_message == None:
                return

            await context.send(unmuted_message)
        except:
            traceback.print_exc()

    @commands.command(name="rules",
                      help="",
                      description="Affiche dans le salon les régles du serveur"
                      )
    @commands.has_permissions(manage_channels=True)
    async def rules(self, context):
        """
        Send the rules
        """
        print("Rules ... TODO")
        try:
            rules = self.bot.servers[str(context.guild.id)]["rules"]
            if rules is None:
                rules = "NaN"

            embed = get_rules_embed(self.bot.servers[str(
                context.guild.id)]["rules"], self.bot.config["footer"], self.bot.config["icon"])

        except:
            traceback.print_exc()
            embed = None

        if embed != None:
            await context.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
