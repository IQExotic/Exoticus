import hikari
import hikari.interactions
import lightbulb

import asyncio
import datetime
import random
from datetime import datetime

from .functions import *



plugin = lightbulb.Plugin("level")


level_from_xp = {
    1: 155,
    2: 220,
    3: 295,
    4: 380,
    5: 475,
    6: 580,
    7: 695,
    8: 820,
    9: 955,
    10: 1100,
    11: 1255,
    12: 1420,
    13: 1595,
    14: 1780,
    15: 1975,
    16: 2180,
    17: 2395,
    18: 2620,
    19: 2855,
    20: 3100,
    21: 3355,
    22: 3620,
    23: 3895,
    24: 4180,
    25: 4475,
    26: 4780,
    27: 5095,
    28: 5420,
    29: 5755,
    30: 6100,
    31: 6455,
    32: 6820,
    33: 7195,
    34: 7580,
    35: 7975,
    36: 8380,
    37: 8795,
    38: 9220,
    39: 9655,
    40: 10100,
    41: 10555,
    42: 11020,
    43: 11395,
    44: 11980,
    45: 12475,
    46: 12980,
    47: 13495,
    48: 14020,
    49: 14555,
    50: 15100,
    51: 15655,
    52: 16220,
    53: 16795,
    54: 17380,
    55: 17975,
    56: 18580,
    57: 19195,
    58: 19820,
    59: 20455,
    60: 21100,
    61: 21755,
    62: 22420,
    63: 23095,
    64: 23780,
    65: 24475,
    66: 25180,
    67: 25895,
    68: 26620,
    69: 27355,
    70: 28100,
    71: 28855,
    72: 29620,
    73: 30395,
    74: 31180,
    75: 31975,
    76: 32780,
    77: 33595,
    78: 34420,
    79: 35255,
    80: 36100,
    81: 36955,
    82: 37820,
    83: 38695,
    84: 39580,
    85: 40475,
    86: 41380,
    87: 42295,
    88: 43220,
    89: 44155,
    90: 45100,
    91: 46055,
    92: 47020,
    93: 47995,
    94: 48980,
    95: 49975,
    96: 50980,
    97: 51995,
    98: 53020,
    99: 54055,
    100: 55100,
}


async def send_level_up_message(current_level, user_id):
    channel = await fetch_channel_from_id(plugin.bot.config.LEVEL_UP_MESSAGE_CHANNEL_ID)
    # Await the fetch_user_from_id function
    user = await fetch_user_from_id(user_id)
    if user is not None:
        await channel_send_message(channel, f"{user.mention}, Du bist jetzt Level {current_level}!", user_mentions=True)


def get_level_from_xp(xp):
    # calculate level from xp
    xp = int(xp)
    level = 0
    for required_xp in level_from_xp.values():
        if xp >= required_xp:
            level += 1

        else:
            break
    return level


def get_level_role_from_level(level):
    # get level role from level
    level_role_id = None
    for required_level, role_id in level_roles.items():
        if level >= required_level:
            level_role_id = role_id
        else:
            break
    return level_role_id


async def give_xp_for_message2(user_id, guild_id):
    current_xp_str = db_read_value("users", "xp", user_id)
    if current_xp_str != None:
        current_xp = int(current_xp_str[0])
        last_xp = current_xp  # replace with actual function to read xp from database
        # gib ihm 200 xp
        if current_xp != None:
            current_xp += 100
            # aktualisiere die xp anzahl in der datenbank mit db_update_value(table, "xp", value, 'xp') <- value steht fuer die id
            db_update_value("users", "xp", user_id, current_xp)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db_update_value("users", "last_message", user_id, current_time)

            await user_has_levelup(last_xp, current_xp, user_id)
            await check_for_level_roles(current_xp, user_id, guild_id)
        return


async def give_xp_for_message(user_id, guild_id):
    last_message_time = db_read_value("users", "last_message", user_id)
    last_message_time = last_message_time[0] if last_message_time else None
    if last_message_time is None:
        await give_xp_for_message2(user_id, guild_id)
    elif last_message_time is not None:
        time_difference = datetime.now() - last_message_time
        cooldown = random.randint(10, 20)
        if time_difference.total_seconds() >= cooldown:
            await give_xp_for_message2(user_id, guild_id)


