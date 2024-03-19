import hikari
import lightbulb
from bot.data.static.functions import *


plugin = lightbulb.Plugin("sudo")

@plugin.command()
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("dashboard", "change essential server settings")
@lightbulb.implements(lightbulb.SlashCommand)
async def dashboard(event: lightbulb.Context) -> None:
    embed = hikari.Embed(
        description="""# Dashboard\nHere, you can change various essential server settings to customize your experience. Use the Buttons below to modify the settings:\n\n""",
        color="#00ffbb"
    )
    dashboard_button = plugin.bot.rest.build_message_action_row()
    dashboard_button.add_interactive_button(
                components.ButtonStyle.PRIMARY,
                "Emoji ID's",
                label="emoji_ids",
            )
    dashboard_button.add_interactive_button(
                components.ButtonStyle.PRIMARY,
                "Filter ID's",
                label="filter_ids",
            )
    dashboard_button.add_interactive_button(
                components.ButtonStyle.PRIMARY,
                "Join Channel & Role ID's",
                label="join_ids",
            )
    dashboard_button.add_interactive_button(
                components.ButtonStyle.PRIMARY,
                "Level Channel & Role ID's",
                label="level_ids",
            )
    dashboard_button.add_interactive_button(
                components.ButtonStyle.PRIMARY,
                "Moderation Channel ID's",
                label="moderation_ids",
            )


    await interaction_response(event, embed, component=dashboard_button)




def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)