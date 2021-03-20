# -*- coding: utf-8 -*-

import random
import discord
from discord.ext import commands, tasks
from database.servers import get_servers, create_server
from database.users import insert_unique
import json
from utils.games import load_games, dump_games
from copy import deepcopy as dp
class Bot(commands.Bot):

    def __init__(self, *args, prefix=None, **kwargs):

        intents = discord.Intents.default()
        prefix = "!"
        intents.members = True
        intents.presences = True
        self.game = None
        super().__init__(*args,
                         command_prefix=prefix,
                         prefix=prefix,
                         intents=intents,
                         **kwargs)
        self.servers = get_servers()
        self.games = load_games()

        try:
            with open("config.json", "r") as f:
                self.config = json.load(f)

            self.config["icon"] = str(self.user.avatar_url)

            with open("config.json", "w") as f:
                json.dump(self.config, f)
        except:
            pass

    async def on_message(self, message: discord.Message):

        try:
            self.prefix = self.servers[str(message.guild.id)]["prefix"]
            self.command_prefix = self.prefix
        except:
            pass

        if message.author != self.user and isinstance(message.channel,
                                                      discord.DMChannel):
            await message.channel.send("Hi ! I am a bot created by Amayas")
            return

        print("message ... TODO")
        try:
            message_lower = message.content.lower()
            for word in self.servers[str(message.guild.id)]["forbidden_words"]:
                if word in message_lower:
                    await message.channel.send("No bro .. TODO", delete_after=10)
                    await message.delete()
                    return
        except:
            pass

        # try:
        #     set_exp(message.author, 5)
        #     lvup, level = level_up(message.author)
        #     if lvup:
        #         levels_channel = self.get_channel(
        #             self.settings.channels["levels"])
        #         message_up = dp(self.settings.messages["level_up_message"])
        #         message_up = message_up.replace("{user}",
        #                                         message.author.mention)
        #         message_up = message_up.replace("{level}", str(level))
        #         await levels_channel.send(message_up)
        # except Exception as e:
        #     pass

        await self.process_commands(message)

    async def on_message_edit(self, after, before):
        return

    @tasks.loop(hours=5)
    async def status(self):
        games = dp(self.games)

        if self.game == None:
            self.game = random.choice(games)

        elif len(games) > 1:
            games.remove(self.game)
            self.game = random.choice(games)

        game = discord.Game(self.game)
        await self.change_presence(status=discord.Status.online, activity=game)

    # @tasks.loop(hours=24)
    # async def birthdays(self):

    #     try:
    #         birthday_channel = await self.fetch_channel(
    #             self.settings.channels["birthdays"])
    #         users = get_users_birthday()
    #         for id_age in users:
    #             try:
    #                 user = await self.fetch_user(int(id_age[0]))
    #                 embed = get_birthday_embed(
    #                     self.settings.embeds["birthday"], user, id_age[1],
    #                     self.user.avatar_url)
    #                 await birthday_channel.send(embed=embed)
    #             except:
    #                 continue
    #     except:
    #         pass

    async def on_ready(self):
        """
        When the bot is activated
        """
        print("Ready ... TODO")
        self.status.start()
        # self.birthdays.start()

        for guild in self.guilds:
            for member in guild.members:
                bot = list(filter(lambda role: role.is_integration() or role.is_bot_managed(), member.roles))
                if bot != []:
                    continue
                insert_unique(member.id, guild.id)
