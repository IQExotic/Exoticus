import hikari
from hikari import CustomEmoji, components
import lightbulb

from .functions import *


plugin = lightbulb.Plugin("tickets")

# Emoji IDs
icon_customstaff = CustomEmoji(id=hikari.Snowflake(
    1157280448087609385), name="icon_customstaff", is_animated=False)
icon_forum = CustomEmoji(id=hikari.Snowflake(
    1157280387026931712), name="icon_forum", is_animated=False)
icon_person = CustomEmoji(id=hikari.Snowflake(
    1157281409807953970), name="icon_person", is_animated=False)
icon_delete = CustomEmoji(id=hikari.Snowflake(
    1157345116533567670), name="icon_delete", is_animated=False)
icon_invite = CustomEmoji(id=hikari.Snowflake(
    1157345158807957524), name="icon_person", is_animated=False)
icon_ban = CustomEmoji(id=hikari.Snowflake(
    1157080134709420053), name="icon_ban", is_animated=False)
icon_timeout = CustomEmoji(id=hikari.Snowflake(
    1157080150811361400), name="icon_timeout", is_animated=False)
icon_important = CustomEmoji(id=hikari.Snowflake(
    1157079716893839401), name="icon_important", is_animated=False)
icon_wrong = CustomEmoji(id=hikari.Snowflake(
    1157076763516608563), name="icon_wrong", is_animated=False)
icon_correct = CustomEmoji(id=hikari.Snowflake(
    1157076742985486336), name="icon_correct", is_animated=False)
icon_channel = CustomEmoji(id=hikari.Snowflake(
    1157081484738445453), name="icon_channel", is_animated=False)


# Command to create a ticket embed
@plugin.command()  # type: ignore
@lightbulb.command("createticketembed", "Erstelle die Ticket Embed")
@lightbulb.implements(lightbulb.SlashCommand)
async def createticket(ctx: lightbulb.SlashContext) -> None:

    channel = await fetch_channel_from_id(963132179813109790)
    ticket_embed = await create_embed(
        "SECTOR 7 - Ticket System", f"Wähle dein Wunsch Ticket aus dem Drop Down Menü unter dieser Nachricht aus.\n*Hinweis: Du kannst von jedem Ticket Typ nur eines gleichzeitig offen haben.*", 0x6694ff)

    row = plugin.bot.rest.build_message_action_row()
    select = row.add_text_menu(
        "tickets", min_values=1, placeholder="Wähle eine Ticket Art aus!")
    select.add_option(
        "Report", "report", description="Melde dem Serverteam einen User oder Bug.", emoji=icon_person)
    select.add_option("Support", "support",
                      description="Du hast eine Allgemeine Frage oder benötigst hilfe.", emoji=icon_forum)
    select.add_option("Bewerbung", "apply",
                      description="Werde ein Teil des Serverteams.", emoji=icon_customstaff)
    await channel_send_embed(channel, ticket_embed, row)
    if channel != None:
        await user_respond(ctx, f"Ticketembed erfolgreich erstellt in <#{channel.id}>")


async def ticket_channel_creat(report_category_id, ticket_type, user, guild_id, event, ticket_info_text):
    category = await fetch_channel_from_id(report_category_id)
    channel_name = f"{ticket_type} - {user.username}"
    description = f"**Art:** {ticket_type}\n**User:** {user.mention}\n**Teammitglied:** *Unclaimed*"

    combined_overwrites = await combine_category_permissions(user, category)

    action_row = plugin.bot.rest.build_message_action_row()
    action_row.add_interactive_button(
        components.ButtonStyle.SUCCESS, "claim", label="Claim", emoji=icon_invite)
    action_row.add_interactive_button(
        components.ButtonStyle.DANGER, "close", label="Schliessen", emoji=icon_delete)

    new_channel = await create_new_text_channel(guild_id, channel_name, combined_overwrites, report_category_id, description)

    if new_channel is not None:

        await interaction_response(event, f"{ticket_type}-Ticket wird erstellt! in {new_channel.mention}")

        ticket_info_embed = await create_embed(f"{ticket_type}-Ticket", ticket_info_text, 0x6694ff)
        user_dm_info = await create_embed(
            "Dein Ticket wurde erstellt!", f"Du hast ein {ticket_type}-Ticket **in <#{new_channel.id}> erstellt**.\n\nIn der ersten Nachricht findest du alle notwendigen Informationen darüber, wie es jetzt weitergeht und was wir von dir benötigen.\n\n*Solltest du versehentlich das falsche Ticket erstellt haben, schließe das Ticket und öffne ein neues mit der richtigen Kategorie!*", 0x6694ff)
        await channel_send_message(new_channel, user.mention, True)
        await channel_send_embed(new_channel, ticket_info_embed, action_row)
        await user_send_dm(user, user_dm_info)

    else:
        await interaction_response(event, f"Wir haben Probleme beim erstellen deines Tickets. Bitte versuche es später erneut.\n Sollte das Problem weiterhin bestehen, wende dich bitte an ein Teammitglied.")


