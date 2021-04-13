# -*- coding: utf-8 -*-

from init.bot import Bot
from discord.ext import commands
from utils.frontend import get_rank_embed, generate_file_rank
from database.users import get_level_exp
import traceback


class LevelSystem(commands.Cog):
    def __init__(self, bot):

        if not isinstance(bot, Bot):
            print("Bot is not a discord Bot")
            exit(1)

        self.description = "Les commandes de niveaux"
        self.bot = bot

    @commands.command(name="rank",
                      help="",
                      description="Affiche la carte niveau de l'utilisateur")
    async def rank(self, context):

        level, exp = get_level_exp(context.author.id, context.guild.id)

        try:
            file = generate_file_rank(context.author, context.guild)

            embed = get_rank_embed(
                context.author, level, exp, self.bot.config["footer"], self.bot.config["icon"])

            await context.send(embed=embed, file=file)
        except:
            traceback.print_exc()

            pass

    # @commands.command(
    #     name="top",
    #     help="",
    #     description="Affiche le TOP 10 des membres selon leurs niveaux")
    # async def top(self, context):
    #     try:
    #         embed = await get_top_embed(self.settings.embeds["top"], self.bot)
    #         if embed == None:
    #             return

    #         await context.send(embed=embed)
    #     except:
    #         pass


def setup(bot):
    bot.add_cog(LevelSystem(bot))