async def user_has_levelup(last_xp, current_xp, user_id):
    # ueberprufe das level vor der nachricht des users mit get_level_from_xp(xp)
    last_level = get_level_from_xp(last_xp)

    # ueberpruefe das level nach der nachricht des users mit get_level_from_xp(xp)
    current_level = get_level_from_xp(current_xp)
    if last_level == current_level:
        return
    # wenn das aktuelle level hoeher ist als das letzte ist sende eine level up nachricht
    if current_level > last_level:
        # replace with actual function to send level up message
        await send_level_up_message(current_level, user_id)
    return


async def check_for_level_roles(current_xp, user_id, guild_id):
    # ueberpruefe sein aktuelles level mit get_level_from_xp(xp)
    current_level = get_level_from_xp(current_xp)

    # ueberpruefe welche rolle er haben sollte mit get_level_role_from_level(level)
    level_role_id = get_level_role_from_level(current_level)

    user = await plugin.bot.rest.fetch_member(guild_id, user_id)

    # wenn er die rolle nicht hat, gib sie ihm
    if level_role_id is not None:
        if user is not None:
            # Entfernen Sie alle Rollen, die in level_roles definiert sind, außer der neuen Rolle
            for role_id in user.role_ids:
                if role_id in level_roles.values() and role_id != level_role_id:
                    await plugin.bot.rest.remove_role_from_member(guild_id, user_id, role_id)
            # Fügen Sie die neue Rolle hinzu, wenn der Benutzer sie noch nicht hat
            if level_role_id not in user.role_ids:
                await plugin.bot.rest.add_role_to_member(guild_id, user_id, level_role_id)

    return


async def give_xp_while_in_voice_channel(user_id, guild_id, in_voice):
    in_voice = in_voice
    current_xp_str = db_read_value("users", "xp", user_id)
    if current_xp_str != None:
        current_xp = int(current_xp_str[0])
        last_xp = current_xp
        while in_voice == True:
            if current_xp != None:
                current_xp += 5
                # aktualisiere die xp anzahl in der datenbank mit db_update_value(table, "xp", value, 'xp') <- value steht fuer die id
                db_update_value("users", "xp", user_id, current_xp)
                voice_xp_str = db_read_value("voice", "voice_xp", user_id)
                if voice_xp_str != None:
                    voice_xp = int(voice_xp_str[0])
                    voice_xp += 5
                    db_update_value("voice", "voice_xp", user_id, voice_xp)
                    await user_has_levelup(last_xp, current_xp, user_id)
                    await check_for_level_roles(current_xp, user_id, guild_id)
                    await asyncio.sleep(60)
                    in_voice_unsorted = db_read_value(
                        "voice", "in_voice", user_id)
                    if in_voice_unsorted != None:
                        in_voice = in_voice_unsorted[0]
                        last_xp = current_xp


@plugin.listener(hikari.MessageCreateEvent)
async def on_message_create(event: hikari.MessageCreateEvent) -> None:
    # wenn der author der nachricht ein bot ist, stoppe
    if event.author.is_bot:
        return
    # wenn der channel ein DM channel ist, stoppe
    if isinstance(event, hikari.DMMessageCreateEvent):
        return  # Skip DM messages

    # wenn der channel in dem die nachricht gesendet wurde nicht der bot channel ist, stoppe
    if event.channel_id not in plugin.bot.config.FORBIDDEN_CHANNELS:
        guild_id = event.guild_id  # type: ignore
        user_id = event.author.id
        # wenn die nachricht in einem server gesendet wurde, gib dem user 200 xp
        await give_xp_for_message(user_id, guild_id)


