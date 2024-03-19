"""

 @lru_cache(maxsize=128, typed=False)

 maxsize -> the max amount of differend values it can store | None for unlimited
 typed=False -> if an argument is int in the cache, but then resives the same data as str. Won't save both of them

 

smth.cache_clear()

smth.cache_info()

smth.cache_parameters()


NOTE: All functions that use @lru MUST start with `cached_` in the name


"""
from functools import lru_cache

class CacheManager:
    def __init__(self, bot):
        self.bot = bot

    @lru_cache(maxsize=128, typed=False)
    async def cached_getChannelID(self, guild_id: int):
        res = await self.bot.db.field(f"SELECT DEFAULT_PREFIX FROM {self.bot.db.schema}.system WHERE GUILD_ID = $1", guild_id)
        return res
    
    async def set_ChannelID(self, value: int, guild_id: int):
        await self.bot.db.execute(f"UPDATE {self.bot.db.schema}.system SET DEFAULT_PREFIX = $1 WHERE GUILD_ID = $2", value, guild_id)
        self.cached_getChannelID.cache_clear()


    @lru_cache(maxsize=128, typed=False)
    async def cached_ReportCategoryID(self, guild_id: int):
        res = await self.bot.db.field(f"SELECT REPORT_CATEGORY_ID FROM {self.bot.db.schema}.system WHERE GUILD_ID = $1", guild_id)
        return res
    
    async def set_ReportCategoryID(self, value: int, guild_id: int):
        await self.bot.db.execute(f"UPDATE {self.bot.db.schema}.system SET REPORT_CATEGORY_ID = $1 WHERE GUILD_ID = $2", value, guild_id)
        self.cached_ReportCategoryID.cache_clear()


    @lru_cache(maxsize=128, typed=False)
    async def cached_SupportCategoryID(self, guild_id: int):
        res = await self.bot.db.field(f"SELECT SUPPORT_CATEGORY_ID FROM {self.bot.db.schema}.system WHERE GUILD_ID = $1", guild_id)
        return res
    
    async def set_SupportCategoryID(self, value: int, guild_id: int):
        await self.bot.db.execute(f"UPDATE {self.bot.db.schema}.system SET SUPPORT_CATEGORY_ID = $1 WHERE GUILD_ID = $2", value, guild_id)
        self.cached_SupportCategoryID.cache_clear()


    @lru_cache(maxsize=128, typed=False)
    async def cached_AppyCategoryID(self, guild_id: int):
        res = await self.bot.db.field(f"SELECT APPY_CATEGORY_ID FROM {self.bot.db.schema}.system WHERE GUILD_ID = $1", guild_id)
        return res
    
    async def set_AppyCategoryID(self, value: int, guild_id: int):
        await self.bot.db.execute(f"UPDATE {self.bot.db.schema}.system SET APPY_CATEGORY_ID = $1 WHERE GUILD_ID = $2", value, guild_id)
        self.cached_AppyCategoryID.cache_clear()


    @lru_cache(maxsize=128, typed=False)
    async def cached_PenaltyChannelID(self, guild_id: int):
        res = await self.bot.db.field(f"SELECT PENALTY_CHANNEL_ID FROM {self.bot.db.schema}.system WHERE GUILD_ID = $1", guild_id)
        return res
    
    async def set_PenaltyChannelID(self, value: int, guild_id: int):
        await self.bot.db.execute(f"UPDATE {self.bot.db.schema}.system SET PENALTY_CHANNEL_ID = $1 WHERE GUILD_ID = $2", value, guild_id)
        self.cached_PenaltyChannelID.cache_clear()


    @lru_cache(maxsize=128, typed=False)
    async def cached_CommandChannelID(self, guild_id: int):
        res = await self.bot.db.field(f"SELECT COMMAND_CHANNEL_ID FROM {self.bot.db.schema}.system WHERE GUILD_ID = $1", guild_id)
        return res
    
    async def set_CommandChannelID(self, value: int, guild_id: int):
        await self.bot.db.execute(f"UPDATE {self.bot.db.schema}.system SET COMMAND_CHANNEL_ID = $1 WHERE GUILD_ID = $2", value, guild_id)
        self.cached_CommandChannelID.cache_clear()


    @lru_cache(maxsize=128, typed=False)
    async def cached_LogKeywordChannelID(self, guild_id: int):
        res = await self.bot.db.field(f"SELECT LOG_KEYWORD_CHANNEL_ID FROM {self.bot.db.schema}.system WHERE GUILD_ID = $1", guild_id)
        return res
    
    async def set_LogKeywordChannelID(self, value: int, guild_id: int):
        await self.bot.db.execute(f"UPDATE {self.bot.db.schema}.system SET LOG_KEYWORD_CHANNEL_ID = $1 WHERE GUILD_ID = $2", value, guild_id)
        self.cached_LogKeywordChannelID.cache_clear()


    @lru_cache(maxsize=128, typed=False)
    async def cached_LogChannelID(self, guild_id: int):
        res = await self.bot.db.field(f"SELECT LOG_CHANNEL_ID FROM {self.bot.db.schema}.system WHERE GUILD_ID = $1", guild_id)
        return res
    
    async def set_LogChannelID(self, value: int, guild_id: int):
        await self.bot.db.execute(f"UPDATE {self.bot.db.schema}.system SET LOG_CHANNEL_ID = $1 WHERE GUILD_ID = $2", value, guild_id)
        self.cached_LogChannelID.cache_clear()


    @lru_cache(maxsize=128, typed=False)
    async def cached_WelcomeChannelID(self, guild_id: int):
        res = await self.bot.db.field(f"SELECT WELCOME_CHANNEL_ID FROM {self.bot.db.schema}.system WHERE GUILD_ID = $1", guild_id)
        return res
    
    async def set_WelcomeChannelID(self, value: int, guild_id: int):
        await self.bot.db.execute(f"UPDATE {self.bot.db.schema}.system SET WELCOME_CHANNEL_ID = $1 WHERE GUILD_ID = $2", value, guild_id)
        self.cached_WelcomeChannelID.cache_clear()


    @lru_cache(maxsize=128, typed=False)
    async def cached_JoinRoleIDs(self, guild_id: int):
        res = await self.bot.db.field(f"SELECT JOIN_ROLE_IDS FROM {self.bot.db.schema}.system WHERE GUILD_ID = $1", guild_id)
        return res
    
    async def set_JoinRoleIDs(self, value: int, guild_id: int):
        await self.bot.db.execute(f"UPDATE {self.bot.db.schema}.system SET JOIN_ROLE_IDS = $1 WHERE GUILD_ID = $2", value, guild_id)
        self.cached_JoinRoleIDs.cache_clear()


    @lru_cache(maxsize=128, typed=False)
    async def cached_LevelRoleIDs(self, guild_id: int):
        res = await self.bot.db.field(f"SELECT LEVEL_ROLE_IDS FROM {self.bot.db.schema}.system WHERE GUILD_ID = $1", guild_id)
        return res
    
    async def set_LevelRoleIDs(self, value: int, guild_id: int):
        await self.bot.db.execute(f"UPDATE {self.bot.db.schema}.system SET LEVEL_ROLE_IDS = $1 WHERE GUILD_ID = $2", value, guild_id)
        self.cached_LevelRoleIDs.cache_clear()


    @lru_cache(maxsize=128, typed=False)
    async def cached_ForbiddenChannels(self, guild_id: int):
        res = await self.bot.db.field(f"SELECT FORBIDDEN_CHANNELS FROM {self.bot.db.schema}.system WHERE GUILD_ID = $1", guild_id)
        return res
    
    async def set_ForbiddenChannels(self, value: int, guild_id: int):
        await self.bot.db.execute(f"UPDATE {self.bot.db.schema}.system SET FORBIDDEN_CHANNELS = $1 WHERE GUILD_ID = $2", value, guild_id)
        self.cached_ForbiddenChannels.cache_clear()


    @lru_cache(maxsize=128, typed=False)
    async def cached_XPLogChannelID(self, guild_id: int):
        res = await self.bot.db.field(f"SELECT XP_LOG_CHANNEL_ID FROM {self.bot.db.schema}.system WHERE GUILD_ID = $1", guild_id)
        return res
    
    async def set_XPLogChannelID(self, value: int, guild_id: int):
        await self.bot.db.execute(f"UPDATE {self.bot.db.schema}.system SET XP_LOG_CHANNEL_ID = $1 WHERE GUILD_ID = $2", value, guild_id)
        self.cached_XPLogChannelID.cache_clear()


    @lru_cache(maxsize=128, typed=False)
    async def cached_LevelUpMessageChannelID(self, guild_id: int):
        res = await self.bot.db.field(f"SELECT LEVEL_UP_MESSAGE_CHANNEL_ID FROM {self.bot.db.schema}.system WHERE GUILD_ID = $1", guild_id)
        return res
    
    async def set_LevelUpMessageChannelID(self, value: int, guild_id: int):
        await self.bot.db.execute(f"UPDATE {self.bot.db.schema}.system SET LEVEL_UP_MESSAGE_CHANNEL_ID = $1 WHERE GUILD_ID = $2", value, guild_id)
        self.cached_LevelUpMessageChannelID.cache_clear()
        

def clearAllCache() -> None:
    for name, func in CacheManager.__dict__.items():
        if name.startswith("cached_"):
            func.cache_clear()