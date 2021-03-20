# -*- coding: utf-8 -*-

from init.bot import Bot
from discord.ext import commands


class Owner(commands.Cog):
    def __init__(self, bot):

        if not isinstance(bot, Bot):
            print("Bot is not a discord Bot")
            exit(1)

        self.description = "Les commandes du propriétaire, elles sont dédiées qu'au propriétaire"
        self.bot = bot

    async def cog_check(self, context):
        return context.author.id in self.bot.config["owners"]

    @commands.command(name="ping",
                      aliases=["test"],
                      help="",
                      description="Test si le bot est fonctionnel")
    async def ping(self, context):
        """
        Check if the bot is alive
        """
        await context.message.delete()
        await context.send("Pong ... Bot fonctionnel", delete_after=5)

    @commands.command(name="shutdown",
                      aliases=["quit", "exit", "logout"],
                      help="",
                      description="Éteindre le bot")
    async def shutdown(self, context):
        """
        Make the bot shutdown
        """
        print("Shutdown ... TODO")
        await context.message.add_reaction("👋")
        await context.send("Good bye !")
        await self.bot.close()

    # @commands.command(name="setgame",
    #                   help="<game> : La nouvelle activité",
    #                   description="Change l'activité du bot")
    # async def set_game(self, context, *, game):
    #     """
    #     Change the game of the bot
    #     """
    #     print("Change game ... TODO")
    #     try:
    #         game = "".join(game)
    #         self.settings.game_status.append(game)
    #         self.settings.refresh_data()
    #         self.bot.game = game
    #         game = discord.Game(self.bot.game)
    #         await self.bot.change_presence(status=discord.Status.online,
    #                                        activity=game)
    #     except:
    #         pass

    # @commands.command(name="verif",
    #                   help="<message_id> : L'identifiant du message",
    #                   description="Crée le message de vérificarion du serveur")
    # async def verif(self, context, message_id: int):

    #     try:
    #         message_verif = await context.fetch_message(message_id)

    #         verification = self.bot.get_channel(
    #             self.settings.channels["verification"])
    #         bot_message = await verification.send(
    #             "The verification system is in configuration ...\n **Added reaction emoji : ** \n - Please react with the emoji of your choice.\n\n *If no emoji is added after 5 min the command will be canceled*"
    #         )

    #         def check(reaction, user):
    #             return user == context.message.author and reaction.message == bot_message

    #         try:
    #             reaction, _ = await self.bot.wait_for("reaction_add",
    #                                                   timeout=300.0,
    #                                                   check=check)
    #             await message_verif.add_reaction(reaction)
    #             self.settings.verification_message = message_verif.id
    #             self.settings.verification_emoji = str(reaction.emoji)
    #             self.settings.refresh_data()
    #         except Exception as e:
    #             print(e)
    #             pass
    #         finally:
    #             await bot_message.delete()

    #     except Exception as e:
    #         print(e)
    #     finally:
    #         await context.message.delete()


def setup(bot):
    bot.add_cog(Owner(bot))
