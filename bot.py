# -*- coding: utf-8 -*-

import random
import discord
from   discord.ext       import commands, tasks
from   settings          import Settings


class Bot(commands.Bot):

    def __init__(self, *args, prefix=None, **kwargs):
        intents = discord.Intents.default()
        self.prefix = prefix
        intents.members = True
        intents.presences = True
        super().__init__(*args, intents=intents, **kwargs)
        self.settings = Settings()


    async def on_message(self, message):
        print("message ... TODO")
        if not self.is_ready():
            return

        await self.process_commands(message)


    async def on_message_edit(self, after, befor):
        return


    @tasks.loop(hours=5)
    async def status(self):
        game = discord.Game(random.choice(self.settings.game_status))
        await self.change_presence(status = discord.Status.online, activity = game)


    async def on_ready(self):
        """
        When the bot is activated
        """
        print("Ready ... TODO")
        self.status.start()