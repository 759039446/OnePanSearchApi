from cachetools import TTLCache

# 创建一个TTLCache实例，最大容量为100，每个缓存项的过期时间为3600秒（1小时）
cover_cache = TTLCache(maxsize=100, ttl=3600)


def get_cover_cache():
    return cover_cache
