import hikari
import hikari.components
import lightbulb

import json

from datetime import datetime, timedelta
from difflib import SequenceMatcher
from .functions import *



plugin = lightbulb.Plugin("filter")

logchannel_id = 1028231177422778398
penalty_channel_id = 1116107606491152395


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


async def user_dm_embed(typ, user, moderator, head_moderator, reason, sanction_duration):
    user_dm_embed = hikari.Embed(
        title=f"**{typ}**", description=f"**User** \n {user.mention} | {user} | {user.id} \n \n **Teammitglied**\n {moderator} | Angenommen von {head_moderator} \n \n **Grund** \n Du wurdest wegen {reason} für **{sanction_duration} ** Sanktioniert, sollte dies falsch sein, melde dich bitte auf dem Entbannungsserver oder Melde dich bei <@442729843055132674>\n \n **Entbannungsserver** \n Comming Soon.", color="#FF6669")
    return user_dm_embed


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


async def safe_in_file(ctx, file, new_file_content):
    file_content = []  # Initialize an empty list
    safe_is_valid = False
    try:
        with open(file, "r") as f:
            file_content = json.load(f)
            if new_file_content in file_content:
                content = f"**{new_file_content}** ist Bereits in der Liste!"
                await user_respond(ctx, content)
                safe_is_valid = None
            else:
                file_content.append(new_file_content)
                try:
                    with open(file, "w") as f:
                        json.dump(file_content, f)
                        safe_is_valid = True  # type: ignore
                except Exception as e:
                    print("Fehler B-05")
    except Exception as e:
        print("Fehler B-04")
        print(f"Error: {e}")

    return safe_is_valid


async def remove_in_file(ctx, file, removed_file_content):
    remove_is_valid = False
    try:
        with open(file, "r") as f:
            file_content = json.load(f)
            if removed_file_content in file_content:
                file_content.remove(removed_file_content)
                try:
                    with open(file, "w") as f:
                        json.dump(file_content, f)
                    remove_is_valid = True
                except Exception as e:
                    print("Fehler B-05")
                    print(f"Error: {e}")
            else:
                content = f"**{removed_file_content}** ist nicht in der Liste!"
                await user_respond(ctx, content)
                remove_is_valid = None

    except Exception as e:
        print("Fehler B-06")
        print(f"Error: {e}")
    return remove_is_valid


# Banned links
@plugin.listener(hikari.MessageCreateEvent)
async def on_message_create(event: hikari.MessageCreateEvent) -> None:  # type: ignore
    mute_words = ["discord.gg/"]

    if isinstance(event, hikari.DMMessageCreateEvent):
        return  # Skip DM messages

    if event.content:
        for word in mute_words:
            if word.lower() in event.content.lower():

                guild_id = event.guild_id  # type: ignore

                start_phrase = "discord.gg/"
                start_index = event.content.find(
                    start_phrase) + len(start_phrase)

                # Find the index of the next space after "discord.gg/"
                end_index = event.content.find(" ", start_index)

                # If there's no space after the code, set end_index to the end of the string
                if end_index == -1:
                    end_index = len(event.content)

                # Extract the code between "discord.gg/" and the next space or end of string
                code = event.content[start_index:end_index].strip()

                guild_valid = await guild_invites(guild_id, code)

                if guild_valid == False or None:

                    typ = "Timeout"
                    reason = "Discord Invite Link"
                    sanction_duration = "Timeout 5 Minuten"
                    additional_information = "Automatische Sanktion"
                    proof = event.content
                    moderator = "<@1128021040350638211>"
                    head_moderator = "<@1128021040350638211>"

                    user_id = event.author.id

                    user = await plugin.bot.rest.fetch_user(user_id)

                    duration = 300

                    logchannel = await plugin.bot.rest.fetch_channel(logchannel_id)
                    penalty_channel = await plugin.bot.rest.fetch_channel(
                        penalty_channel_id)

                    user_embed = await user_dm_embed(typ, user, moderator, head_moderator, reason, sanction_duration)

                    await message_delete(event.channel_id, event.message_id)
                    await communication_disabled(guild_id, user_id, duration, reason)
                    await user_send_dm(user, user_embed)

                    penalty_embed = await mod_penalty_embed(
                        user, reason, sanction_duration, proof, additional_information, moderator)

                    log_mute_embed = await log_embed(
                        typ, user, reason, sanction_duration, additional_information)

                    await channel_send_embed(logchannel, log_mute_embed)
                    await channel_send_embed(penalty_channel, penalty_embed)
                    return
                elif guild_valid == True:
                    return
            else:
                return
    else:
        return


