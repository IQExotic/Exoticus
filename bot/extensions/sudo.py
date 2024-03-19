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
        title="Dashboard",
        description="You can change all settings on the dashboard website. Click the button below to access it.",
        color="#00ffbb"
    )
    dashboard_button = plugin.bot.rest.build_message_action_row()
    dashboard_button.add_link_button("https://www.example.com", label="Dashboard", emoji="🌐")
    await interaction_response(event, embed, component=dashboard_button)


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)