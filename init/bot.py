# -*- coding: utf-8 -*-

import random
import discord
from   discord.ext   import commands, tasks
from   init.settings import Settings


class Bot(commands.Bot):

    def __init__(self, *args, prefix=None, **kwargs):
        self.settings = Settings()
        intents = discord.Intents.default()
        prefix = self.settings.prefix
        intents.members = True
        intents.presences = True
        super().__init__(*args, command_prefix=prefix, prefix=prefix, intents=intents, **kwargs)
    

    async def on_message(self, message: discord.Message):
        print("message ... TODO")
    
        message_lower = message.content.lower()
        for word in self.settings.forbidden_words:
            if word in message_lower:
                # TODO WARN
                await message.channel.send("No bro ad qar ara aken", delete_after = 10)
                await message.delete()
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