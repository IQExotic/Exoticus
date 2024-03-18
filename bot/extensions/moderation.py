import hikari
import lightbulb

from .functions import *
from bot.config import *

plugin = lightbulb.Plugin("moderation")


async def mod_penalty_send(event, user, sanktion, dauer, regelbruch, proof, zusätzliches, moderator, id, penalty_row):
    try:
        embed = hikari.Embed(
            title="Neue Mod Penalty",
            description=f"**User:** {user.mention}\n\n**ID:** {id}\n\n**Sanktion:** {sanktion} {dauer}\n\n**Regelbruch:** {regelbruch}\n\n**Beweismittel:** {proof}\n\n**Zusätzliche Informationen:** {zusätzliches}\n\n**Moderator** {moderator.mention}",
            color=0xE74C3C,
        )
        embed.set_footer(
            text=(f"Uhrzeit: {datetime.now().strftime('%H:%M')}"))

        channel = await fetch_channel_from_id(penalty_channel_id)
        await channel_send_embed(channel, embed, penalty_row)
        await event.respond(f"Mod Penalty erstellt in <#{penalty_channel_id}>!")
    except Exception as e:
        await error_message("Fehler MP-01", e)
        content = f"Fehler **MP-01**"
        await interaction_response(event, content, component=None)


@plugin.command()
@lightbulb.option("zusaetzliches", "Extra Dinge, die ihr anmerken wollt", required=False)
@lightbulb.option("proof", "Beweismaterial")
@lightbulb.option("regelbruch", "Die Regel, die der Nutzer verbrochen hat", required=True)
@lightbulb.option("dauer", "Die Dauer der Sanktion", required=True, choices=[
    "1 Tag",
    "3 Tage",
    "1 Woche",
    "2 Wochen",
    "1 Monat",
    "3 Monate",
    "Permanent",],
)
@lightbulb.option("sanktion", "Die Sanktion, die gegen den Nutzer erhoben wurde", required=True, choices=["Verwarnung", "Timeout", "Ban"],)
@lightbulb.option("id", "Die ID des Users")
@lightbulb.option("user", "Die ID des Nutzers", type=hikari.OptionType.USER)
@lightbulb.command("mod-penalty", "Notiere eine Sanktion, die gegen einen Nutzer erhoben wurde")
@lightbulb.implements(lightbulb.SlashCommand)
async def mod_penalty(event: lightbulb.Context) -> None:
    zusätzliches = event.options.zusaetzliches
    regelbruch = event.options.regelbruch
    sanktion = event.options.sanktion
    dauer = event.options.dauer
    user = event.options.user
    id = event.options.id
    proof = event.options.proof
    moderator = event.member

    if sanktion == "Timeout" and dauer in ["Permanent", "3 Monate", "1 Monat"]:
        content = "Timeout können nicht länger als 2 Wochen sein!"
        await interaction_response(event, content, component=None)
        return

    if event.channel_id != command_channel_id:
        content = "Bitte nutze diesen Command nur in <#1143231143425089667>!"
        await interaction_response(event, content, component=None)
        return

    if id != user.id:

        if sanktion.lower() == "ban":
            penalty_row = plugin.bot.rest.build_message_action_row()
            penalty_row.add_interactive_button(
                components.ButtonStyle.DANGER,
                "permban",
                label="Permanent Bannen",
                emoji=icon_ban,
            )
            await mod_penalty_send(event, user, sanktion, dauer, regelbruch, proof, zusätzliches, moderator, id, penalty_row)
            return

        elif sanktion.lower() == "timeout":
            penalty_row = plugin.bot.rest.build_message_action_row()
            penalty_row.add_interactive_button(
                components.ButtonStyle.PRIMARY,
                "timeout",
                label=f"{dauer} Timeouten",
                emoji=icon_timeout,
            )
            await mod_penalty_send(event, user, sanktion, dauer, regelbruch, proof, zusätzliches, moderator, id, penalty_row)
            return

        elif sanktion.lower() == "verwarnung":
            penalty_row = plugin.bot.rest.build_message_action_row()
            penalty_row.add_interactive_button(
                components.ButtonStyle.SECONDARY,
                "warn",
                label="Verwarnen",
                emoji=icon_important,
            )
            await mod_penalty_send(event, user, sanktion, dauer, regelbruch, proof, zusätzliches, moderator, id, penalty_row)
            return
    else:
        await user_respond(event, "Fehler **B-01**")


def get_embed_values(event):
    if len(event.interaction.message.embeds) > 0:
        embed = event.interaction.message.embeds[0]
        regelbruch = embed.description.split(
            "**Regelbruch:** ")[1].split("\n")[0]
        try:
            dauer = embed.description.split(
                "**Sanktion:** Ban ")[1].split("\n")[0]
        except Exception as e:
            try:
                dauer = embed.description.split(
                    "**Sanktion:** Timeout ")[1].split("\n")[0]
            except Exception as e:
                dauer = None

        moderator = embed.description.split("**Moderator** ")[1].split("\n")[0]
        id = int(embed.description.split("**ID:** ")[1].split("\n")[0])
        return regelbruch, dauer, moderator, id


