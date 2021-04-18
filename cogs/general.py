# -*- coding: utf-8 -*-

import traceback
from init.bot import Bot
from discord.ext import commands
from utils.frontend import get_poll_embed
import random
from datetime import datetime
from utils.frontend import get_head_image, get_tail_image


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
        help=None,
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


def setup(bot):
    bot.add_cog(General(bot))
