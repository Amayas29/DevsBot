# -*- coding: utf-8 -*-

from operator import index
import random
import re
import discord
import json
from   discord.ext   import commands, tasks
from   init.settings import Settings
from   copy          import deepcopy as dp
from   utils.levels  import update_users, set_exp, level_up


class Bot(commands.Bot):

    def __init__(self, *args, prefix=None, **kwargs):
        self.settings = Settings()
        intents = discord.Intents.default()
        prefix = self.settings.prefix
        intents.members = True
        intents.presences = True
        self.game = None
        super().__init__(*args, command_prefix=prefix, prefix=prefix, intents=intents, **kwargs)
    

    async def on_message(self, message: discord.Message):

        if message.author != self.user and isinstance(message.channel, discord.DMChannel):
            await message.channel.send("Hi ! I am a bot created by Amayas")
            return
            
        print("message ... TODO")

        message_lower = message.content.lower()
        for word in self.settings.forbidden_words:
            if word in message_lower:
                await message.channel.send("No bro .. TODO", delete_after = 10)
                await message.delete()
                return

        try:
            set_exp(message.author, 5)
            lvup, level = level_up(message.author)
            if lvup:
                levels_channel = self.get_channel(self.settings.channels["levels"])
                message_up = dp(self.settings.level_up_message)
                message_up = message_up.replace("{user}", message.author.mention)
                message_up = message_up.replace("{level}", str(level))
                await levels_channel.send(message_up)
        except Exception as e:
            pass

        await self.process_commands(message)


    async def on_message_edit(self, after, befor):
        return


    @tasks.loop(hours=5)
    async def status(self):

        games = dp(self.settings.game_status)

        if self.game == None:
            self.game = games[0]

        elif len(games) > 1:
            games.remove(self.game)
            self.game = random.choice(games)
        
        game = discord.Game(self.game)
        await self.change_presence(status = discord.Status.online, activity = game)


    async def on_ready(self):
        """
        When the bot is activated
        """
        print("Ready ... TODO")
        self.status.start()

        liste = []
        for member in self.get_all_members():

            add = True
            for role in member.roles:
                if role.is_integration() or role.is_bot_managed():
                    add = False
                    break
                
            if add:
                liste.append(member)

        update_users(False, liste)