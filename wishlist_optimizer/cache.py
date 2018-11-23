from functools import wraps
import pickle

from wishlist_optimizer.redis import get_connection


def ttl_cache(ttl):
    def cache(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            # do not pickle 'self' arg
            key = '{}:{}'.format(
                func.__name__, pickle.dumps([args[1:], kwargs])
            )
            conn = get_connection()
            cached = conn.get(key)
            if cached:
                return pickle.loads(cached)
            result = await func(*args, **kwargs)
            conn.set(key, pickle.dumps(result), ttl)
            return result
        return inner
    return cache
