from __future__ import annotations

from os import getenv
from json import loads
from dotenv import load_dotenv
from ast import literal_eval

from bot import Bot, __version__
from bot.config import Config

ENV_PATH = ".env"

def fetch_config(filepath: str):
    load_dotenv(filepath)
    return Config(
        TOKEN = getenv("TOKEN"),
        DEFAULT_PREFIX = getenv("DEFAULT_PREFIX", ">>"),
        HUB_GUILD_ID = int(getenv("HUB_GUILD_ID", "")),
        HUB_COMMANDS_CHANNEL_ID = int(getenv("HUB_COMMANDS_CHANNEL_ID", "")),
        HUB_RELAY_CHANNEL_ID = int(getenv("HUB_RELAY_CHANNEL_ID", "")),
        HUB_STDOUT_CHANNEL_ID = int(getenv("HUB_STDOUT_CHANNEL_ID", "")),

        # Database credentials
        PG_DB = getenv("PG_DB", ""),
        PG_HOST = getenv("PG_HOST", ""),
        PG_USER = getenv("PG_USER", ""),
        PG_PASS = getenv("PG_PASS", ""),
        PG_PORT = int(getenv("PG_PORT", "")),

        # Emoji IDS
        ACCEPT_EMOJI_ID = int(getenv("ACCEPT_EMOJI_ID", "")),
        CANCEL_EMOJI_ID = int(getenv("CANCEL_EMOJI_ID", "")),
        INFO_EMOJI_ID = int(getenv("INFO_EMOJI_ID", "")),
        EXIT_EMOJI_ID = int(getenv("EXIT_EMOJI_ID", "")),

        # Ticket category IDs
        REPORT_CATEGORY_ID = int(getenv("REPORT_CATEGORY_ID", "")),
        SUPPORT_CATEGORY_ID = int(getenv("SUPPORT_CATEGORY_ID", "")),
        APPY_CATEGORY_ID = int(getenv("APPY_CATEGORY_ID", "")),

        # Filter Ids
        LOG_KEYWORD_CHANNEL_ID = int(getenv("LOG_KEYWORD_CHANNEL_ID", "")),

        # Join Channel & Role Ids
        LOG_CHANNEL_ID = int(getenv("LOG_CHANNEL_ID", "")),
        WELCOME_CHANNEL_ID = int(getenv("WELCOME_CHANNEL_ID", "")),

        JOIN_ROLE_IDS = loads(getenv("JOIN_ROLE_IDS", "")),

        # Level Channel & Role Ids
        LEVEL_ROLES = literal_eval(getenv("LEVEL_ROLES", "")),

        FORBIDDEN_CHANNELS = loads(getenv("FORBIDDEN_CHANNELS", "")),
        XP_LOG_CHANNEL_ID = int(getenv("XP_LOG_CHANNEL_ID", "")),
        LEVEL_UP_MESSAGE_CHANNEL_ID = int(getenv("LEVEL_UP_MESSAGE_CHANNEL_ID", "")),

        # Moderation Channel Ids
        PENALTY_CHANNEL_ID = int(getenv("PENALTY_CHANNEL_ID", "")),
        MODERATION_LOG_CHANNEL_ID = int(getenv("MODERATION_LOG_CHANNEL_ID", "")),
        COMMAND_CHANNEL_ID = int(getenv("COMMAND_CHANNEL_ID", ""))
        )

def main():
    bot = Bot(version=__version__, config=fetch_config(ENV_PATH))
    bot.run()

if __name__ == "__main__":
    main()