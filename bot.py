# -*- coding: utf-8 -*-

import asyncio
import discord
from   discord.ext import commands
import json

class Bot(commands.Bot):

    def __init__(self, *args, prefix=None, **kwargs):
        intents = discord.Intents.default()
        self.prefix = prefix
        intents.members = True
        intents.presences = True
        super().__init__(*args, intents=intents, **kwargs)

        try:
            with open(f"resources/forbidden.json", encoding='utf8') as data:
                self.forbidden = json.load(data)
        except FileNotFoundError :
                self.forbidden = {}


    async def on_message(self, message):
        print("message ... TODO")
        if not self.is_ready():
            return

        forbidden_word = self.forbidden["words"]
        message_content = message.content.lower()
        for word in forbidden_word:
            if word in message_content:
                await message.channel.send("Attention mot interdit", delete_after = 5)
                await message.delete()
                return

        await self.process_commands(message)


    async def on_message_edit(self, after, befor):

        forbidden_word = self.forbidden["words"]
        message_content = befor.content.lower()
        for word in forbidden_word:
            if word in message_content:
                await after.channel.send("Attention mot interdit", delete_after=5)
                await after.delete()
                return

    async def on_ready(self):
        """
        When the bot is activated
        """
        print("Ready ... TODO")