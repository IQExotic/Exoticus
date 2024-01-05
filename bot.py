from env import token
import hikari
import lightbulb
from Extensions.db import *


bot = lightbulb.BotApp(
    token=token,
    intents=hikari.Intents.ALL_UNPRIVILEGED
    | hikari.Intents.MESSAGE_CONTENT
    | hikari.Intents.GUILD_MEMBERS,
)


bot.load_extensions("Extensions.filter")
bot.load_extensions("Extensions.functions")
bot.load_extensions("Extensions.join")
bot.load_extensions("Extensions.level")
bot.load_extensions("Extensions.tickets")

bot.run()
