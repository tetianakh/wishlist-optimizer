import pytest
from unittest import mock

from tests_backend.conftest import amock


from wishlist_optimizer.mkm_api import HttpClient, MkmApi  # noqa


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


@pytest.yield_fixture
def http_client(event_loop):
    with mock.patch.object(HttpClient, 'get'):
        yield HttpClient(event_loop, {'url': 'http://some.url'})


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