@plugin.listener(hikari.VoiceStateUpdateEvent)
async def on_voice_state_update(event: hikari.VoiceStateUpdateEvent):
    user_id = str(event.state.user_id)
    guild_id = str(event.state.guild_id)

    async def voice_xp_check():
        if event.state.channel_id != None:  # user ist in einem channel
            exists = dv_check_if_exists("voice", "id", user_id)
            if exists == False:  # user ist nicht in der Datenbank
                db_insert_value("voice", "id, in_voice",
                                f"{user_id}, 'True'")
                await give_xp_while_in_voice_channel(user_id, guild_id, True)
            elif exists == True:  # user ist in der Datenbank
                db_update_value("voice", "in_voice", user_id, True)
                await give_xp_while_in_voice_channel(user_id, guild_id, True)
                # Überprüfen, ob der Benutzer einen Voice-Channel verlassen hat

    if event.old_state != None:

        if event.state.channel_id != event.old_state.channel_id:
            if event.old_state.channel_id != None:
                if event.state.channel_id == None:  # user hat den channel verlassen
                    exists = dv_check_if_exists("voice", "id", user_id)
                    if exists == False:  # user ist nicht in der Datenbank
                        db_insert_value("voice", "id, in_voice",
                                        f"{user_id}, 'False'")
                    elif exists == True:  # user ist in der Datenbank
                        db_update_value("voice", "in_voice", user_id, False)
                        return
            elif event.old_state.channel_id == None:
                in_voice_unsorted = db_read_value(
                    "voice", "in_voice", user_id)
                if in_voice_unsorted != None:
                    in_voice = in_voice_unsorted[0]
                    if in_voice == False or None:
                        await voice_xp_check()
    elif event.old_state == None:
        await voice_xp_check()


@plugin.command()
@lightbulb.option("user", "Gib einem User XP", type=hikari.OptionType.USER)
@lightbulb.option("type", "XP geben oder nehmen", choices=["add", "remove"])
@lightbulb.option("amount", "amount of xp", type=hikari.OptionType.INTEGER)
@lightbulb.command("xpedit", "Vergibt oder entfernt XP von einem Benutzer.")
@lightbulb.implements(lightbulb.SlashCommand)
async def xpedit(ctx: lightbulb.SlashContext) -> None:
    user = ctx.options.user
    xp_type = ctx.options.type
    amount = ctx.options.amount
    Teammitglied = ctx.member

    user_id = user.id
    guild_id = ctx.guild_id

    async def send_embed():
        title = "XP Log"
        color = 0x000000
        description = "fehler"
        if Teammitglied != None:
            description = f"**Teammitglied:** {Teammitglied.mention} **User:** {user.mention} | {user.id}\n**Type:** {xp_type}\n**Amount:** {amount}"
        if xp_type == "add":
            color = "#4cbb64"
        elif xp_type == "remove":
            color = "#ff6669"
        embed = await create_embed(title, description, color)
        channel = await fetch_channel_from_id(xp_log_channel_id)
        await channel_send_embed(channel, embed, component=None)

        return

    if xp_type == "add":
        current_xp = db_read_value(
            "users", "xp", user_id)
        if current_xp != None:
            current_xp = int(current_xp[0])
            new_xp = current_xp + int(amount)
            db_update_value("users", "xp", user_id, new_xp)
            await send_embed()
            await user_respond(ctx, f"Du hast {amount} XP an {user.mention} gegeben.")
            await user_has_levelup(current_xp, new_xp, user_id)
            await check_for_level_roles(new_xp, user_id, guild_id)
        return
    elif xp_type == "remove":
        current_xp = db_read_value(
            "users", "xp", user_id)
        if current_xp != None:
            current_xp = int(current_xp[0])
            new_xp = current_xp - int(amount)
            db_update_value("users", "xp", user_id, new_xp)
            await send_embed()
            await user_respond(ctx, f"Du hast {amount} XP von {user.mention} entfernt.")
            await user_has_levelup(current_xp, new_xp, user_id)
            await check_for_level_roles(new_xp, user_id, guild_id)
        return


