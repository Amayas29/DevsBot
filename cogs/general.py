# -*- coding: utf-8 -*-

import traceback
from init.bot import Bot
from discord.ext import commands
from utils.frontend import get_poll_embed, get_head_image, get_tail_image, get_gifs
from database.users import set_birth_date
import random
from datetime import datetime
import asyncio


class General(commands.Cog):

    def __init__(self, bot):

        if not isinstance(bot, Bot):
            print("Bot is not a discord Bot")
            exit(1)

        self.description = "Les commandes générales"
        self.bot = bot
        self.numbers = ("1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣",
                        "🔟")

    @commands.command(
        name="poll",
        help="<question> : La question du sondage.\n<options> : La liste des options pour le sondage"
        " (limitation à 10 options).\n\n *Si un des éléments est une phrase il faut mettre des \" \" autour*",
        description="Crée un sondage avec plusieurs options"
    )
    async def poll(self, context, question: str, *options):
        """
        Create a poll where members can vote
        """
        print("Poll ... TODO")
        try:
            if question == "" or question is None:
                return

            if len(options) < 1 or len(options) > 10:
                return

            liste = "\n".join([
                f"{self.numbers[i]} - {option}"
                for i, option in enumerate(options)
            ])

            try:
                embed = get_poll_embed(context.author, question, liste,
                                       self.bot.config["footer"], self.bot.config["icon"])
            except:
                embed = None

            if embed is None:
                return

            message_poll = await context.send(embed=embed)

            for emoji in self.numbers[:len(options)]:
                await message_poll.add_reaction(emoji)

            await message_poll.add_reaction("🤷")

        except:
            traceback.print_exc()

    @commands.command(
        name="flip",
        aliases=["pf"],
        help="",
        description="Jette une piece pour jouer à pile ou face"
    )
    async def flip(self, context):

        random.seed(datetime.now())
        coin = random.randint(1, 2)

        if coin == 1:  # Pile
            file = get_head_image()
            result = "Pile | Head"
        else:
            file = get_tail_image()
            result = "Face | Tail"

        await context.send(f" --  **{result}**  --", file=file)

    @commands.command(
        name="bottle",
        help="",
        description="Tire un membre au sort depuis une liste (Le jeu de la bouteille)"
    )
    async def bottle(self, context):
        print("Bottle ... TODO")

        await context.send("Le tirage commence dans 10 secondes | The draw will start in 10 seconds\n ⁣  ⁣⁣")
        await context.send("Envoyez **Moi** pour participer au tirage au sort | Send **Me** to enter in the draw\n ⁣  ⁣⁣")

        players = []

        def check(message):
            message_content = message.content.lower()
            return message.channel == context.message.channel and message.author not in players \
                and (message_content == "me" or message_content == "moi")

        try:
            while True:
                participation = await self.bot.wait_for("message", timeout=10, check=check)
                players.append(participation.author)
                await participation.delete()
                await context.send(f"**{participation.author.name}** : participe au tirage | participate in the draw\n ⁣  ")
        except:
            end = await context.send("Fin de la sélection des joueurs | End of the selection of players\n ⁣  ⁣⁣")
            await asyncio.sleep(1)

        if len(players) < 2:
            await context.send("ATTENTION ! Minimum 2 membres pour jouer | Minimum 2 members to play")
            return

        start = await context.send("Le tirage commence | The draw start ...")
        await end.delete()

        bottle = get_gifs("bottle_game")
        bottle_msg = await context.send(bottle)
        await asyncio.sleep(3)
        await bottle_msg.delete()
        await start.delete()

        user_selected = random.choice(players)
        await context.send(f">> Le perdant | The looser : **{user_selected.mention}**")

    @commands.command(
        name="birthdate",
        aliases=["bd", "naiss", "birth"],
        help="[date] : La date de naissance en format dd-mm-YYYY exemple : 29-05-2001",
        description="Changer la date de naissance de l'utilisateur"
    )
    async def birthdate(self, context, *, date):
        """
        Change the birthdate of the user
        """
        date = "".join(date)
        try:
            date_birth = datetime.strptime(date, "%d-%m-%Y")
        except:
            await context.send(f"⚠️ **{date}** : n'est pas une date valide | is not a valid date")
            return

        set_birth_date(context.author.id, context.guild.id, date)


def setup(bot):
    bot.add_cog(General(bot))
