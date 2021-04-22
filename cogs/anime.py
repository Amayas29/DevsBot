# -*- coding: utf-8 -*-

import requests
import traceback
from init.bot import Bot
from discord.ext import commands

QUOTE_URL = 'https://animechan.vercel.app/api/random'


class Anime(commands.Cog):

    def __init__(self, bot):

        if not isinstance(bot, Bot):
            print("Bot is not a discord Bot")
            exit(1)

        self.description = "Les commandes d'anime"
        self.bot = bot

    @commands.command(
        name="quote",
        help="",
        description="Envoie une citation d'un personnage d'anime random"
    )
    async def quote(self, context):
        """
        Send an anime character quote
        """
        data = requests.get(QUOTE_URL).json()

        anime = data['anime']
        character = data['character']
        quote = data['quote']

        await context.send(f"**Anime : {anime}** | __{character}__ : *\"{quote}\"*")


def setup(bot):
    bot.add_cog(Anime(bot))
