from asyncio.events import AbstractEventLoopPolicy
import discord
from discord.ext import commands
import asyncio
import random

from discord.ext.commands.core import check
from discord.gateway import DiscordWebSocket

inte = discord.Intents.default()
inte.members = True
inte.presences = True
# Creation du client (bot)

bot = commands.Bot(command_prefix = "?", intents=inte, description = "Bot de Amayas pour le serveur Devs")

@bot.event
async def on_ready():
    print("Je suis en execution ! ")

@bot.command()
async def serverInfo(ctx):
    server = ctx.guild
    number_txt_channels = len(server.text_channels)
    number_voc_channels = len(server.voice_channels)
    server_description = server.description
    number_members = server.member_count

    message = f"Le serveur ***{server.name}***  contient *{number_members}* membres. \n\n"

    if server_description == None :
        server_description = " - *Ce serveur est un lieu de partage entre de superbe personnes sur plusieurs thématiques principalement l'informatique*  :desktop:"

    message += f"{server_description} \n\n"

    message += f"    **>>** Ce serveur possède {number_txt_channels} salons textuels ainsi que {number_voc_channels} salons vocaux"

    await ctx.send(message)
    

@bot.command()
async def say(ctx, *args):
    await ctx.send(" ".join(args))


@bot.command()
async def art(ctx, *args):
    styles = {
        0:["𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ", "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫", "ℍ𝕖𝕝𝕝𝕠"],
        1: ["𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴", "𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏", "𝐻𝑒𝓁𝓁𝑜"]
    }
    choice_style = "\n\t".join([ str(i) + ") Hello -> " + str(styles[i][2]) for i in range(len(styles))])
    usage = f" >> Usage ?art <numero> <texte> \n\n - <numero> : Le numéro du style de l'ecriture \n\n\t *Voici les styles existants* : \n\t{choice_style} \n\n - <texte> : Le texte a écrire"
    
    if len(args) < 2:
        await ctx.send(f"***Manque de paramètres.***\n\n{usage}")
        return
    
    choice = args[0]
    if choice.isdigit():
       choice = int(choice)

    if choice not in styles:
        await ctx.send(f"***Style introuvable.***\n\n{usage}")
        return

    new_msg = []
    for i in range(1, len(args)):
        for char in args[i]:
            if char.isalpha():

                maj = 0
                if char. isupper():
                    index = ord(char) - ord("A")
                else:
                    index = ord(char) - ord("a")
                    maj = 1

                if index < 0 or index > 25:
                    await ctx.send("Les caractères avec accents ne sont pas pris en comptes")
                    return

                transformed = styles[choice][maj][index]
                new_msg.append(transformed)
            else:
                new_msg.append(char)
        new_msg.append(" ")
    
    await ctx.send("".join(new_msg))

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx : commands.Context, number = 0):
    deleted = await ctx.channel.purge(limit=number)
    message = await ctx.send('Deleted {} message(s)'.format(len(deleted)))
    await asyncio.sleep(5)
    await message.delete()
    return


@bot.command()
async def kick(ctx, user: discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.kick(user, reason = reason)
    await ctx.send(f"{user} à été kick")


@bot.command()
async def ban(ctx, user: discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.ban(user, reason = reason)
    await ctx.send(f"{user} à été ban pour la raison suivante : {reason}")

@bot.event
async def on_command_error(ctx, err):
    if isinstance(err, commands.MissingPermissions):
        await ctx.send("Tu manque de permer mon frer")
    print("Err", err)

@bot.command()
async def unban(ctx, user, *reason):
    reason = " ".join(reason)
    user_name, user_id = user.split('#')
    banned_users = await ctx.guild.bans()

    for usban in banned_users:
        if usban.user.name == user_name and usban.user.discriminator == user_id:
            await ctx.guild.unban(usban.user, reason = reason)
            await ctx.send(f"{user} à été unban")
            return
        
    await ctx.send(f"{user} n'est pas dans la liste des bans")

@bot.command()
async def cuisiner(ctx):
    await ctx.send("Hem ?")

    def check_message(message):
        return message.author == ctx.message.author and ctx.message.channel == message.channel 

    try:
        recette = await bot.wait_for("message", timeout = 10, check = check_message)
    except:
        return

    message = await ctx.send(f"{recette.content}")
    await message.add_reaction("🟢")
    await message.add_reaction("🥇")

    def check_reaction(reaction, user):
        return ctx.message.author == user and message.id == reaction.message.id and ( str(reaction.emoji) == "🟢" or str(reaction.emoji) == "🥇" )

    try:
        reaction, user = await bot.wait_for("reaction_add", timeout = 10, check = check_reaction)

        if reaction.emoji == "🟢":
            await ctx.send("Verte")
        else:
            await ctx.send("Jaune")
    except:
        await ctx.send("Annule")

@bot.command()
async def roulette(ctx):
    await ctx.send("Yeh envoye h")

    players = []
    def check(msg):
        return msg.channel == ctx.message.channel and msg.author not in players and msg.content == "h"
    
    try:
        while True:
            part = await bot.wait_for("message", timeout=10, check=check)
            players.append(part.author)
            await ctx.send(f"{part.author.name} participe")
    except:
        print()
    
    g = ["b", "k", "r", "m", "g"]
    await ctx.send("Dans 3")
    await asyncio.sleep(1)
    await ctx.send("2")
    await asyncio.sleep(1)
    await ctx.send("1")
    await asyncio.sleep(1)
    
    l = random.choice(players)
    p = random.choice(g)
    await ctx.send(f"La personne qui a ganger un {p} est ...")
    await asyncio.sleep(1)
    await ctx.send("**" +l.name+"**")


@bot.group()
@commands.guild_only()
# @commands.has_permissions(ban_members=True)
async def find(ctx):
    """ Finds a user within your search term """

    if ctx.invoked_subcommand is None:
        await ctx.send_help(str(ctx.command))

@find.command(name="username", aliases=["name"])
async def find_name( ctx, *, search: str):

    loop = ""
    for member in ctx.guild.members: 
        if search.lower() in member.name.lower() and not member.bot:
            loop += "\t - " + str(member.name) + "\n"


    if loop != "":
        loop = "Les membres du seveur trouvés : \n" + str(loop)

    await ctx.send(f"{loop}")


# Le lancer avec son token
bot.run("ODE1NjM0NDc5NDEwMDUzMTUw.YDvQzQ.b-5KnH6e_nSPK1qd3ojkXZybE5I")