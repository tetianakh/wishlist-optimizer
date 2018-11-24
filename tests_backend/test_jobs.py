import asyncio

from wishlist_optimizer.jobs import get_pricing
from wishlist_optimizer.mkm_api import MkmApi
from wishlist_optimizer.languages_service import LanguagesService

from unittest import mock
import pytest


def get_wishlist(quantity=1, languages=None, expansions=None):
    return {
        'cards': [
            {
                'name': 'Shock',
                'quantity': quantity,
                'languages': languages or [],
                'expansions': expansions or [],
            }
        ]
    }


def amock(result):
    f = asyncio.Future()
    f.set_result(result)
    return f


LANGS_MAP = {
    'English': 1,
    'French': 2,
    'German': 3,
}


@pytest.yield_fixture
def mock_langs():
    with mock.patch.object(
            LanguagesService, 'get_language_mkm_ids', return_value=LANGS_MAP
            ) as m:
        yield m


@mock.patch.object(MkmApi, 'get_product_ids', return_value=amock([]))
def test_no_products_found(mock_api, mock_langs, app):
    result = get_pricing(get_wishlist())
    assert result['error'] is None
    assert result['result'] == []


@mock.patch.object(MkmApi, 'get_product_ids')
@mock.patch.object(MkmApi, 'get_articles')
def test_single_product_single_article(
        mock_get_articles, mock_get_pids, mock_langs, app):
    mock_get_pids.return_value = amock([123])
    mock_get_articles.return_value = amock([
        {
            'language': 1,
            'price': 0.1,
            'seller_username': 'seller',
            'seller_url': 'seller_url',
            'seller_id': 'seller_id',
            'count': 1,
            'id': 456,
        }
    ])
    result = get_pricing(get_wishlist())
    assert result['error'] is None
    assert result['result'] == [
        {
            'missing_cards': [],
            'seller_id': 'seller_id',
            'seller_url': 'seller_url',
            'seller_username': 'seller',
            'total_count': 1,
            'total_price': 0.1
        }
    ]


@mock.patch.object(MkmApi, 'get_product_ids')
@mock.patch.object(MkmApi, 'get_articles')
def test_gets_cards_from_multiple_articles(
        mock_get_articles, mock_get_pids, mock_langs, app):
    mock_get_pids.return_value = amock([123])
    mock_get_articles.return_value = amock([
        {
            'language': 1,
            'price': 0.5,
            'seller_username': 'seller',
            'seller_url': 'seller_url',
            'seller_id': 'seller_id',
            'count': 2,
            'id': 456,
        },
        {
            'language': 1,
            'price': 0.1,
            'seller_username': 'seller',
            'seller_url': 'seller_url',
            'seller_id': 'seller_id',
            'count': 1,
            'id': 456,
        }
    ])
    result = get_pricing(get_wishlist(quantity=2))
    assert result['error'] is None
    assert result['result'][0]['total_count'] == 2
    assert result['result'][0]['total_price'] == 0.6


@mock.patch.object(MkmApi, 'get_product_ids')
@mock.patch.object(MkmApi, 'get_articles')
def test_reports_missing_cards(
        mock_get_articles, mock_get_pids, mock_langs, app):
    mock_get_pids.return_value = amock([123])
    mock_get_articles.return_value = amock([
        {
            'language': 1,  # English only
            'price': 0.1,
            'seller_username': 'seller',
            'seller_url': 'seller_url',
            'seller_id': 'seller_id',
            'count': 1,
            'id': 456,
        }
    ])
    result = get_pricing(get_wishlist(quantity=2, languages=['German']))
    assert result['error'] is None
    assert result['result'] == [
        {
            'missing_cards': [{'name': 'Shock', 'quantity': 1}],
            'seller_id': 'seller_id',
            'seller_url': 'seller_url',
            'seller_username': 'seller',
            'total_count': 1,
            'total_price': 0.1
        }
    ]


@mock.patch.object(MkmApi, 'get_product_ids')
@mock.patch.object(MkmApi, 'get_articles')
def test_handles_duplicated_card_names_in_wishlist(
        mock_get_articles, mock_get_pids, mock_langs, app):
    mock_get_pids.return_value = amock([123])
    mock_get_articles.return_value = amock([
        {
            'language': 1,  # English only
            'price': 0.1,
            'seller_username': 'seller',
            'seller_url': 'seller_url',
            'seller_id': 'seller_id',
            'count': 2,
            'id': 456,
        }
    ])
    wishlist = get_wishlist()
    wishlist['cards'].extend([
        {'name': 'Shock', 'languages': [], 'expansions': [], 'quantity': 1},
        {'name': 'Shock', 'languages': [], 'expansions': [], 'quantity': 1}
    ])  # effectively searching for 3 shocks
    result = get_pricing(wishlist)
    assert result['error'] is None
    assert result['result'] == [
        {
            'missing_cards': [{'name': 'Shock', 'quantity': 1}],
            'seller_id': 'seller_id',
            'seller_url': 'seller_url',
            'seller_username': 'seller',
            'total_count': 2,  # only 2 were available
            'total_price': 0.2
        }
    ]
