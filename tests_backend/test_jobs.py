import asyncio

from wishlist_optimizer.jobs import get_pricing
from wishlist_optimizer.mkm_api import MkmApi
from wishlist_optimizer.languages_service import LanguagesService

from unittest import mock
import pytest


def get_wishlist():
    return {
        'cards': [
            {
                'name': 'Shock',
                'quantity': 1,
                'languages': [],
                'expansions': [],
            }
        ]
    }


def dummy_cache(ttl):
    def cache(func):
        async def inner(*args, **kwargs):
            return await func(*args, **kwargs)
        return inner
    return cache


def amock(result):
  f = asyncio.Future()
  f.set_result(result)
  return f


LANGS_MAP = {
    'English': 1,
    'French': 2,
    'German': 3,
}


@mock.patch.object(MkmApi, 'get_product_ids', return_value=amock([]))
@mock.patch.object(LanguagesService, 'get_language_mkm_ids', return_value=LANGS_MAP)  # noqa
def test_no_products_found(mock_langs, mock_http, app):
    result = get_pricing(get_wishlist())
    assert result['error'] == None
    assert result['result'] == []
