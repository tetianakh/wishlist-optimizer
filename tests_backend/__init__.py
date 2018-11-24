import wishlist_optimizer.cache
#  monkey patching ttl_cache decorator before mkm_api module is imported


def dummy_cache(ttl):
    def cache(func):
        async def inner(*args, **kwargs):
            return await func(*args, **kwargs)
        return inner
    return cache


wishlist_optimizer.cache.ttl_cache = dummy_cache
