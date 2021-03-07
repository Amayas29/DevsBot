# -*- coding: utf-8 -*-

import asyncio
from datetime import time
from logging import error
import discord
from   discord.ext   import commands, tasks
from   init.settings import Settings


class Owner(commands.Cog):

    def __init__(self, bot):

        if not isinstance(bot, commands.Bot):
            print("Bot is not a discord Bot")
            exit(1)

        self.bot = bot
        self.settings = Settings()


    async def cog_check(self, context):
        return context.author.id in self.settings.owners


    @commands.command(name="ping", aliases=["test"])
    async def ping(self, context):
        """
        Check if the bot is alive
        """
        await context.message.delete()
        await context.send("Pong ... Bot fonctionnel", delete_after=5)


    @commands.command(name="shutdown")
    async def shutdown(self, context):
        """
        Make the bot shutdown
        """
        print("Shutdown ... TODO")


    @commands.command(name="setgame")
    async def set_game(self, context, game : str):
        """
        Change the game of the bot
        """
        print("Change game ... TODO")


    @commands.command(name="verif")
    async def verif(self, context, message_id : int):

        try:
            message_verif = await context.fetch_message(message_id)
            
            verification = self.bot.get_channel(self.settings.channels["verification"])
            bot_message = await verification.send("The verification system is in configuration ...\n **Added reaction emoji : ** \n - Please react with the emoji of your choice.\n\n *If no emoji is added after 5 min the command will be canceled*")
            
            def check(reaction, user):
                return user == context.message.author and reaction.message == bot_message

            try:
                reaction, _ = await self.bot.wait_for("reaction_add", timeout=300.0, check=check)
                await message_verif.add_reaction(reaction)
                self.settings.verification_message = message_verif.id
                self.settings.verification_emoji = str(reaction.emoji)
                self.settings.refresh_data()
            except Exception as e:
                print(e)
                pass
            finally:
                await bot_message.delete()

        except Exception as e:
            print(e)
        finally:
            await context.message.delete()


def setup(bot):
    bot.add_cog(Owner(bot))