@plugin.listener(hikari.MessageCreateEvent)
async def on_message_create(event: hikari.MessageCreateEvent) -> None:  # type: ignore
    ban_words = ["pornhub.com", "xhamster.com", "xvideos.com", "youporn.com", "redtube.com", "xnxx.com", "txxx.com", "spankbang.com", "tube8.com", "hentaihaven.xxx",
                 "chaturbate.com", "livejasmin.com", "cam4.com", "myfreecams.com", "bongacams.com", "stripchat.com", "camsoda.com", "xlovecam.com"]  # Liste der verbotenen Wörter

    if event.content:
        for word in ban_words:
            if word.lower() in event.content.lower():
                typ = "Permanent Gebannt"
                reason = "NSFW links"
                sanction_duration = "Ban Permanent"
                additional_information = "Automatische Sanktion"
                proof = event.content
                moderator = "<@1128021040350638211>"
                head_moderator = "<@1128021040350638211>"

                guild_id = event.guild_id  # type: ignore
                user_id = event.author.id

                user = await plugin.bot.rest.fetch_user(user_id)

                logchannel = await plugin.bot.rest.fetch_channel(logchannel_id)
                penalty_channel = await plugin.bot.rest.fetch_channel(
                    penalty_channel_id)

                user_embed = await user_dm_embed(typ, user, moderator, head_moderator, reason, sanction_duration)

                # incomming feature
                # row = plugin.bot.rest.build_message_action_row().add_interactive_button(
                #    ButtonStyle.SUCCESS, "unban", label="Ban Aufheben")

                await message_delete(event.channel_id, event.message_id)
                await user_send_dm(user, user_embed)
                await user_permanent_ban(guild_id, user_id, reason)

                penalty_embed = await mod_penalty_embed(
                    user, reason, sanction_duration, proof, additional_information, moderator)

                log_mute_embed = await log_embed(
                    typ, user, reason, sanction_duration, additional_information)

                await channel_send_embed(logchannel, log_mute_embed)
                await channel_send_embed(penalty_channel, penalty_embed)
                # LFG words


@plugin.command()
@lightbulb.option("wort", "Das Wort das geblacklisted wurde.", required=True)
@lightbulb.option("art", "Hinzufueger oder entfernen", required=True, choices=["Add", "Remove", "Show"])
@lightbulb.command("mod-lfg-keywords", "Notiere eine Sanktion, die gegen einen Nutzer erhoben wurde")
@lightbulb.implements(lightbulb.SlashCommand)
async def add_key_words(ctx: lightbulb.Context) -> None:
    type = ctx.options.art
    word = ctx.options.wort
    author = ctx.member
    file = "key-words.json"

    log_keyword_channel = await plugin.bot.rest.fetch_channel(plugin.bot.config.LOG_KEYWORD_CHANNEL_ID)             # type: ignore

    log_keyword_add_embed = hikari.Embed(
        title="LFG Keyword Hinzugefuegt",
        description=f"**Teammitglied:** {ctx.user.mention} | {ctx.user}\n**Wort:** {word}",
        color="#4cbb64",
    )
    log_keyword_remove_embed = hikari.Embed(
        title="LFG Keyword Entfernt",
        description=f"**Teammitglied:** {ctx.user.mention} | {ctx.user}\n**Wort:** {word}",
        color="#ff6669",
    )

    if type == "Add":
        safe_is_valid = await safe_in_file(ctx, file, word)
        if safe_is_valid == True:
            content = f"**{word}** Erfolgreich der Liste hinzugefügt!"
            await user_respond(ctx, content)
            await channel_send_embed(log_keyword_channel, log_keyword_add_embed)
        elif safe_is_valid == False:
            await user_respond(ctx, "Fehler B-04 oder Fehler B-05 Kontaktiere einen Developer!")
        elif safe_is_valid == None:
            return

    elif type == "Remove":
        remove_is_valid = await remove_in_file(ctx, file, word)
        if remove_is_valid == True:
            content = f"**{word}** Erfolgreich der Liste Entfernt!"
            await user_respond(ctx, content)
            await channel_send_embed(log_keyword_channel, log_keyword_remove_embed)
        elif remove_is_valid == False:
            await user_respond(ctx, "Fehler B-05 oder Fehler B-06 Kontaktiere einen Developer!")
        elif remove_is_valid == None:
            return

    elif type == "Show":
        with open(file, "r") as f:
            file_content = json.load(f)
            formatierte_liste = [f"{item}" for item in file_content]

            # Verbinde die formatierten Strings mit Zeilenumbrüchen
            my_new_list = "\n- ".join(formatierte_liste)
            print(my_new_list)
            await user_respond(ctx, my_new_list)


@plugin.listener(hikari.MessageCreateEvent)
async def on_message_create(event: hikari.MessageCreateEvent) -> None:
    lfg_id = 845059359129206784
    file = "./bot/data/static/key-words.json"
    with open(file, "r") as f:
        forbidden_words = json.load(f)

    if event.channel_id == lfg_id:
        to_do = False
        if not event.content:
            return
        for word in forbidden_words:
            words = event.content.lower().split()
            forb = word.split() if word else []
            possible = []
            if len(forb) > 1:
                for a in list(range(len(words)-(len(forb)-1))):
                    work = []
                    for b in list(range(0, len(forb))):
                        if words[a+b]:
                            work.append(words[a+b].lower())
                    possible.append(' '.join(work))
            else:
                for i in range(len(words)):
                    if words[i]:
                        possible.append(words[i].lower())

            for p in possible:
                if word is not None:
                    ratio = SequenceMatcher(None, word.lower(), p).ratio()
                    if ratio >= 0.7:
                        to_do = True
                        break
        if to_do:
            user_id = event.author.id
            user = await plugin.bot.rest.fetch_user(user_id)
            await user.send("Es sieht so aus, als hättest du versucht, nach Leuten zum Spielen zu suchen! Bitte verwende dafür die vorgesehenen Channels:\n\n- Valorant <#904782610667028520>\n- Rainbow 6 PC <#1115663068786065438>\n- Rainbow 6 Console <#1110933872612478987>\n- Andere Spiele <#1110936973474021457>\n\n Solltest du nach etwas Permanenten Suchen erstelle gerne einen Post in <#1110940005230202920>\n\n\n Solltest du keine Spieler suchen und diese Nachricht ein fehler sein, Melde dich bitte beim Serverteam indem du ein <#963132179813109790> erstellst!")
            # Nachricht löschen
            await plugin.bot.rest.delete_message(event.channel_id, event.message_id)
    f.close()

def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)