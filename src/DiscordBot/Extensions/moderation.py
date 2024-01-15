import hikari
import lightbulb

from .functions import *
from config import *
from customemojis import *

plugin = lightbulb.Plugin("moderation")


async def mod_penalty_send(event, user, sanktion, dauer, regelbruch, proof, zusätzliches, moderator, id, penalty_row):
    try:
        embed = hikari.Embed(
            title="Neue Mod Penalty",
            description=f"**User:** {user}\n\n**ID:** {id}\n\n**Sanktion:** {sanktion} {dauer}\n\n**Regelbruch:** {regelbruch}\n\n**Beweismittel:** {proof}\n\n**Zusätzliche Informationen:** {zusätzliches}\n\n**Moderator** {moderator}",
            color=0xE74C3C,
        )
        embed.set_footer(
            text=(f"Uhrzeit: {datetime.now().strftime('%H:%M')}"))

        channel = await fetch_channel_from_id(penalty_channel_id)
        await channel_send_embed(channel, embed, penalty_row)
        await event.respond(f"Mod Penalty erstellt in <#{penalty_channel_id}>!")
    except Exception as e:
        await error_message("Fehler B-01", e)


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
@lightbulb.option("sanktion", "Die Sanktion, die gegen den Nutzer erhoben wurde", required=True, choices=["Verwarnung", "Mute", "Ban"],)
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

    if event.channel_id != command_channel_id:
        await event.respond("Bitte nutze diesen Command nur in <#1143231143425089667>!")
        return
    if id != user.id:
        if sanktion.lower() == "ban":
            if dauer.lower() == "permanent":
                penalty_row = plugin.bot.rest.build_message_action_row()
                penalty_row.add_interactive_button(
                    components.ButtonStyle.DANGER,
                    "permban",
                    label="Permanent Bannen",
                    emoji=icon_ban,
                )
                await mod_penalty_send(event, user, sanktion, dauer, regelbruch, proof, zusätzliches, moderator, id, penalty_row)

                return
            else:
                penalty_row = plugin.bot.rest.build_message_action_row()
                penalty_row.add_interactive_button(
                    components.ButtonStyle.DANGER,
                    "tempban",
                    label=f"{dauer} Bannen",
                    emoji=icon_ban,
                )
                await mod_penalty_send(event, user, sanktion, dauer, regelbruch, proof, zusätzliches, moderator, id, penalty_row)
                return
        elif sanktion.lower() == "mute":
            penalty_row = plugin.bot.rest.build_message_action_row()
            penalty_row.add_interactive_button(
                components.ButtonStyle.PRIMARY,
                "mute",
                label=f"{dauer} Muten",
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
        dauer = embed.description.split("**Sanktion:** Ban ")[1].split("\n")[0]
        moderator = embed.description.split("**Moderator** ")[1].split("\n")[0]
        id = int(embed.description.split("**ID:** ")[1].split("\n")[0])
        return regelbruch, dauer, moderator, id


@plugin.listener(hikari.InteractionCreateEvent)
async def on_interaction_create(event: hikari.InteractionCreateEvent):
    if isinstance(event.interaction, hikari.ComponentInteraction):
        custom_id = event.interaction.custom_id
        guild_id = event.interaction.guild_id
        if custom_id in ["permban", "tempban", "mute", "warn"]:
            if custom_id == "permban":
                values = get_embed_values(event)
                if values:
                    regelbruch = values[0]
                    moderator = values[2]
                    id = values[3]
                    user = await fetch_user_from_id(int(id))
                    if user:
                        embed = await create_embed("Du wurdest Permanent Gebannt", f"**User** \n <@{id}> | user | {id} \n \n **Teammitglied**\n {moderator} | Angenommen von {event.interaction.user.mention} \n \n **Grund** \n Du wurdest wegen **{regelbruch}** Permanent Gebannt, sollte dies falsch sein, melde dich bitte auf dem Entbannungsserver oder bei {event.interaction.user.mention} \n \n **Entbannungsserver** \n Comming Soon.", "#FF6669")
                        try:
                            await user_send_dm(user, embed, component=None)
                            embed = await create_embed("Permanent Gebannt", f"**User:** {user.mention} | {user.username}\n**ID:** {user.id}\n**Regelbruch:** {regelbruch}\n**Dauer:** Permanent\n**Teammitglied:** {moderator}", "#FF6669")
                            await channel_send_embed(moderation_log_channel_id, embed, component=None)
                        except Exception as e:
                            embed = await create_embed("Permanent Gebannt", f"**User:** {user.mention} | {user.username}\n**ID:** {user.id}\n**Regelbruch:** {regelbruch}\n**Dauer:** Permanent\n**Teammitglied:** {moderator}", "#FF6669")
                            await channel_send_embed(moderation_log_channel_id, embed, component=None)
                        try:
                            await user_permanent_ban(guild_id, int(id), regelbruch)
                        except Exception as e:
                            await error_message("Fehler **B-01**", e)
            elif custom_id == "tempban":
                values = get_embed_values(event)
                if values:
                    regelbruch = values[0]
                    dauer = values[1]
                    moderator = values[2]
                    id = values[3]
                    # Send DM
                    # Send Log (if send)
                    # Ban
                return
            elif custom_id == "mute":
                values = get_embed_values(event)
                if values:
                    regelbruch = values[0]
                    dauer = values[1]
                    moderator = values[2]
                    id = values[3]
                    # Mute
                    # Send DM
                    # Send Log (if send)
                return
            elif custom_id == "warn":
                values = get_embed_values(event)
                if values:
                    regelbruch = values[0]
                    dauer = values[1]
                    moderator = values[2]
                    id = values[3]
                    # Send DM
                return


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
