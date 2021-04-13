# -*- coding: utf-8 -*-

from init.bot import Bot
from discord.ext import commands
from utils.frontend import get_rank_embed, generate_file_rank, get_top_embed
from database.users import get_level_exp, get_exp_level_guild
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

    @commands.command(
        name="top",
        help="",
        description="Affiche le TOP 10 des membres selon leurs niveaux")
    async def top(self, context):
        try:

            users = get_exp_level_guild(context.guild.id)
            users = filter(lambda x: x[1] != -1, users)

            users = sorted(
                users, key=lambda x: (x[1], x[2]), reverse=True)

            users_dict = {}
            for item in users:
                user = await self.bot.fetch_user(item[0])
                user = user.name if user is not None else item[0]
                users_dict[user] = [item[1], item[2]]

            embed = get_top_embed(
                users_dict, self.bot.config["footer"], self.bot.config["icon"])

            await context.send(embed=embed)
        except:
            traceback.print_exc()


def setup(bot):
    bot.add_cog(LevelSystem(bot))
