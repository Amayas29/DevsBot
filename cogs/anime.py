# -*- coding: utf-8 -*-

from init.bot import Bot
from discord.ext import commands
from utils.frontend import get_anime_embed, get_character_embed
import traceback
import os
import requests

JIKAN_SEARCH_URL = "https://jikan1.p.rapidapi.com/search/"


class Anime(commands.Cog):

    def __init__(self, bot):

        if not isinstance(bot, Bot):
            print("Bot is not a discord Bot")
            exit(1)

        self.RAPID_API_KEY = os.getenv("RAPID_API_KEY")
        self.description = "Les commandes d'animés"
        self.bot = bot

    def search(self, type, name):
        """
            Faire une recherche d'un anime ou d'un character et retourne son id
        """

        if type != "anime" and type != "character":
            raise ValueError("Invalid type")

        url = f"{JIKAN_SEARCH_URL}{type}"
        querystring = {"q": name}

        headers = {
            'x-rapidapi-key': self.RAPID_API_KEY,
            'x-rapidapi-host': "jikan1.p.rapidapi.com"
        }

        response = requests.request(
            "GET", url, headers=headers, params=querystring)

        if not response.ok:
            raise Exception("Not found")

        results = response.json()["results"]

        if results == []:
            raise Exception("Not found")

        result = results[0]

        if type == "anime":
            return get_anime_embed(result, self.bot.config["footer"], self.bot.config["icon"])

        return get_character_embed(result, self.bot.config["footer"], self.bot.config["icon"])

    @commands.command(
        name="anime",
        aliases=["a"],
        help="<name> : Le nom de l'anime à rechercher",
        description="Permet de rechercher un anime")
    async def anime(self, context, *name):
        try:
            pass
        except:
            traceback.print_exc()

    @commands.command(
        name="character",
        aliases=["c"],
        help="<name> : Le nom du perso à rechercher",
        description="Permet de rechercher un perso d'anime")
    async def character(self, context, *name):
        try:
            name = " ".join(name)
            character_embed = self.search("character", name)

            await context.send(embed=character_embed)
        except:
            traceback.print_exc()


def setup(bot):
    bot.add_cog(Anime(bot))
