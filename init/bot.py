# -*- coding: utf-8 -*-

import random
import discord
from discord.ext import commands, tasks
from database.servers import get_servers
from database.users import add_user, set_exp, set_level, get_level_exp, get_users_birthdate
import json
from utils.games import load_games
from copy import deepcopy
import traceback
from pathlib import Path
from utils.levels import update_user
from utils.frontend import get_levelup_message, get_birthdate_embed, get_leveldown_message


CONFIG_PATH = f"{str(Path(__file__).parent.parent)}/config.json"


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

    async def on_message(self, message: discord.Message):

        try:
            self.prefix = self.servers[str(message.guild.id)]["prefix"]
            self.command_prefix = self.prefix
        except:
            traceback.print_exc()

        if message.author != self.user and isinstance(message.channel,
                                                      discord.DMChannel):
            await message.channel.send("Hi ! I am a bot created by Amayas")
            return

        moderators_roles = self.servers[str(
            message.guild.id)]["moderators_roles"]

        admin = False

        for role in message.author.roles:
            if role.is_integration() or role.is_bot_managed():
                await self.process_commands(message)
                return

            if role.id in moderators_roles:
                admin = True

        print("message ... TODO")
        if not admin:
            try:
                message_lower = message.content.lower()
                for word in self.servers[str(message.guild.id)]["forbidden_words"]:
                    if word in message_lower:

                        await message.channel.send("🚫 - You can't send this word | Vous ne pouvez pas envoyer ce mot", delete_after=10)
                        await message.delete()
                        if update_user(message.author.id, message.guild.id, -20) == -1:
                            level, _ = get_level_exp(
                                message.author.id, message.guild.id)

                            lvldwn = get_leveldown_message(
                                message.author, str(level))

                            if lvldwn is not None:
                                try:
                                    lvlup_channel = self.get_channel(
                                        self.servers[str(message.guild.id)]["channels"]["levels"])

                                    await lvlup_channel.send(lvldwn)

                                except:
                                    traceback.print_exc()
                                    await message.channel.send(lvldwn)

                        return
            except:
                traceback.print_exc()

        if update_user(message.author.id, message.guild.id) == 1:

            level, _ = get_level_exp(message.author.id, message.guild.id)
            lvlup = get_levelup_message(message.author, str(level))

            if lvlup is not None:
                try:
                    lvlup_channel = self.get_channel(
                        self.servers[str(message.guild.id)]["channels"]["levels"])

                    await lvlup_channel.send(lvlup)

                except:
                    traceback.print_exc()
                    await message.channel.send(lvlup)

        await self.process_commands(message)

    @tasks.loop(hours=5)
    async def status(self):
        print("Status ...")
        games = deepcopy(self.games)

        if self.game == None:
            self.game = random.choice(games)

        elif len(games) > 1:
            games.remove(self.game)
            self.game = random.choice(games)

        game = discord.Game(self.game)
        await self.change_presence(status=discord.Status.online, activity=game)

    @tasks.loop(hours=24)
    async def birthdays(self):
        print("Birthdays ...")
        for server in self.servers:
            try:
                birthdates_channel = self.servers[server]["channels"]["birthdays"]

                if birthdates_channel is None:
                    continue

                birthdates_channel = await self.fetch_channel(birthdates_channel)

                users = get_users_birthdate(server)

                for user_id in users:
                    user = await self.fetch_user(user_id[0])

                    embed = get_birthdate_embed(
                        user, user_id[1], self.config["footer"], self.config["icon"])

                    await birthdates_channel.send(embed=embed)
            except:
                continue

    async def on_ready(self):
        """
        When the bot is activated
        """
        print("Ready ... TODO")

        try:
            with open(CONFIG_PATH, "r") as f:
                self.config = json.load(f)

            self.config["icon"] = str(self.user.avatar_url)

            with open(CONFIG_PATH, "w") as f:
                json.dump(self.config, f)
        except:
            traceback.print_exc()

        self.status.start()
        self.birthdays.start()

        owners = self.config["owners"]

        for guild in self.guilds:

            ignored_roles_levels = self.servers[str(
                guild.id)]["ignored_roles_levels"]

            for member in guild.members:

                bot = list(filter(lambda role: role.is_integration()
                           or role.is_bot_managed(), member.roles))
                if bot:
                    continue

                add_user(member.id, guild.id)

                if member.id in ignored_roles_levels or member.id in owners:
                    set_exp(member.id, guild.id, -1)
                    set_level(member.id, guild.id, -1)
                    continue

                level, _ = get_level_exp(member.id, guild.id)
                if level == -1:
                    set_exp(member.id, guild.id, 0)
                    set_level(member.id, guild.id, 1)
