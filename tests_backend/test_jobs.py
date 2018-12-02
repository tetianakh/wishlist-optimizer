from wishlist_optimizer.jobs import get_pricing
from wishlist_optimizer.mkm_api import MkmApi

from unittest import mock
import pytest

from tests_backend.conftest import amock


def get_wishlist(quantity=1, languages=None, expansions=None, foil=None):
    return {
        'cards': [
            {
                'name': 'Shock',
                'quantity': quantity,
                'languages': languages or [],
                'expansions': expansions or [],
                'foil': foil
            }
        ]
    }


LANGS_MAP = {
    'English': 1,
    'French': 2,
    'German': 3,
}


def echo(arg):
    return arg


@mock.patch.object(MkmApi, 'get_product_ids', return_value=amock([]))
def test_no_products_found(mock_api, db_session, app):
    result = get_pricing(get_wishlist())
    assert result['error'] is None
    assert result['result'] == []


@mock.patch.object(MkmApi, 'get_product_ids')
@mock.patch.object(MkmApi, 'get_articles')
def test_single_product_single_article(
        mock_get_articles, mock_get_pids, db_session, app):
    mock_get_pids.return_value = amock([123])
    mock_get_articles.return_value = amock([
        {
            'language': 1,
            'price': 0.1,
            'seller_username': 'seller',
            'seller_url': 'seller_url',
            'seller_id': 'seller_id',
            'seller_country': 'AT',
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
            'total_price': 0.1,
            'seller_country': 'AT',

        }
    ]


@mock.patch.object(MkmApi, 'get_product_ids')
@mock.patch.object(MkmApi, 'get_articles')
def test_gets_cards_from_multiple_articles(
        mock_get_articles, mock_get_pids, db_session, app):
    mock_get_pids.return_value = amock([123])
    mock_get_articles.return_value = amock([
        {
            'language': 1,
            'price': 0.5,
            'seller_username': 'seller',
            'seller_url': 'seller_url',
            'seller_id': 'seller_id',
            'count': 2,
            'seller_country': 'AT',
            'id': 456,
        },
        {
            'language': 1,
            'price': 0.1,
            'seller_username': 'seller',
            'seller_country': 'AT',
            'seller_url': 'seller_url',
            'seller_id': 'seller_id',
            'seller_country': 'AT',
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
        mock_get_articles, mock_get_pids, db_session, app):
    mock_get_pids.return_value = amock([123])
    mock_get_articles.return_value = amock([
        {
            'language': 1,  # English only
            'price': 0.1,
            'seller_username': 'seller',
            'seller_url': 'seller_url',
            'seller_id': 'seller_id',
            'seller_country': 'AT',
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
            'seller_country': 'AT',
            'total_count': 1,
            'total_price': 0.1
        }
    ]


@mock.patch.object(MkmApi, 'get_product_ids')
@mock.patch.object(MkmApi, 'get_articles')
def test_handles_duplicated_card_names_in_wishlist(
        mock_get_articles, mock_get_pids, db_session, app):
    mock_get_pids.return_value = amock([123])
    mock_get_articles.return_value = amock([
        {
            'language': 1,
            'price': 0.1,
            'seller_username': 'seller',
            'seller_url': 'seller_url',
            'seller_id': 'seller_id',
            'seller_country': 'AT',
            'count': 2,  # only two shocks are available
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
            'seller_country': 'AT',
            'total_count': 2,  # only 2 were available
            'total_price': 0.2
        }
    ]


@mock.patch.object(MkmApi, 'get_product_ids', return_value=amock([]))
def test_filters_product_ids_by_expansion(mock_pids, db_session, app):
    expansions = ['Dominaria', ]
    get_pricing(get_wishlist(expansions=expansions))
    mock_pids.assert_called_once_with('Shock', expansions)


@mock.patch.object(MkmApi, 'get_product_ids')
@mock.patch.object(MkmApi, 'get_articles')
def test_calls_get_articles_with_correct_params_with_language(
        mock_get_articles, mock_get_pids, db_session, app):
    mock_get_pids.return_value = amock([123])
    mock_get_articles.return_value = amock([])

    get_pricing(get_wishlist(languages=['English'], foil=True))
    mock_get_articles.assert_called_once_with(123, language_id=1, foil=True)


@mock.patch.object(MkmApi, 'get_product_ids')
@mock.patch.object(MkmApi, 'get_articles')
def test_calls_get_articles_with_correct_params_without_language(
        mock_get_articles, mock_get_pids, db_session, app):
    mock_get_pids.return_value = amock([123])
    mock_get_articles.return_value = amock([])
    get_pricing(get_wishlist(foil=True))
    mock_get_articles.assert_called_once_with(123, foil=True)


@mock.patch.object(MkmApi, 'get_product_ids')
@mock.patch.object(MkmApi, 'get_articles')
def test_gets_correct_quantity_of_foil_cards(
        mock_get_articles, mock_get_pids, db_session, app):
    mock_get_pids.return_value = amock([123])

    async def get_articles(product_id, foil=None):
        if foil:
            return [{
                'language': 1,
                'price': 10,  # foil
                'seller_username': 'seller',
                'seller_url': 'seller_url',
                'seller_id': 'seller_id',
                'seller_country': 'AT',
                'count': 5,
                'id': 789,
            }]
        return [{
            'language': 1,
            'price': 0.1,
            'seller_username': 'seller',
            'seller_url': 'seller_url',
            'seller_id': 'seller_id',
            'seller_country': 'AT',
            'count': 20,
            'id': 456,
        }]

    mock_get_articles.side_effect = get_articles
    wishlist = get_wishlist(foil=False, quantity=10)
    wishlist['cards'].append({
        'name': 'Shock',
        'quantity': 5,
        'languages': [],
        'expansions': [],
        'foil': True
    })
    result = get_pricing(wishlist)
    print(result)
    assert result['error'] is None
    assert result['result'][0]['total_count'] == 15
    assert result['result'][0]['total_price'] == 51


@mock.patch.object(MkmApi, 'get_product_ids')
@mock.patch.object(MkmApi, 'get_articles')
def test_reportsc_cards_that_no_seller_has_as_missing(
        mock_get_articles, mock_get_pids, db_session, app):
    mock_get_pids.return_value = amock([123])

    async def get_articles(product_id, language_id=None, foil=None):
        if language_id == 1:
            return [{
                'language': 1,
                'price': 10,
                'seller_username': 'seller',
                'seller_url': 'seller_url',
                'seller_id': 'seller_id',
                'seller_country': 'AT',
                'count': 4,
                'id': 789,
            }]
        return []  # no cards in other languages

    mock_get_articles.side_effect = get_articles
    wishlist = get_wishlist(foil=False, quantity=4, languages=['English'])
    wishlist['cards'].append({
        'name': 'Missing card',
        'quantity': 4,
        'languages': ['German'],
        'expansions': [],
    })
    result = get_pricing(wishlist)
    print(result)
    assert result['error'] is None
    assert result['result'][0]['total_count'] == 4
    assert result['result'][0]['total_price'] == 40
    assert result['result'][0]['missing_cards'] == [
        {'name': 'Missing card', 'quantity': 4}
    ]
