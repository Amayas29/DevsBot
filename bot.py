# -*- coding: utf-8 -*-

import asyncio
import discord
from   discord.ext import commands


class Bot(commands.Bot):

    def __init__(self, *args, prefix=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = prefix
        self.intents = discord.Intents.default()
        self.intents.members = True
        self.intents.presences = True


    async def on_message(self, msg):
        print("message ... TODO")
        if not self.is_ready():
            return
        await self.process_commands(msg)


    async def on_ready(self):
        """
        When the bot is activated
        """
        print("Ready ... TODO")