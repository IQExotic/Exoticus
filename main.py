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
        TOKEN = getenv("TOKEN"),                                                        # type: ignore
        DEFAULT_PREFIX = getenv("DEFAULT_PREFIX"),                                      # type: ignore
        HUB_GUILD_ID = int(getenv("HUB_GUILD_ID", "")),                                 # type: ignore
        HUB_COMMANDS_CHANNEL_ID = int(getenv("HUB_COMMANDS_CHANNEL_ID", "")),           # type: ignore
        HUB_RELAY_CHANNEL_ID = int(getenv("HUB_RELAY_CHANNEL_ID", "")),                 # type: ignore
        HUB_STDOUT_CHANNEL_ID = int(getenv("HUB_STDOUT_CHANNEL_ID", "")),               # type: ignore

        # Database credentials
        PG_DB = getenv("PG_DB", ""),                                                    # type: ignore
        PG_HOST = getenv("PG_HOST", ""),                                                # type: ignore
        PG_USER = getenv("PG_USER", ""),                                                # type: ignore
        PG_PASS = getenv("PG_PASS", ""),                                                # type: ignore
        PG_PORT = int(getenv("PG_PORT", "")),                                           # type: ignore

        # Emoji IDS
        ACCEPT_EMOJI_ID = int(getenv("ACCEPT_EMOJI_ID", "")),                           # type: ignore
        CANCEL_EMOJI_ID = int(getenv("CANCEL_EMOJI_ID", "")),                           # type: ignore
        INFO_EMOJI_ID = int(getenv("INFO_EMOJI_ID", "")),                               # type: ignore
        EXIT_EMOJI_ID = int(getenv("EXIT_EMOJI_ID", "")),                               # type: ignore

        # Ticket category IDs
        REPORT_CATEGORY_ID = int(getenv("REPORT_CATEGORY_ID", "")),                     # type: ignore
        SUPPORT_CATEGORY_ID = int(getenv("SUPPORT_CATEGORY_ID", "")),                   # type: ignore
        APPY_CATEGORY_ID = int(getenv("APPY_CATEGORY_ID", "")),                         # type: ignore

        # Filter Ids
        LOG_KEYWORD_CHANNEL_ID = int(getenv("LOG_KEYWORD_CHANNEL_ID", "")),             # type: ignore

        # Join Channel & Role Ids
        LOG_CHANNEL_ID = int(getenv("LOG_CHANNEL_ID", "")),                             # type: ignore
        WELCOME_CHANNEL_ID = int(getenv("WELCOME_CHANNEL_ID", "")),                     # type: ignore

        JOIN_ROLE_IDS = loads(getenv("JOIN_ROLE_IDS", "")),                             # type: ignore

        # Level Channel & Role Ids
        LEVEL_ROLES = literal_eval(getenv("LEVEL_ROLES", "")),                          # type: ignore

        FORBIDDEN_CHANNELS = loads(getenv("FORBIDDEN_CHANNELS", "")),                   # type: ignore
        XP_LOG_CHANNEL_ID = int(getenv("XP_LOG_CHANNEL_ID", "")),                       # type: ignore
        LEVEL_UP_MESSAGE_CHANNEL_ID = int(getenv("LEVEL_UP_MESSAGE_CHANNEL_ID", "")),  # type: ignore

        # Moderation Channel Ids
        PENALTY_CHANNEL_ID = int(getenv("PENALTY_CHANNEL_ID", "")),                     # type: ignore
        MODERATION_LOG_CHANNEL_ID = int(getenv("MODERATION_LOG_CHANNEL_ID", "")),       # type: ignore
        COMMAND_CHANNEL_ID = int(getenv("COMMAND_CHANNEL_ID", ""))                      # type: ignore
        )

def main():
    bot = Bot(version=__version__, config=fetch_config(ENV_PATH))
    bot.run()

if __name__ == "__main__":
    main()