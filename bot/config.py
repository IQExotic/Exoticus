from __future__ import annotations

from os import getenv
from json import loads
from typing import Final
from ast import literal_eval

from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

@dataclass
class Config:
    # Bot token & admin credentials
    TOKEN: Final
    DEFAULT_PREFIX: Final
    HUB_GUILD_ID: Final
    HUB_COMMANDS_CHANNEL_ID: Final
    HUB_RELAY_CHANNEL_ID: Final
    HUB_STDOUT_CHANNEL_ID: Final

    # Database credentials
    PG_DB: Final
    PG_HOST: Final
    PG_USER: Final
    PG_PASS: Final
    PG_PORT: Final

    # Emoji IDS
    ACCEPT_EMOJI_ID: Final
    CANCEL_EMOJI_ID: Final
    INFO_EMOJI_ID: Final
    EXIT_EMOJI_ID: Final

    # Ticket category IDs
    REPORT_CATEGORY_ID: Final
    SUPPORT_CATEGORY_ID: Final
    APPY_CATEGORY_ID: Final

    # Filter Ids
    LOG_KEYWORD_CHANNEL_ID: Final

    # Join Channel & Role Ids
    LOG_CHANNEL_ID: Final
    WELCOME_CHANNEL_ID: Final

    JOIN_ROLE_IDS: Final

    # Level Channel & Role Ids
    LEVEL_ROLES: Final

    FORBIDDEN_CHANNELS: Final
    XP_LOG_CHANNEL_ID: Final
    LEVEL_UP_MESSAGE_CHANNEL_ID: Final

    # Moderation Channel Ids
    PENALTY_CHANNEL_ID: Final
    MODERATION_LOG_CHANNEL_ID: Final
    COMMAND_CHANNEL_ID: Final
