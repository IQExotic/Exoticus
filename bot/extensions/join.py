from PIL import Image, ImageDraw, ImageFont
import asyncio
import hikari
import lightbulb
import datetime
import hikari.interactions
from datetime import datetime

import requests
from ..data.static.functions import *
from .level import *
from psycopg2.errors import UniqueViolation
import io



        
plugin = lightbulb.Plugin("join")


async def log_embed_join(event, member):
    guild_id = event.guild_id
    member_count = plugin.bot.rest.fetch_members(guild_id)
    member_count_int = await member_count.count()

    log_join_embed = hikari.Embed(
        title="Neuer User",
        description=f"**User:** {member.mention} | {member.username}\n**ID:** {member.id}\n**Count:** {member_count_int}",
        color="#4cbb64",
    )
    log_join_embed.set_footer(
        text=(f"Uhrzeit: {datetime.now().strftime('%H:%M')}"))

    log_channel = await fetch_channel_from_id(LOG_CHANNEL_ID)
    await channel_send_embed(log_channel, log_join_embed)


async def log_embed_leave(event, member):
    guild_id = event.guild_id
    member_count = plugin.bot.rest.fetch_members(guild_id)
    member_count_int = await member_count.count()

    log_join_embed = hikari.Embed(
        title="User Leave",
        description=f"**User:** {member.mention} | {member.username}\n**ID:** {member.id}\n**Count:** {member_count_int}",
        color="#ff6669",
    )
    log_join_embed.set_footer(
        text=(f"Uhrzeit: {datetime.now().strftime('%H:%M')}"))

    log_channel = await fetch_channel_from_id()
    await channel_send_embed(log_channel, log_join_embed)


async def add_role(member):
    for role_id in join_role_ids:
        await member.add_role(role_id)


async def member_join_information(member):
    await member.send(f"# Wilkommen auf **Sector 7**, {member.username}!\n## In <#924775053042798593> findest du eine simple übresicht des Servers!\n\nWenn du nach **Leuten zum Spielen zu suchst**, verwende bitte die dafür **vorgesehenen Channels:**\n\n- Valorant <#904782610667028520>\n- Rainbow 6 PC <#1115663068786065438>\n- Rainbow 6 Console <#1110933872612478987>\n- Andere Spiele <#1110936973474021457>\n\n Solltest du nach etwas **Permanenten** Suchen erstelle gerne einen **Post in** <#1110940005230202920>\n\n\nBei **Fragen** öffne gerne ein <#963132179813109790> oder Melde dich bei <@442729843055132674>!\n\n **Sector 7** :https://discord.gg/7kqsMgNURY")


def create_joincard(username, count, avatar):
    # Create a new image with background.png as background
    background = Image.open("assets/background.png")
    width, height = 960, 411

    # Resize the background image while maintaining the aspect ratio
    aspect_ratio = 21 / 9
    new_width = width
    new_height = int(new_width / aspect_ratio)
    background = background.resize((new_width, new_height))

    image = Image.new("RGBA", (width, new_height), (0, 0, 0, 0))
    image.paste(background, (0, 0))

    # Resize the background image while maintaining the aspect ratio
    aspect_ratio = background.width / background.height
    new_width = width
    new_height = int(new_width / aspect_ratio)
    background = background.resize((new_width, new_height))

    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    image.paste(background, (0, 0))

    # Set the image "profile.png" to a size of 200x200
    response = requests.get(avatar)
    with open("assets/avatar.png", "wb") as file:
        file.write(response.content)

    profile = Image.open("assets/avatar.png")
    profile = profile.resize((190, 190))

    # Check if the profile image has an alpha channel
    if profile.mode != "RGBA":
        profile = profile.convert("RGBA")

    # Create a circular mask image with the same size as the profile image
    mask = Image.new("L", profile.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, profile.width, profile.height), fill=255, outline=0)

    # Apply the circular mask to the profile image
    profile = Image.composite(profile, Image.new(
        "RGBA", profile.size, (0, 0, 0, 0)), mask)

    # Set the profile image in the middle of the background image
    profile_x = (width - profile.width) // 2 - 1
    # Adjust the value to move the profile image higher
    profile_y = (height - profile.height) // 2 - 35

    # Set the profile image using the new mask image
    image.paste(profile, (profile_x, profile_y), mask=mask)

    # Set a text with the font "Akira_Expanded.otf" with a size of 50px in the middle of the background image
    draw = ImageDraw.Draw(image)
    font_path = "assets/Akira_Expanded.otf"
    font = ImageFont.truetype(font_path, 35)
    text = f"{username}"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2 + 97
    draw.text((text_x, text_y), text, font=font, fill=(33, 34, 34))

    # Add a second text "2583"
    text2 = f"{count}"
    text2_bbox = draw.textbbox(
        (0, 0), text2, font=ImageFont.truetype(font_path, 25))
    text2_width = text2_bbox[2] - text2_bbox[0]
    text2_height = text2_bbox[3] - text2_bbox[1]
    text2_x = (width - text2_width) // 2 + 400
    text2_y = text_y + text2_height // 2 + 50
    draw.text((text2_x, text2_y), text2, font=ImageFont.truetype(
        font_path, 25), fill=(33, 34, 34))

    # Return the image instead of saving it
    output_buffer = io.BytesIO()
    image.save(output_buffer, format="PNG")
    output_buffer.seek(0)
    return output_buffer


@plugin.listener(hikari.MemberCreateEvent)
async def on_member_join(event: hikari.MemberCreateEvent):

    member = event.member
    guild = event.guild_id
    member_count = plugin.bot.rest.fetch_members(guild)
    member_count_int = await member_count.count()
    username = member.username

    await asyncio.gather(
        log_embed_join(event, member),
        add_role(member),
        member_join_information(member),
    )
    avatar_url = str(member.avatar_url)
    joincard = create_joincard(username, member_count_int, avatar_url)

    channel = await fetch_channel_from_id(plugin.bot.config.WELCOME_CHANNEL_ID)
    await channel_send_with_attachment(channel, f"Hey {member.mention}, Wilkommen auf Sector 7! Sag doch mal Hallo im ⁠<#845059359129206784>", joincard, user_mentions=True)
    while member.is_pending:
        await asyncio.sleep(1)
        member = await plugin.bot.rest.fetch_member(guild, member)

    await asyncio.sleep(5)
    current_roles = member.role_ids

    table = "users"
    column = "id, username, join_date, xp, sanctions, roles, badges, in_server"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    value = f"{member.id}, '{member.username}', '{current_time}', '0', '0', '{current_roles}', '0' , 'true'"

    try:
        db_insert_value_join(table, column, value)
    except UniqueViolation:
        table = "users"
        value = member.id
        xp = db_read_value(table, "xp", value)
        if xp != None:
            xp = int(xp[0])
            if int(xp) >= 155:
                level = get_level_from_xp(xp)
                level_role_id = get_level_role_from_level(level)
                await member.add_role(level_role_id)  # type: ignore
        current_roles = member.role_ids
        db_update_value(table, "roles", value, current_roles)
        db_update_value(table, "username", value, member.username)
        db_update_value(table, "in_server", value, 'true')


@plugin.listener(hikari.MemberDeleteEvent)
async def on_member_leave(event: hikari.MemberDeleteEvent):
    member = event.user
    await log_embed_leave(event, member)
    table = "users"
    value = member.id
    db_update_value(table, "in_server", value, 'false')
    current_roles = "[]"
    db_update_value(table, "roles", value, current_roles)
    
def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)