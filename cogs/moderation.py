# -*- coding: utf-8 -*-

import discord
import json
from   init.bot       import Bot
from   discord.ext    import commands
from   init.settings  import Settings
from   utils.frontend import get_ban_unban_embed, get_warn_embed, get_kick_embed, get_rules_embed


class Moderation(commands.Cog):

    def __init__(self, bot):

        if not isinstance(bot, Bot):
            print("Bot is not a discord Bot")
            exit(1)

        self.description = "Les commandes de modération, elles fonctionnent si seulement si vous êtes modérateur"
        self.bot = bot
        self.settings = Settings()


    async def cog_check(self, context):
        for role in context.author.roles:
            if role.id in self.settings.moderators_roles:
                return True
        return False


    @commands.command(
        name='kick',
        help="<member> : Le membre a expulsé.\n[reason] : La raison du kick",
        description="Expulser un membre du serveur"
    )
    @commands.has_permissions(kick_members=True)
    async def kick(self, context, member: discord.Member, *, reason = None):
        """
        Kick a user out of the server.
        """
        print("kick ... TODO")
        if reason != None:
            reason = " ".join(reason)

        await context.guild.kick(member, reason = reason)

        try:
            embed = get_kick_embed(self.settings.embeds["kick"], member, context.author, reason, self.bot.user.avatar_url)
        except:
            embed = None
            
        if embed != None:
            try:
                ban_channel = self.bot.get_channel(self.settings.channels["kick"]) 
                await ban_channel.send(embed = embed)
            
            except:   
                await context.send(embed = embed)    

    
    @commands.command(
        name="nick",
        help="<member> : Le membre cible.\n<name> : Le nouveau surnom",
        description="Changer le surnom d'un membre dans le serveur"
    )
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, context, member: discord.Member, *, name):
        """
        Change the nickname of a user on a server.
        """
        print("nick ... TODO")
        try:
            name = "".join(name)
            await member.edit(nick=name)
            muted_message = self.settings.messages["nickname"]
            muted_message = muted_message.replace("{user}", member.mention)
            await context.send(muted_message)
        except:
            pass


    @commands.command(
        name="ban",
        help="<member> : Le membre a bannir.\n[reason] : La raison du ban",
        description="Bannir un membre du serveur"
    )
    @commands.has_permissions(ban_members=True)
    async def ban(self, context, member: discord.Member, *, reason = None):
        """
        Bans a user from the server.
        """
        if reason != None:
            reason = " ".join(reason)

        await context.guild.ban(member, reason = reason)

        try:
            embed = get_ban_unban_embed(self.settings.embeds["ban"], member, context.author, reason, self.bot.user.avatar_url)
        except:
            embed = None
            
        if embed != None:
            try:
                ban_channel = self.bot.get_channel(self.settings.channels["ban_warn"]) 
                await ban_channel.send(embed = embed)
            
            except:   
                await context.send(embed = embed)        


    @commands.command(
        name="unban",
        help="<member_id> : L'identifiant du membre a pardonné.\n[reason] : La raison du unban",
        description="Pardonner à un membre"
    )
    @commands.has_permissions(ban_members=True)
    async def unban(self, context, member_id: int, *, reason = None):
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

        embed = get_ban_unban_embed(self.settings.embeds["unban"], ban.user, context.author, reason, self.bot.user.avatar_url)
        if embed != None:
            try:
                ban_channel = self.bot.get_channel(self.settings.channels["ban_warn"]) 
                await ban_channel.send(embed = embed)
            
            except:   
                await context.send(embed = embed)
    

    @commands.command(
        name="warn",
        help="<member> : Le membre a avertir.\n[reason] : La raison du warn",
        description="Avertir un membre du serveur"
    )
    @commands.has_permissions(manage_roles=True, ban_members=True)
    async def warn(self, context, member: discord.Member, *, reason = None):
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
            embed = get_warn_embed(self.settings.embeds["warn"], member, context.author, reason, self.bot.user.avatar_url)
        except:
            embed = None
            
        if embed != None:
            try:
                ban_channel = self.bot.get_channel(self.settings.channels["ban_warn"]) 
                await ban_channel.send(embed = embed)
            
            except:   
                await context.send(embed = embed)    

    
    @commands.command(
        name="warns",
        help="<member> : Le membre cible",
        description="Affiche le nombre cumulé d'avertissement d'un membre"
    )
    @commands.has_permissions(manage_roles=True, ban_members=True)
    async def warns(self, context, member: discord.Member):
        """
        Shows the number of warns a user has
        """
        print("Warns ... TODO")
        try:

            with open("resources/users.json") as data:
                users : dict = json.load(data)
            
            user = users[str(member.id)]

            warns_message = self.settings.messages["warns_message"]

            warns_message = warns_message.replace("{user}", member.name)
            warns_message = warns_message.replace("{warns}", str(user["warns"]))
            await context.send(warns_message)

        except:
            pass


    @commands.command(
        name="clear",
        aliases=["clean", "purge"],
        help="<number> : Le nombre de message à supprimer",
        description="Supprimer un nombre de messages dans un salon"
    )
    @commands.has_permissions(manage_messages=True)
    async def clear(self, context, number: int):
        """
        Delete a number of messages.
        """
        print("clear ... TODO")
        deleted = await context.channel.purge(limit = number + 1)
        await context.send(f"Deleted {len(deleted) - 1} message(s)", delete_after = 5)


    @commands.command(
        name="mute",
        help="<member> : Le membre cible",
        description="Mettre un membre Muet"
    )
    @commands.has_permissions(manage_roles = True)
    async def mute(self, context, member: discord.Member):
        """
        Mutes a user from the current server
        """
        print("Mute ... TODO")
        try:
            muted_role = context.guild.get_role(self.settings.muted_role)
            await member.add_roles(muted_role)
            muted_message = self.settings.messages["muted_message"]
            muted_message = muted_message.replace("{user}", member.mention)
            await context.send(muted_message)
        except:
            pass
    

    @commands.command(
        name="unmute",
        help="<member> : Le membre cible",
        description="Enleve le Muet pour un membre"
    )
    @commands.has_permissions(manage_roles = True)
    async def unmute(self, context, member: discord.Member):
        """
        Unmutes a user from the current server
        """
        print("Unmute ... TODO")
        try:
            muted_role = context.guild.get_role(self.settings.muted_role)
            await member.remove_roles(muted_role)
            muted_message = self.settings.messages["unmuted_message"]
            muted_message = muted_message.replace("{user}", member.mention)
            await context.send(muted_message)
        except:
            pass


    @commands.command(
        name="rules",
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
            try:
                with open("rules.txt") as file:
                    rules = file.read()
            except:
                rules = "NaN"
                
            embed = get_rules_embed(self.settings.embeds["rules"], rules, context.guild.name, context.guild.icon_url, self.bot.user.avatar_url)
        except Exception as e:
            print(e)
            embed = None

        if embed != None:
            await context.send(embed = embed)

  
def setup(bot):
    bot.add_cog(Moderation(bot))
