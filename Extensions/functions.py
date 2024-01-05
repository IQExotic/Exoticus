import lightbulb
import hikari
from hikari import components
from datetime import datetime, timedelta
from .db import *

plugin = lightbulb.Plugin("functions")


async def error_message(error_code, error):
    channel_id = 1136345878681108510
    channel = await plugin.bot.rest.fetch_channel(channel_id)
    content = f"**{error_code}**\n\n'''{error}'''"
    try:
        await channel.send(content)  # type: ignore
        return
    except Exception as e:
        print(f"Error: {e}")


async def fetch_user_from_id(id):
    user = None
    try:
        user = await plugin.bot.rest.fetch_user(id)
    except Exception as e:
        await error_message("Fehler B-01", e)
    return user


async def interaction_response(event, content, component=None):
    if component != None:
        try:
            await event.interaction.create_initial_response(
                content=content,
                components=[component],
                flags=64,
                response_type=hikari.ResponseType.MESSAGE_CREATE
            )
        except Exception as e:
            await error_message("Fehler B-10", e)
            print(f"Error: {e}")
    elif component == None:
        try:
            await event.interaction.create_initial_response(
                content=content,
                flags=64,
                response_type=hikari.ResponseType.MESSAGE_CREATE
            )
        except Exception as e:
            await error_message("Fehler B-10", e)
            print(f"Error: {e}")


async def user_respond(ctx, content):
    try:
        await ctx.respond(content)
    except Exception as e:
        await error_message("Fehler B-03", e)
    return


async def create_new_text_channel(guild_id, channel_name, combined_overwrites, category_id, description):
    channel = None
    try:
        channel = await plugin.bot.rest.create_guild_text_channel(
            guild_id,
            name=channel_name,
            permission_overwrites=combined_overwrites,
            category=category_id,
            topic=description
        )
    except Exception as e:
        await error_message("Fehler B-07", e)
    return channel


async def fetch_channel_from_id(id):
    channel = None
    try:
        channel = await plugin.bot.rest.fetch_channel(id)
    except Exception as e:
        await error_message("Fehler B-?", e)
    return channel


async def combine_category_permissions(user, category):
    # Get the permission overwrites of the category
    category_overwrites = category.permission_overwrites.values()

    # Create the user's permissions
    user_overwrite = hikari.PermissionOverwrite(
        id=user.id,
        type=hikari.PermissionOverwriteType.MEMBER,
        allow=(hikari.Permissions.SEND_MESSAGES
               | hikari.Permissions.ADD_REACTIONS
               | hikari.Permissions.ATTACH_FILES
               | hikari.Permissions.USE_EXTERNAL_EMOJIS
               | hikari.Permissions.VIEW_CHANNEL
               | hikari.Permissions.USE_APPLICATION_COMMANDS
               ),
    )
    # Combine the category and user permissions
    combined_overwrites = [user_overwrite, *category_overwrites]
    return combined_overwrites


async def channel_send_embed(channel, embed, component=None):
    if component == None:
        try:
            await channel.send(embed=embed)
            return
        except Exception as e:
            await error_message("Fehler B-08", e)
    elif component != None:
        try:
            await channel.send(embed=embed, components=[component])
            return
        except Exception as e:
            await error_message("Fehler B-08", e)


async def channel_send_message(channel, content, user_mentions=False):
    try:
        await channel.send(content, user_mentions=user_mentions)
        return
    except Exception as e:
        await error_message("Fehler B-12", e)


async def channel_send_with_attachment(channel, content, attachment, user_mentions=False):
    await channel.send(content=content, attachment=hikari.Bytes(attachment, "filename.png"), user_mentions=user_mentions)
    return


async def user_send_dm(user, embed, component=None):
    if component == None:
        await user.send(embed=embed)
    elif component != None:
        await user.send(embed=embed, components=[component])


async def create_embed(title, description, color):
    embed = None
    try:
        embed = hikari.Embed(
            title=title,
            description=description,
            color=color)
    except Exception as e:
        await error_message("Fehler B-09", e)
    return embed


async def create_action_row(style, custom_id, label, emoji):
    action_row = None
    try:
        action_row = plugin.bot.rest.build_message_action_row()
        if style == "SUCCESS":
            action_row.add_interactive_button(
                components.ButtonStyle.SUCCESS, custom_id, label=label, emoji=emoji)
        elif style == "DANGER":
            action_row.add_interactive_button(
                components.ButtonStyle.DANGER, custom_id, label=label, emoji=emoji)
        elif style == "PRIMARY":
            action_row.add_interactive_button(
                components.ButtonStyle.PRIMARY, custom_id, label=label, emoji=emoji)
        elif style == "SECONDARY":
            action_row.add_interactive_button(
                components.ButtonStyle.SECONDARY, custom_id, label=label, emoji=emoji)
    except Exception as e:
        await error_message("Fehler B-12", e)
    return action_row


async def guild_invites(guild_id, message_invite_code):
    try:
        invites = await plugin.bot.rest.fetch_guild_invites(guild_id)

        all_guild_invite_codes = [invite.code for invite in invites]
        if message_invite_code in all_guild_invite_codes:
            guild_valid = True
        else:
            guild_valid = False
        return guild_valid
    except Exception as e:
        print("Fehler B-02")
        print(f"Error: {e}")


async def mod_penalty_embed(user, reason, sanction_duration, proof, additional_information, moderator):
    penalty_embed = hikari.Embed(
        title="Neue Mod Penalty", description=f"**User:** {user.mention}\n\n**ID:** {user.id}\n\n**Regelbruch:** {reason}\n\n**Sanktion:** {sanction_duration}\n\n**Beweismittel:** {proof}\n\n**Zusätzliche Informationen:** {additional_information}\n\n**Moderator** {moderator}", color=0xE74C3C)
    return penalty_embed


async def log_embed(typ, user, reason, sanction_duration, additional_information):
    logmute = hikari.Embed(
        title=f"{typ}",
        description=f"**User:** {user.mention}\n**ID:** {user.id}\n**Regelbruch:** {reason}\n**Sanktion:** {sanction_duration}\n**Zusätzliche Informationen: ** {additional_information}",
        color=0xE74C3C,
    )
    logmute.set_footer(
        text=(f"Sector 7 Moderation#4384 • {datetime.now().strftime('%H:%M')}"))
    return logmute


async def message_delete(channel_id, message_id):
    try:
        await plugin.bot.rest.delete_message(channel_id, message_id)
    except Exception as e:
        print("Fehler B-01")
        print(f"Error: {e}")


async def communication_disabled(guild_id, user_id, seconds, reason):
    try:
        user_timeout = await plugin.bot.rest.fetch_member(guild_id, user_id)
        await user_timeout.edit(
            communication_disabled_until=datetime.utcnow()
            + timedelta(seconds=seconds),
            reason=reason,
        )
        return
    except Exception as e:
        print("Fehler M-11")
        print(f"Error: {e}")


async def user_permanent_ban(guild_id, user_id, reason):
    try:
        await plugin.bot.rest.ban_user(guild_id, user_id, reason=reason)
    except Exception as e:
        print("Fehler M-07")
        print(f"Error: {e}")


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
