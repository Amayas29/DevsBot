# -*- coding: utf-8 -*-

import traceback


async def add_reaction_verification(bot, payload):

    # todo :
    settings = None
    guild = bot.get_guild(payload.guild_id)
    try:
        if payload.message_id == settings.verification_message and payload.emoji.name == settings.verification_emoji:
            verified_role = guild.get_role(settings.verified_role)
            if verified_role in payload.member.roles:
                return

        for role in payload.member.roles:
            if role.is_integration() or role.is_bot_managed():
                return

        for role in settings.initial_roles:
            role_discord = guild.get_role(role)
            await payload.member.add_roles(role_discord)

    except:
        traceback.print_exc()


async def delete_reactions(member):

    try:
        # todo :
        settings = None
        server = member.guild
        verification = settings.channels["verification"]
        verification = server.get_channel(verification)
        verification_message = await verification.fetch_message(
            settings.verification_message)
        await verification_message.remove_reaction(settings.verification_emoji,
                                                   member)
    except:
        traceback.print_exc()
