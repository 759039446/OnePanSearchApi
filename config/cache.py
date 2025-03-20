import json

from cachetools import TTLCache
import shelve

# 创建一个TTLCache实例，最大容量为100，每个缓存项的过期时间为3600秒（1小时）
cover_cache = TTLCache(maxsize=100, ttl=3600)


def contain_cover_cache(key):
    return key in cover_cache


def get_cover_cache(key):
    return cover_cache[key]


def set_cover_cache(key, value):
    cover_cache[key] = value
    with shelve.open('quark_hot.db') as db:
        db[tuple_to_key(key)] = value


def tuple_to_key(t):
    return json.dumps(t, sort_keys=True)


def key_to_tuple(key):
    return tuple(json.loads(key))


def get_shelve_quark_hot(key):
    with shelve.open('quark_hot.db') as db:
        return db.get(tuple_to_key(key), {})
