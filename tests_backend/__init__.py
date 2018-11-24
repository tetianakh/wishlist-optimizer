from functools import wraps

import wishlist_optimizer.cache
import wishlist_optimizer.auth
#  monkey patching ttl_cache decorator before other modules are imported

USER_ID = 1


def dummy_cache(ttl):
    def cache(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            return await func(*args, **kwargs)
        return inner
    return cache


def dummy_auth(func):
    @wraps(func)
    def inner(*args, **kwargs):
        return func(USER_ID, *args, **kwargs)
    return inner


wishlist_optimizer.cache.ttl_cache = dummy_cache
wishlist_optimizer.auth.login_required = dummy_auth
