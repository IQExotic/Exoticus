from __future__ import annotations

from os import getenv
from json import loads
from typing import Final
from ast import literal_eval

from dotenv import load_dotenv

load_dotenv()


class Config:
    try:
        # Load production token.
        with open(getenv("TOKEN", "")) as f:
            token = f.read()
    except FileNotFoundError:
        # Load development token.
        token = getenv("TOKEN", "")

    # Bot token & admin credentials
    TOKEN: Final = token
    DEFAULT_PREFIX: Final = getenv("DEFAULT_PREFIX", ">>")
    HUB_GUILD_ID: Final = int(getenv("HUB_GUILD_ID", ""))
    HUB_COMMANDS_CHANNEL_ID: Final = int(getenv("HUB_COMMANDS_CHANNEL_ID", ""))
    HUB_RELAY_CHANNEL_ID: Final = int(getenv("HUB_RELAY_CHANNEL_ID", ""))
    HUB_STDOUT_CHANNEL_ID: Final = int(getenv("HUB_STDOUT_CHANNEL_ID", ""))

    # Database credentials
    PG_DB: Final = getenv("PG_DB", "")
    PG_HOST: Final = getenv("PG_HOST", "")
    PG_USER: Final = getenv("PG_USER", "")
    PG_PASS: Final = getenv("PG_PASS", "")
    PG_PORT: Final = int(getenv("PG_PORT", ""))

    # Emoji IDS
    ACCEPT_EMOJI_ID: Final = int(getenv("ACCEPT_EMOJI_ID", ""))
    CANCEL_EMOJI_ID: Final = int(getenv("CANCEL_EMOJI_ID", ""))
    INFO_EMOJI_ID: Final = int(getenv("INFO_EMOJI_ID", ""))
    EXIT_EMOJI_ID: Final = int(getenv("EXIT_EMOJI_ID", ""))

    # Ticket category IDs
    REPORT_CATEGORY_ID: Final = int(getenv("REPORT_CATEGORY_ID", ""))
    SUPPORT_CATEGORY_ID: Final = int(getenv("SUPPORT_CATEGORY_ID", ""))
    APPY_CATEGORY_ID: Final = int(getenv("APPY_CATEGORY_ID", ""))

    # Filter Ids
    LOG_KEYWORD_CHANNEL_ID: Final = int(getenv("LOG_KEYWORD_CHANNEL_ID", ""))

    # Join Channel & Role Ids
    LOG_CHANNEL_ID: Final = int(getenv("LOG_CHANNEL_ID", ""))
    WELCOME_CHANNEL_ID: Final = int(getenv("WELCOME_CHANNEL_ID", ""))

    JOIN_ROLE_IDS: Final = loads(getenv("JOIN_ROLE_IDS", ""))

    # Level Channel & Role Ids
    LEVEL_ROLES: Final = literal_eval(getenv("LEVEL_ROLES", ""))

    FORBIDDEN_CHANNELS: Final = loads(getenv("FORBIDDEN_CHANNELS", ""))
    XP_LOG_CHANNEL_ID: Final = int(getenv("XP_LOG_CHANNEL_ID", ""))
    LEVEL_UP_MESSAGE_CHANNEL_ID: Final = int(getenv("LEVEL_UP_MESSAGE_CHANNEL_ID", ""))

    # Moderation Channel Ids
    PENALTY_CHANNEL_ID: Final = int(getenv("PENALTY_CHANNEL_ID", ""))
    MODERATION_LOG_CHANNEL_ID: Final = int(getenv("MODERATION_LOG_CHANNEL_ID", ""))
    COMMAND_CHANNEL_ID: Final = int(getenv("COMMAND_CHANNEL_ID", ""))
