# -*- coding: utf-8 -*-

from init.bot import Bot
from discord.ext import commands
from utils.frontend import get_help_cmd_embed, get_help_all_embed
import traceback


class Help(commands.Cog):
    def __init__(self, bot):

        if not isinstance(bot, Bot):
            print("Bot is not a discord Bot")
            exit(1)

        self.description = "Les commandes d'aides"
        self.bot = bot
        self.bot.remove_command("help")

    @commands.command(
        name="help",
        help="[command] : Si elle est donnée c'est que l'aide de la commande qui serait afficher sinon le catalogue de toutes les commandes",
        description="Affiche l'aide des commandes")
    async def help(self, context, command=None):
        """
        Shows the help embed.
        """

        print("help ... TODO")
        if command is None:
            try:
                cogs_dict = self.get_cogs_dict()

                embed = get_help_all_embed(
                    self.bot.config["name"], cogs_dict, self.bot.config["footer"], self.bot.config["icon"])

                await context.send(embed=embed)
            except:
                traceback.print_exc()

            return

        get_commande = None
        for cmd in self.bot.commands:
            if cmd.name == command or command in cmd.aliases:
                get_commande = cmd
                break

        command = get_commande
        if command is not None:

            name_aliases = "|".join([str(command), *command.aliases])
            params = []
            for key, value in command.params.items():
                if key not in ("self", "context"):
                    params.append(f"[{key}]" if "None" in
                                  str(value) else f"<{key}>")

            params = " ".join(params)

            syntaxe = f"`{self.bot.prefix}{name_aliases}"
            if params != "":
                syntaxe += f" {params}"
            syntaxe += "`"

            help = f"{cmd.description}\n\n{cmd.help}"

            try:
                embed = get_help_cmd_embed(
                    command.name, self.bot.config["name"], name_aliases, syntaxe, help, self.bot.config["footer"], self.bot.config["icon"])

                await context.send(embed=embed)
            except:
                pass

            return

        await context.send("Cette commande n'existe pas")

    def get_cogs_dict(self):
        dict_cogs = {}
        cogs = [c for c in self.bot.cogs.keys()]
        cogs.remove("Events")

        for cog in cogs:
            cogbot = self.bot.get_cog(cog)
            list_commands = f"\n*Description générale : {cogbot.description}*\n\n⁣ ⁣  ⁣⁣"

            for cmd in cogbot.walk_commands():

                if cmd.hidden or cmd.parent != None:
                    continue

                list_commands += f"**{cmd.name}** - *{cmd.description}* \n⁣ ⁣  ⁣"

            if cog != cogs[-1]:
                list_commands += "\n ⁣  ⁣"

            dict_cogs[cog] = list_commands

        return dict_cogs


def setup(bot):
    bot.add_cog(Help(bot))
