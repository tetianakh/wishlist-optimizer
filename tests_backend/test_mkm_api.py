import pytest
from unittest import mock

from tests_backend.conftest import amock


from wishlist_optimizer.mkm_api import HttpClient, MkmApi


def get_product(
        product_id=123,
        name='Shock',
        expansion='Kaladesh',
        category='Magic Single'):
    return {
        'idProduct': product_id,
        'expansionName': expansion,
        'categoryName': category,
        'enName': name
    }


def get_article(article_id=123, language_id=1, price=0.1, count=1):
    return {
        'idArticle': article_id,
        'language': {'idLanguage': language_id},
        'price': price,
        'seller': {
            'username': 'some_seller',
            'idUser': 'some_id',
        },
        'count': count,
    }


@pytest.yield_fixture
def http_client(event_loop):
    with mock.patch.object(HttpClient, 'get'):
        client = HttpClient(event_loop, {'url': 'http://some.url'})
        yield client
        event_loop.run_until_complete(client.close())


@pytest.mark.parametrize(['name'], (
    ('Fire',),
    ('Ice',),
    ('Fire Ice',),
    ('Fire / Ice',),
    ('Fire/Ice',),
    ('Fire//Ice',),
    ('Fire // Ice',)
))
@pytest.mark.asyncio
async def test_handles_split_cards(name, http_client):
    response = [get_product(name='Fire // Ice')]
    http_client.get.return_value = amock(response)
    api = MkmApi(http_client)
    result = await api.get_product_ids(name, expansions=None)
    assert result == [123]


@pytest.mark.parametrize(['name'], (
    ('Search for Azcanta',),
    ('Azcanta, the Sunken Ruin',),
    ('Search for Azcanta Azcanta, the Sunken Ruin',),
    ('Search for Azcanta / Azcanta, the Sunken Ruin',),
    ('Search for Azcanta/Azcanta, the Sunken Ruin',),
    ('Search for Azcanta//Azcanta, the Sunken Ruin',),
    ('Search for Azcanta // Azcanta, the Sunken Ruin',)
))
@pytest.mark.asyncio
async def test_handles_flip_cards(name, http_client):
    response = [
        get_product(name='Search for Azcanta / Azcanta, the Sunken Ruin')
    ]
    http_client.get.return_value = amock(response)
    api = MkmApi(http_client)
    result = await api.get_product_ids(name, expansions=None)
    assert result == [123]


@pytest.mark.asyncio
async def test_filters_out_product_that_are_not_cards(http_client):
    response = amock([
        get_product(category='Magic Single', product_id=123),
        get_product(category='some other category', product_id=456),
    ])
    http_client.get.return_value = response
    api = MkmApi(http_client)
    result = await api.get_product_ids('Shock', expansions=None)
    assert result == [123]


@pytest.mark.parametrize(['name', 'exact'], (
    ('Shock', "false"), ('Opt', "true")
))
@pytest.mark.asyncio
async def test_calls_api_with_correct_params(name, exact, http_client):
    http_client.get.return_value = amock([get_product()])
    api = MkmApi(http_client)
    await api.get_product_ids(name, expansions=None)
    params = {
        'search': name.lower(),
        'exact': exact,
        'idGame': 1
    }
    http_client.get.assert_called_once_with(
        'products/find', params=params, headers={}, field='product'
    )


@pytest.mark.asyncio
async def test_filters_products_by_expansion(http_client):
    response = amock([
        get_product(expansion='Kaladesh', product_id=123),
        get_product(expansion='Dominaria', product_id=456),
        get_product(expansion='Magic 2019', product_id=789),
    ])
    http_client.get.return_value = response
    api = MkmApi(http_client)
    result = await api.get_product_ids(
        'Shock', expansions=['Magic 2019', 'Dominaria']
    )
    assert set(result) == {456, 789}


@pytest.mark.asyncio
async def test_get_article(http_client, app):
    response = amock([get_article()])
    http_client.get.return_value = response
    api = MkmApi(http_client)
    result = await api.get_articles('some_product_id')
    http_client.get.assert_called_once_with(
        'articles/some_product_id',
        params={}, headers={}, field='article'
    )
    assert len(result) == 1
    assert result[0] == {
        'language': 1,
        'price': 0.1,
        'seller_username': 'some_seller',
        'seller_url': 'http://dummy.user.url/some_seller',
        'seller_id': 'some_id',
        'count': 1,
        'id': 123,
    }


@pytest.mark.asyncio
async def test_filters_articles_by_language(http_client, app):
    response = amock([get_article()])
    http_client.get.return_value = response
    api = MkmApi(http_client)
    await api.get_articles('some_product_id', language_id=10)
    params = {'idLanguage': 10}
    http_client.get.assert_called_once_with(
        'articles/some_product_id',
        params=params, headers={}, field='article'
    )


@pytest.mark.parametrize(['foil', 'params'], (
    (True, {'isFoil': 'true'}),
    (False, {'isFoil': 'false'}),
    (None, {})
))
@pytest.mark.asyncio
async def test_filters_articles_by_foil(foil, params, http_client, app):
    response = amock([get_article()])
    http_client.get.return_value = response
    api = MkmApi(http_client)
    await api.get_articles('some_product_id', foil=foil)
    http_client.get.assert_called_once_with(
        'articles/some_product_id',
        params=params, headers={}, field='article'
    )
