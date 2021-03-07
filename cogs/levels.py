# -*- coding: utf-8 -*-

from   discord.ext    import commands
from   init.settings  import Settings
from   utils.frontend import get_file_rank, get_level_embed, get_top_embed


class LevelSystem(commands.Cog):

    def __init__(self, bot):

        if not isinstance(bot, commands.Bot):
            print("Bot is not a discord Bot")
            exit(1)

        self.description = "Les commandes de niveaux"
        self.bot = bot
        self.settings = Settings()


    @commands.command(
        name="rank",
        help="",
        description="Affiche la carte niveau de l'utilisateur de la commande"
    )
    async def rank(self, context):
        try:
            file = get_file_rank(context.author)
            embed = get_level_embed(self.settings.embeds["rank"], context.author, self.bot.user.avatar_url)

            if file == None or embed == None:
                return

            await context.send(embed = embed, file=file)
        except:
            pass


    @commands.command(
        name="top",
        help="",
        description="Affiche le haut du classement des membres selon leurs niveaux"
    )
    async def top(self, context):
        try:

            embed = await get_top_embed(self.settings.embeds["top"], self.bot)
            if embed == None:
                return
            
            await context.send(embed = embed)
        except:
            pass
    

def setup(bot):
    bot.add_cog(LevelSystem(bot))