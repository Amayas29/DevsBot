# -*- coding: utf-8 -*-

import asyncio
import discord
from   discord.ext   import commands
from   init.settings import Settings


class General(commands.Cog):
    
    def __init__(self, bot):

        if not isinstance(bot, commands.Bot):
            print("Bot is not a discord Bot")
            exit(1)

        self.bot = bot
        self.settings = Settings()
        

    @commands.command(name="poll")
    async def poll(self, context, *args):
        """
        Create a poll where members can vote
        """
        print("Poll ... TODO")

    
    @commands.command(name="art")
    async def art(self, context, choice : str, *args):
        """
        Show a text in a defined style
        """
        if choice not in self.settings.styles:
            choices = "\t" + "\n\t".join( (str(k) + " : Hello -> " + v["hello"] ) for k, v in self.settings.styles.items())
            await context.send("Not found try with : \n" + str(choices))
            return

        new_message = []
        for word in args:
            for char in word:

                if char.isalpha():
                    
                    if char. isupper():
                        index = ord(char) - ord("A")
                        maj_min = "maj"
                    else:
                        index = ord(char) - ord("a")
                        maj_min = "min"

                    if index < 0 or index > 25:
                        await context.send("Les caractères avec accents ne sont pas pris en comptes")
                        return

                    transformed = self.settings.styles[choice][maj_min][index]
                    new_message.append(transformed)
                else:
                    new_message.append(char)
            new_message.append(" ") 

        new_message = "".join(new_message)
        await context.send(new_message)

    
def setup(bot):
    bot.add_cog(General(bot))