@plugin.command()
@lightbulb.option("user", "user to check xp", type=hikari.OptionType.USER, required=False)
@lightbulb.command("rank", "Zeigt die XP und das Level des Benutzers an.")
@lightbulb.implements(lightbulb.SlashCommand)
async def rank(ctx: lightbulb.SlashContext) -> None:
    if ctx.channel_id in plugin.bot.config.FORBIDDEN_CHANNELS:
        if ctx.options.user is None:
            user = ctx.author
        else:
            user = ctx.options.user

        def xp_for_next_rank(current_xp):
            for xp in level_from_xp.items():
                if int(xp[0]) > current_xp:
                    return xp - current_xp
            return 0

        rank = get_rank_from_value("users", "xp", user.id)
        xp = db_read_value("users", "xp", user.id)
        xp = int(xp[0]) if xp else None
        next_rank_xp = xp_for_next_rank(xp)
        voice_xp = db_read_value("voice", "voice_xp", user.id)
        voice_xp = int(voice_xp[0]) if voice_xp else None

        rankembed = hikari.Embed(
            title="Level Daten",
            color="#ffffff",
        )
        rankembed.add_field(
            name="Meta Daten",
            value=f"> **User:** {user.mention}\n> **Rank:** {rank}",
            inline=False
        )
        if xp != None:
            rankembed.add_field(
                name="Level Daten",
                value=f"> **XP:** {xp} - Davon durch Voice Chat erhalten: {voice_xp}\n> **Level:** {get_level_from_xp(xp)}\n> **XP bis zum nächsten Level:** {next_rank_xp}",
                inline=False
            )

        await ctx.respond(embed=rankembed)


@plugin.command()
@lightbulb.command("top", "Erstelle eine Leaderboard nachricht in Ranking")
@lightbulb.implements(lightbulb.SlashCommand)
async def top(ctx: lightbulb.SlashContext) -> None:

    embed = hikari.Embed(
        title="Level Leaderboard")
    top_5 = top_5_from_column("users", "id, xp", "xp", "5")

    row = plugin.bot.rest.build_message_action_row().add_interactive_button(
        components.ButtonStyle.SUCCESS,
        "updatelb",
        label="Leaderboard Aktualisieren"
    )

    if top_5 != None:
        for rank, (user_id, xp) in enumerate(top_5, 1):
            user = await fetch_user_from_id(user_id)
            if user is not None:
                embed.add_field(
                    name=f"{rank}. Platz",
                    value=f"{user.mention} (@{user.username}) | XP: {xp}",
                    inline=False
                )

    channel = await fetch_channel_from_id(1130012873452699729)
    await channel_send_embed(channel, embed, row)


@plugin.listener(hikari.InteractionCreateEvent)
async def on_interaction_create(event: hikari.InteractionCreateEvent):
    if isinstance(event.interaction, hikari.ComponentInteraction):
        if event.interaction.custom_id == "updatelb":
            top_5 = top_5_from_column("users", "id, xp", "xp", "5")

            channel_id = event.interaction.channel_id
            message_id = event.interaction.message.id
            message = await plugin.bot.rest.fetch_message(channel_id, message_id)

            embed = message.embeds[0]
            fields = []
            if top_5 != None:
                for rank, (user_id, xp) in enumerate(top_5, 1):
                    user = await fetch_user_from_id(user_id)
                    if user is not None:
                        embed.add_field(
                            name=f"{rank}. Platz",
                            value=f"{user.mention} (@{user.username}) | XP: {xp}",
                            inline=False
                        )
                        fields.append(hikari.EmbedField(name=f"{rank}. Platz",
                                                        value=f"{user.mention} (@{user.username}) | XP: {xp}",
                                                        inline=False)
                                      )
            updated_embed = hikari.Embed(title=embed.title, color=embed.color)
            now = datetime.now() + timedelta(hours=0)
            updated_embed.set_footer(
                text=f"Letztes Update: {now.strftime('%H:%M')}")

            for field in fields:
                updated_embed.add_field(name=field.name, value=field.value)

            await message.edit(embed=updated_embed)
            await event.interaction.create_initial_response(hikari.ResponseType.DEFERRED_MESSAGE_UPDATE)
            return
        
def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)