"""

 @lru_cache(maxsize=128, typed=False)

"""
from functools import lru_cache


@lru_cache(maxsize=128, typed=False)
async def smth():
    pass

@lru_cache(maxsize=128, typed=False)
def sth2():
    pass
