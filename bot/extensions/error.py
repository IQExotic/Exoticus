import hikari
import lightbulb


plugin = lightbulb.Plugin("error")

def load(bot):
    bot.add_plugin(plugin)
    global bot_obj
    bot_obj = bot


def unload(bot):
    bot.remove_plugin(plugin)
    global bot_obj
    bot_obj = bot


# Starting error handling