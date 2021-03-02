# -*- coding: utf-8 -*-

import asyncio
import discord
from   discord.ext import commands

import json

class General(commands.Cog):
    
    def __init__(self, bot):

        if not isinstance(bot, commands.Bot):
            print("Bot is not a discord Bot")
            exit(1)

        self.bot = bot

        try:
            with open(f"resources/styles.json", encoding='utf8') as data:
                self.styles = json.load(data)
        except FileNotFoundError :
            self.styles = {}


    @commands.command(name="myinfo")
    async def my_info(self, context):
        """
        Get the user info
        """
        print("My info ... TODO")


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
        if choice not in self.styles:
            choices = "\t" + "\n\t".join( (str(k) + " : Hello -> " + v["hello"] ) for k, v in self.styles.items())
            await context.send("Not found try with : \n" + str(choices))
            return

        new_msg = []
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

                    transformed = self.styles[choice][maj_min][index]
                    new_msg.append(transformed)
                else:
                    new_msg.append(char)
            new_msg.append(" ") 

        new_msg = "".join(new_msg)
        await context.send(new_msg)

    
def setup(bot):
    bot.add_cog(General(bot))