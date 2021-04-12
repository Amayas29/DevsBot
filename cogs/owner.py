# -*- coding: utf-8 -*-

import discord
from init.bot import Bot
from discord.ext import commands
from utils.games import dump_games


class Owner(commands.Cog):
    def __init__(self, bot):

        if not isinstance(bot, Bot):
            print("Bot is not a discord Bot")
            exit(1)

        self.description = "Les commandes du propriétaire, elles sont dédiées qu'au propriétaire"
        self.bot = bot

    async def cog_check(self, context):
        return context.author.id in self.bot.config["owners"]

    @commands.command(name="ping",
                      aliases=["test"],
                      help="",
                      description="Test si le bot est fonctionnel")
    async def ping(self, context):
        """
        Check if the bot is alive
        """
        await context.message.delete()
        await context.send("Pong ... Bot fonctionnel", delete_after=5)

    @commands.command(name="shutdown",
                      aliases=["quit", "exit", "logout"],
                      help="",
                      description="Éteindre le bot")
    async def shutdown(self, context):
        """
        Make the bot shutdown
        """
        print("Shutdown ... TODO")
        await context.message.add_reaction("👋")
        await context.send("Good bye !")
        await self.bot.close()

    @commands.command(name="setgame",
                      help="<game> : La nouvelle activité",
                      description="Change l'activité du bot")
    async def set_game(self, context, *, game):
        """
        Change the game of the bot
        """
        print("Change game ... TODO")
        try:
            game = "".join(game)
            self.bot.games.append(game)
            dump_games(self.bot.games)
            self.bot.game = game
            game = discord.Game(self.bot.game)
            await self.bot.change_presence(status=discord.Status.online,
                                           activity=game)
        except:
            pass


def setup(bot):
    bot.add_cog(Owner(bot))
