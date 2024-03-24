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
    async def cached_dbselect(self, query):
        res = await self.bot.db.field(query)
        return res
    
    async def execute_update(self, query):
        await self.bot.db.execute(query)
        self.cached_dbselect.cache_clear()


def clearAllCache() -> None:
    for name, func in CacheManager.__dict__.items():
        if name.startswith("cached_"):
            func.cache_clear()