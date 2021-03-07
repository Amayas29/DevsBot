# -*- coding: utf-8 -*-

from   init.settings import Settings


settings = Settings()


async def add_reaction_verification(bot, payload):

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
            pass


async def delete_reactions(member):
        
        try:
            server = member.guild
            verification = settings.channels["verification"]
            verification = server.get_channel(verification)
            verification_message = await verification.fetch_message(settings.verification_message)
            await verification_message.remove_reaction(settings.verification_emoji, member)
        except Exception as e:
            print(e)