def create_db_sanction():
    # add 1 sanction to user where id is id
    # generate case_id
    # add a reason
    # add a sanction
    case_id = 0000  # reade highes case_id
    case_id += 1
    table = "moderation"
    db_insert_value(table, 'case_id', case_id)


@plugin.listener(hikari.InteractionCreateEvent)
async def on_interaction_create(event: hikari.InteractionCreateEvent):
    if isinstance(event.interaction, hikari.ComponentInteraction):
        custom_id = event.interaction.custom_id
        guild_id = event.interaction.guild_id

        if custom_id in ["permban", "timeout", "warn"]:

            if custom_id == "permban":
                values = get_embed_values(event)

                if values:
                    regelbruch = values[0]
                    moderator = values[2]
                    id = values[3]
                    user = await fetch_user_from_id(int(id))

                    if user:
                        embed = await create_embed("Du wurdest Permanent Gebannt", f"**User** \n {user.mention} | {user} | {id} \n \n **Teammitglied**\n {moderator} | Angenommen von {event.interaction.user.mention} \n \n **Grund** \n Du wurdest wegen **{regelbruch}** Permanent Gebannt, sollte dies falsch sein, melde dich bitte auf dem Entbannungsserver oder bei {event.interaction.user.mention} \n \n **Entbannungsserver** \n Comming Soon.", "#FF6669")

                        try:
                            await user_send_dm(user, embed, component=None)
                            embed = await create_embed("Permanent Gebannt", f"> **User:** {user.mention} | {user.username}\n> **ID:** {user.id}\n> **Regelbruch:** {regelbruch}\n> **Dauer:** Permanent\n> **Teammitglied:** {moderator}", "#E74D3C")
                            channel = await fetch_channel_from_id(moderation_log_channel_id)
                            await channel_send_embed(channel, embed, component=None)
                        except Exception as e:
                            embed = await create_embed("Permanent Gebannt", f"> **User:** {user.mention} | {user.username}\n> **ID:** {user.id}\n> **Regelbruch:** {regelbruch}\n> **Dauer:** Permanent\n> **Teammitglied:** {moderator}", "#E74D3C")
                            channel = await fetch_channel_from_id(moderation_log_channel_id)
                            await channel_send_embed(channel, embed, component=None)
                            await error_message("Fehler MP-04", e)
                            content = f"Fehler **MP-04**"
                            await interaction_response(event, content, component=None)

                        try:
                            await user_permanent_ban(guild_id, int(id), regelbruch)
                        except Exception as e:
                            await error_message("Fehler **MP-02**", e)
                            content = f"Fehler **MP-02**"
                            await interaction_response(event, content, component=None)

                        edited_button = []
                        ban_button = plugin.bot.rest.build_message_action_row()
                        ban_button.add_interactive_button(
                            components.ButtonStyle.DANGER,
                            "ban",
                            label=f"gebannt von {event.interaction.user.username}",
                            is_disabled=True,
                        )
                        unban_button = plugin.bot.rest.build_message_action_row()
                        unban_button.add_interactive_button(
                            components.ButtonStyle.SUCCESS,
                            "unban",
                            label=f"Entbannen",
                        )
                        edited_button.append(ban_button)
                        edited_button.append(unban_button)
                        await event.interaction.message.edit(components=edited_button)

            elif custom_id == "timeout":
                values = get_embed_values(event)

                if values:
                    regelbruch = values[0]
                    dauer = values[1]
                    moderator = values[2]
                    id = values[3]

                    if guild_id and dauer:
                        try:
                            user = await plugin.bot.rest.fetch_member(guild_id, id)
                        except Exception as e:
                            await error_message("Fehler **F-01**", e)
                            content = f"Fehler **F-01**"
                            await interaction_response(event, content, component=None)
                            return

                        duration_mapping = {
                            "1 Tag": 1 * 24 * 60 * 60,
                            "3 Tage": 3 * 24 * 60 * 60,
                            "1 Woche": 7 * 24 * 60 * 60,
                            "2 Wochen": 14 * 24 * 60 * 60,
                            "1 Monat": 30 * 24 * 60 * 60,
                            "3 Monate": 3 * 30 * 24 * 60 * 60,
                        }
                        duration = duration_mapping.get(dauer)

                        if duration and user:

                            try:
                                await user.edit(
                                    communication_disabled_until=datetime.utcnow()
                                    + timedelta(seconds=duration),
                                    reason=regelbruch,
                                )
                                content = f"Fehler **MP-01**"
                                await interaction_response(event, content, component=None)
                            except Exception as e:
                                await error_message("Fehler **MP-03**", e)
                                content = f"Fehler **MP-03**"
                                await interaction_response(event, content, component=None)

                            embed = await create_embed("Du wurdest Timeouted", f"**User** \n {user.mention} | user | {id} \n \n **Teammitglied**\n {moderator} | Angenommen von {event.interaction.user.mention} \n \n **Grund** \nDu wurdest wegen **{regelbruch}** für {dauer} in den Timeout versetzt. Infolge hast du eine Verwarnung erhalten. Die verwarnung bleibt für 3 Monate bestehen. Solltest du insgesamt drei Verwarnungen erhalten, droht ein Permaneter ausschluss!\n\nWenn du der Meinung bist, dass hier ein Fehler vorliegt, kannst du jederzeit ein <#963132179813109790> öffnen.\n\nBitte achte in Zukunft darauf, einen respektvollen Umgangston zu wahren und eine positive Atmosphäre in unserer Community zu fördern.\n \n **Entbannungsserver** \n Comming Soon.", "#FF6669")

                            try:
                                await user_send_dm(user, embed, component=None)
                                embed = await create_embed("Timeout", f"> **User:** {user.mention} | {user.username}\n> **ID:** {user.id}\n> **Regelbruch:** {regelbruch}\n> **Dauer:** Timeout {dauer}\n> **Teammitglied:** {moderator}", "#FF6669")
                                channel = await fetch_channel_from_id(moderation_log_channel_id)
                                await channel_send_embed(channel, embed, component=None)
                            except Exception as e:
                                embed = await create_embed("Timeout", f"> **User:** {user.mention} | {user.username}\n> **ID:** {user.id}\n> **Regelbruch:** {regelbruch}\n> **Dauer:** Timeout {dauer}\n> **Teammitglied:** {moderator}", "#FF6669")
                                channel = await fetch_channel_from_id(moderation_log_channel_id)
                                await channel_send_embed(channel, embed, component=None)
                                await error_message("Fehler MP-04", e)
                                content = f"Fehler **MP-04**"
                                await interaction_response(event, content, component=None)

                            edited_button = []
                            timeout_button = plugin.bot.rest.build_message_action_row()
                            timeout_button.add_interactive_button(
                                components.ButtonStyle.PRIMARY,
                                "timeout",
                                label=f"Timedout von {event.interaction.user.username}",
                                is_disabled=True,
                            )
                            remove_timeout_button = plugin.bot.rest.build_message_action_row()
                            remove_timeout_button.add_interactive_button(
                                components.ButtonStyle.SUCCESS,
                                "remove_timeout",
                                label=f"Remove Timeout",
                            )
                            edited_button.append(timeout_button)
                            edited_button.append(remove_timeout_button)
                            await event.interaction.message.edit(components=edited_button)

            elif custom_id == "warn":
                values = get_embed_values(event)

                if values:
                    regelbruch = values[0]
                    id = values[3]

                    if guild_id:
                        try:
                            user = await plugin.bot.rest.fetch_member(guild_id, id)
                        except Exception as e:
                            await error_message("Fehler **F-01**", e)
                            content = f"Fehler **F-01**"
                            await interaction_response(event, content, component=None)

                        embed = await create_embed("Du wurdest Verwarnt", f"Hey {user.mention}, \n\nWir müssen dir leider mitteilen, dass du eine Verwarnung erhalten hast. Grund dafür ist **{regelbruch}**. Diese Verwarnung bleibt für 3 Monate bestehen. \n Solltest du insgesamt drei Verwarnungen erhalten, droht ein Permanenter ausschluss!\n\nWenn du der Meinung bist, dass hier ein Fehler vorliegt, kannst du jederzeit ein <#963132179813109790> öffnen.\n\nBitte achte in Zukunft darauf, einen respektvollen Umgangston zu wahren und eine positive Atmosphäre in unserer Community zu fördern. \n\nBeste Grüße, \nDas Moderationsteam", "#FF6669")

                        try:
                            await user_send_dm(user, embed, component=None)
                        except Exception as e:
                            await error_message("Fehler **MP-04**", e)
                            content = f"Fehler **MP-04**"
                            await interaction_response(event, content, component=None)

                        content = f"{user.mention} Erfolgreich Verwarnt"
                        await interaction_response(event, content, component=None)

                        edited_button = []
                        warn_button = plugin.bot.rest.build_message_action_row()
                        warn_button.add_interactive_button(
                            components.ButtonStyle.SECONDARY,
                            "warn",
                            label=f"Verwarnt von {event.interaction.user.username}",
                            is_disabled=True,
                        )
                        remove_warn_button = plugin.bot.rest.build_message_action_row()
                        remove_warn_button.add_interactive_button(
                            components.ButtonStyle.SUCCESS,
                            "remove_warn",
                            label=f"Remove Warn",
                        )
                        edited_button.append(warn_button)
                        edited_button.append(remove_warn_button)
                        await event.interaction.message.edit(components=edited_button)

        elif custom_id in ["unban", "remove_timeout", "remove_warn"]:
            values = get_embed_values(event)
            if values:
                id = values[3]
                if custom_id == "unban":
                    # if user is banned <- check if user is banned fia db
                    # if interaction.user has permission <- check via db
                    await user_unban(guild_id, id)
                    # Edit Button
                    return
                elif custom_id == "remove_timeout":
                    # if user is still in timeout
                    # if interaction.user has permission <- check via db
                    # remove timeout
                    # Edit Button
                    return
                elif custom_id == "remove_warn":
                    # set warn to false in db
                    return