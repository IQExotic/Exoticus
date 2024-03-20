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
    async def cached_dbselect(self, column: str, guild_id: int):
        res = await self.bot.db.field(f"SELECT {column} FROM {self.bot.db.schema}.system WHERE GUILD_ID = {guild_id}")
        return res
    
    async def set_dbupdate(self, column: str, value: int, guild_id: int):
        await self.bot.db.execute(f"UPDATE {self.bot.db.schema}.system SET {column} = {value} WHERE GUILD_ID = {guild_id}")
        self.cached_dbselect.cache_clear()
    
    async def insert_dbrecord(self, column: str, value: int, guild_id: int):
        await self.bot.db.execute(f"INSERT INTO {self.bot.db.schema}.system ({column}, GUILD_ID) VALUES ({value}, {guild_id})")
        self.cached_dbselect.cache_clear()


def clearAllCache() -> None:
    for name, func in CacheManager.__dict__.items():
        if name.startswith("cached_"):
            func.cache_clear()