@plugin.listener(hikari.InteractionCreateEvent)
async def on_interaction_create(event: hikari.InteractionCreateEvent):
    interaction_list = ["tickets", "claim", "close", "rate_1",
                        "rate_2", "rate_3", "rate_4", "rate_5", "confirm_close"]
    functional_interaction_list = ["claim", "close", "confirm_close"]
    rating_interaction_list = [
        "rate_1", "rate_2", "rate_3", "rate_4", "rate_5"]
    team_rating_list = ["teamupdate"]

    try:
        if event.interaction.custom_id not in interaction_list:  # type: ignore
            return

        event_interaction = event.interaction
        costum_id = event_interaction.custom_id  # type: ignore
    except AttributeError:
        return
    guild_id = event_interaction.guild_id  # type: ignore
    user = event_interaction.user  # type: ignore

    if costum_id == "tickets":
        inter: hikari.ComponentInteraction = event_interaction  # type: ignore
        ticket_type = inter.values[0] if inter.component_type == 3 else inter.custom_id

        report_ticket_type_string = "Report"
        support_ticket_type_string = "Support"
        apply_ticket_type_string = "Bewerbungs"

        report_ticket_info_text = f"**Wie geht's weiter?**\nZunächst einmal danke, dass du mithilfst, unsere Community sauber zu halten!\n\nUm dein Ticket bearbeiten zu können, benötigen wir einige Informationen:\n- Wen möchtest du melden?\n- Was ist vorgefallen?\n- Bitte füge alle relevanten Beweise, wie Screenshots oder Clips, hinzu, sofern vorhanden.\n\nFalls du noch weitere Informationen hast, die bei der Bearbeitung deines Falles hilfreich sein könnten, lass es uns wissen.\n\nEin Teammitglied wird sich so schnell wie möglich deinem Fall annehmen und sich anschließend bei dir melden."
        support_ticket_info_text = "**Wie geht's weiter?**\nBitte schildere dein Anliegen. Ein Teammitglied wird sich so schnell wie möglich deinem Fall widmen und sich anschließend bei dir melden."
        apply_ticket_info_text = "**Wie geht's weiter?**\n\n**Danke, dass du die Initiative ergriffen hast und dich bei uns bewirbst!**\nWir schätzen es, wenn Bewerber ihren eigenen Stil in die Bewerbung einbringen. Das gibt uns einen Einblick, mit welcher Ernsthaftigkeit du an die Sache herangehst. Es gibt jedoch einige Punkte, die uns wichtig sind und die wir gerne in deiner Bewerbung sehen würden.\n\n- Wer bist du?\n- Was machst du in deiner Freizeit (außer online zu sein)?\n- Warum bist du besonders geeignet für uns?\n- Was erwartest du vom Projekt 'Sector 7'?\n\nWenn du Hilfe benötigst oder Fragen hast, melde dich einfach in diesem Ticket!\n\nWir werden uns so schnell wie möglich deine Bewerbung anschauen und uns bei dir melden!"

        if ticket_type == "report":
            await ticket_channel_creat(plugin.bot.config.REPORT_CATEGORY_ID,  report_ticket_type_string, user, guild_id, event, report_ticket_info_text)
        elif ticket_type == "support":
            await ticket_channel_creat(plugin.bot.config.SUPPORT_CATEGORY_ID, support_ticket_type_string, user, guild_id, event, support_ticket_info_text)
        elif ticket_type == "apply":
            await ticket_channel_creat(plugin.bot.config.APPLY_CATEGORY_ID, apply_ticket_type_string, user, guild_id, event, apply_ticket_info_text)

    elif costum_id in functional_interaction_list:
        if costum_id == "close":
            action_row = await create_action_row(
                "SUCCESS", "confirm_close", "Ja", icon_correct)
            await interaction_response(event, "Bist du sicher das du das Ticket schliessen willst?", action_row)

        elif costum_id == "confirm_close":
            topic_staff_mention = "*Unclaimed*"
            topic_user_mention = "Unbekannt"
            topic_staff_mention_end = "uns"

            channel_id = event.interaction.channel_id  # type: ignore
            channel = await fetch_channel_from_id(channel_id)
            current_topic = channel.topic  # type: ignore

            topic_user_raw_mention = current_topic.split(
                "**User:** ")[1].split()[0]
            topic_user_id = topic_user_raw_mention.strip("<@!>")
            topic_user = await fetch_user_from_id(topic_user_id)
            if topic_user != None:
                topic_user_mention = topic_user.mention

            topic_staff_raw_mention = current_topic.split(
                "**Teammitglied:** ")[1].split()[0]
            if topic_staff_raw_mention != "*Unclaimed*":
                topic_staff_id = topic_staff_raw_mention.strip("<@!>")
                topic_staff = await fetch_user_from_id(topic_staff_id)
                if topic_staff != None:
                    topic_staff_mention = topic_staff.mention
                    topic_staff_mention_end = topic_staff_mention

            rate = plugin.bot.rest.build_message_action_row()
            rate.add_interactive_button(
                components.ButtonStyle.DANGER, "rate_1", label="1", emoji="⭐")
            rate.add_interactive_button(
                components.ButtonStyle.DANGER, "rate_2", label="2", emoji="⭐")
            rate.add_interactive_button(
                components.ButtonStyle.PRIMARY, "rate_3", label="3", emoji="⭐")
            rate.add_interactive_button(
                components.ButtonStyle.SUCCESS, "rate_4", label="4", emoji="⭐")
            rate.add_interactive_button(
                components.ButtonStyle.SUCCESS, "rate_5", label="5", emoji="⭐")

            if topic_staff_raw_mention == "*Unclaimed*":
                dm_no_rating_embed = await create_embed("Ticket Geschlossen", f"Dein Ticket wurde von {user.mention} geschlossen.\n\n**Teammitglied:** {topic_staff_mention}\n\n**Geöffnet** von: {topic_user_mention}", 0x6694ff)
                await user_send_dm(topic_user, dm_no_rating_embed)
            elif topic_staff_raw_mention != "*Unclaimed*":
                dm_rating_embed = await create_embed("Ticket Geschlossen", f"Dein Ticket wurde von {user.mention} geschlossen.\n\n**Teammitglied:** {topic_staff_mention}\n\n**Geöffnet** von: {topic_user_mention}\n\n**Wie Wars?**\nErzähl uns wie zufrieden du mit {topic_staff_mention_end} warst:\n1 :star: = Nicht sehr zufriden. - 5 :star: = Sehr Zufriden!", 0x6694ff)
                await user_send_dm(topic_user, dm_rating_embed, rate)
            await plugin.bot.rest.delete_channel(channel_id)
        elif costum_id == "claim":
            team_member = {
                442729843055132674: "CL",
                785963795834732656: "M2",
                761769735683178507: "T6",
                1019691466349613187: "T10",
                386614847019810836: "D2",
                478162390547169281: "T11",
                679385724516040704: "T12",
            }
            user_id = user.id
            if user_id in team_member:
                team_id = team_member.get(user_id)
                channel_id = event.interaction.channel_id  # type: ignore
                channel = await fetch_channel_from_id(channel_id)

                if channel is not None:
                    current_name = channel.name
                    if current_name != None:
                        username = current_name.split("-")[1].strip()
                        current_topic = channel.topic  # type: ignore
                        oldtopic = current_topic.split(
                            "**User:** ")[1].split()[0]
                        type = current_topic.split("**Art:** ")[1].split()[0]

                        new_channel_name = f"{team_id}-{username}"
                        new_topic = f"**Art:** {type}\n**User:** {oldtopic}\n**Teammitglied:** {user.mention}"
                        await channel_send_message(channel, f"{user.mention} wirds sich um das Ticket kümmern.")
                        await interaction_response(event, "Ticket erfolgreich geclaimed!")

                        try:
                            await plugin.bot.rest.edit_channel(channel.id, name=new_channel_name, topic=new_topic)
                        except Exception as e:
                            await error_message("Fehler B-14", e)
    elif costum_id in rating_interaction_list:
        embed = event_interaction.message.embeds[0]  # type: ignore
        rating_file = "ratings.json"

        try:
            teammitglied_mention = embed.description.split(
                "**Teammitglied:** ")[1].split("\n")[0]

            # Extrahieren Sie die ID aus der Erwähnung
            teammitglied_id = teammitglied_mention.strip("<@!>")

            # Lesen Sie die aktuelle JSON-Datei
            with open(rating_file, "r") as file:
                ratings = json.load(file)

            # Aktualisieren Sie die Bewertung des Teammitglieds
            rating_key = f"rating_{costum_id}"
            if teammitglied_id in ratings:
                ratings[teammitglied_id][rating_key] = ratings[teammitglied_id].get(
                    rating_key, 0) + 1
            else:
                ratings[teammitglied_id] = {rating_key: 1}

            # Schreiben Sie die aktualisierten Daten zurück in die JSON-Datei
            with open(rating_file, "w") as file:
                json.dump(ratings, file)

            # Entfernen Sie die Buttons von der Nachricht
            await event_interaction.message.edit(components=[])  # type: ignore
            await interaction_response(event, "Danke für deine Bewertung!")

        except Exception as e:
            await error_message("Fehler B-15", e)

def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)