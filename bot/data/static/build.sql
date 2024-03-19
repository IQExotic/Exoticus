CREATE TABLE IF NOT EXISTS sector.bot (
    Key text PRIMARY KEY,
    Value timestamptz
);

INSERT INTO sector.bot (Key, Value) VALUES ('last commit', CURRENT_TIMESTAMP) ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sector.system (
    GUILD_ID bigint PRIMARY KEY,
    DEFAULT_PREFIX text DEFAULT '>>',

    REPORT_CATEGORY_ID bigint,
    SUPPORT_CATEGORY_ID bigint,
    APPY_CATEGORY_ID bigint,

    PENALTY_CHANNEL_ID bigint,
    COMMAND_CHANNEL_ID bigint,

    LOG_KEYWORD_CHANNEL_ID bigint,
    LOG_CHANNEL_ID bigint,
    WELCOME_CHANNEL_ID bigint,

    JOIN_ROLE_IDS bigint[],
    LEVEL_ROLE_IDS bigint[],
    FORBIDDEN_CHANNELS bigint[],
    XP_LOG_CHANNEL_ID bigint,
    LEVEL_UP_MESSAGE_CHANNEL_ID bigint
);