# -*- coding: utf-8 -*-

from init.bot import Bot
from discord.ext import commands
from init.settings import Settings
from utils.frontend import get_help_all_embed, get_help_cmd_embed


class Help(commands.Cog):
    def __init__(self, bot):

        if not isinstance(bot, Bot):
            print("Bot is not a discord Bot")
            exit(1)

        self.description = "Les commandes d'aides"
        self.bot = bot
        self.bot.remove_command("help")
        self.settings = Settings()

    @commands.command(
        name="help",
        help=
        "[command] : Si elle est donnée c'est que l'aide de la commande qui serait afficher sinon le catalogue de toutes les commandes",
        description="Affiche l'aide des commandes")
    async def help(self, context, command=None):
        """Shows this message."""
        if command is None:
            try:
                embed = get_help_all_embed(self.settings.embeds["help"],
                                           self.bot)
                await context.send(embed=embed)
            except:
                pass

            return

        get_commande = None
        for cmd in self.bot.commands:
            if cmd.name == command or command in cmd.aliases:
                get_commande = cmd
                break

        command = get_commande
        if not command is None:
            try:
                embed = get_help_cmd_embed(self.settings.embeds["help_cmd"],
                                           command, self.bot.user.avatar_url)
                await context.send(embed=embed)
            except:
                pass

            return

        await context.send("Cette commande n'existe pas")


def setup(bot):
    bot.add_cog(Help(bot))