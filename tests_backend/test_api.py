import json

from wishlist_optimizer.models import Wishlist, User, Card

from . import USER_ID

import pytest


@pytest.fixture
def user(db_session):
    u = User(sub='123abc', id=USER_ID)
    db_session.add(u)
    db_session.commit()
    return u


def get_wishlist():
    return {
        'name': 'name',
        'cards': [
            {
                'name': 'Shock',
                'languages': ['English'],
                'expansions': ['Dominaria'],
                'quantity': 4
            },
        ]
    }


def create_wishlist(client, wishlist=None):
    return client.post(
        '/api/wishlists',
        data=json.dumps(wishlist or get_wishlist()),
        headers={
            'Content-Type': 'application/json',
        }
    ).get_json()['wishlist']


def test_save_empty_wishlist_via_api(db_session, client, user):
    wishlist = {
        'name': 'name',
        'cards': []
    }
    resp = client.post(
        '/api/wishlists',
        data=json.dumps(wishlist),
        headers={
            'Content-Type': 'application/json',
        }
    )
    assert resp.status == '201 CREATED'
    result = resp.get_json()['wishlist']
    assert result['cards'] == []
    assert result['name'] == 'name'
    assert db_session.query(Wishlist).get(result['id']).to_dict() == result


def test_save_wishlist_with_cards(db_session, client, user):
    resp = client.post(
        '/api/wishlists',
        data=json.dumps(get_wishlist()),
        headers={
            'Content-Type': 'application/json',
        }
    )
    assert resp.status == '201 CREATED'
    result = resp.get_json()['wishlist']
    card = result['cards'][0]
    assert len(result['cards']) == 1
    assert card['name'] == 'Shock'
    assert card['languages'] == ['English']
    assert card['expansions'] == ['Dominaria']
    assert result['name'] == 'name'
    assert db_session.query(Wishlist).get(result['id']).to_dict() == result


def test_can_retrieve_wishlist(db_session, client, user):
    wishlist_id = client.post(
        '/api/wishlists',
        data=json.dumps(get_wishlist()),
        headers={
            'Content-Type': 'application/json',
        }
    ).get_json()['wishlist']['id']
    resp = client.get(f'/api/wishlists/{wishlist_id}')
    assert resp


def test_delete_wishlist(db_session, client, user):
    wishlist_id = create_wishlist(client)['id']
    resp = client.delete(f'/api/wishlists/{wishlist_id}')
    assert resp.status == '204 NO CONTENT'
    assert db_session.query(Wishlist).get(wishlist_id) is None


def test_add_card(db_session, client, user):
    empty_wishlist = {
        'name': 'name',
        'cards': []
    }
    wishlist_id = create_wishlist(client, empty_wishlist)['id']
    card = {
        'name': 'Shock',
        'languages': ['English'],
        'quantity': 2,
        'expansions': ['Dominaria']
    }
    client.post(f'/api/wishlists/{wishlist_id}/cards',
                data=json.dumps(card),
                content_type='application/json')
    cards = db_session.query(Wishlist).get(wishlist_id).cards
    assert len(cards) == 1
    card = cards[0].to_dict()
    assert cards[0].name == 'Shock'
    assert card['languages'] == ['English']
    assert card['expansions'] == ['Dominaria']
    assert card['quantity'] == 2
    assert card['min_condition'] is None


def test_bulk_add_cards(db_session, client, user):
    empty_wishlist = {
        'name': 'name',
        'cards': []
    }
    wishlist_id = create_wishlist(client, empty_wishlist)['id']
    cards = [
        {
            'name': 'Shock',
            'quantity': 2,
        },
        {
            'name': 'Bomat',
            'quantity': 4
        }
    ]
    client.post(f'/api/wishlists/{wishlist_id}/cards_batch',
                data=json.dumps({'cards': cards}),
                content_type='application/json')
    cards = db_session.query(Wishlist).get(wishlist_id).cards
    assert len(cards) == 2
    assert cards[0].name == 'Shock'
    assert cards[0].quantity == 2
    assert cards[1].name == 'Bomat'
    assert cards[1].quantity == 4


def test_update_card(db_session, client, user):
    wishlist = create_wishlist(client)
    wishlist_id = wishlist['id']
    old_card = wishlist['cards'][0]
    card_id = old_card['id']
    assert old_card['name'] == 'Shock'
    assert old_card['quantity'] == 4
    assert old_card['languages'] == ['English']
    assert old_card['expansions'] == ['Dominaria']
    new_card = {
        'name': 'Bomat',
        'quantity': 4,
        'languages': ['German'],
        'expansions': ['Kaladesh'],
        'foil': True
    }
    url = f'/api/wishlists/{wishlist_id}/cards/{card_id}'
    resp = client.put(
        url, data=json.dumps(new_card), content_type='application/json'
    )
    assert resp.status == '200 OK'
    updated_card = db_session.query(Card).get(card_id).to_dict()
    assert updated_card['name'] == new_card['name']
    assert updated_card['quantity'] == new_card['quantity']
    assert updated_card['languages'] == new_card['languages']
    assert updated_card['expansions'] == new_card['expansions']
    assert updated_card['foil'] is True


@pytest.mark.parametrize(['foil', 'expected'], (
    (True, True),
    (False, False),
    (None, None),
    ('foo', None)
))
def test_foil(foil, expected, db_session, client, user):
    wishlist = create_wishlist(client)
    wishlist_id = wishlist['id']
    card = wishlist['cards'][0]
    card['foil'] = foil
    card_id = card['id']
    url = f'/api/wishlists/{wishlist_id}/cards/{card_id}'
    result = client.put(
        url, data=json.dumps(card), content_type='application/json'
    ).get_json()['card']
    assert result['foil'] is expected


def test_rename_wishlist(db_session, client, user):
    empty_wishlist = {
        'name': 'old name',
        'cards': []
    }
    wishlist_id = create_wishlist(client, empty_wishlist)['id']
    resp = client.put(
        f'/api/wishlists/{wishlist_id}/name',
        data=json.dumps({'name': 'new name'}),
        content_type='application/json'
    )
    wishlist = db_session.query(Wishlist).get(wishlist_id)
    assert resp.status == '200 OK'
    assert wishlist.name == 'new name'
    assert resp.get_json()['name'] == 'new name'


@pytest.mark.parametrize(['min_cond', 'exp'], (
    ('EX', 'EX'),
    ('foo', None)
))
def test_add_card_with_min_condition(db_session, client, user, min_cond, exp):
    empty_wishlist = {
        'name': 'name',
        'cards': []
    }
    wishlist_id = create_wishlist(client, empty_wishlist)['id']
    card = {
        'name': 'Shock',
        'languages': ['English'],
        'quantity': 2,
        'expansions': ['Dominaria'],
        'min_condition': min_cond,
    }
    client.post(f'/api/wishlists/{wishlist_id}/cards',
                data=json.dumps(card),
                content_type='application/json')
    cards = db_session.query(Wishlist).get(wishlist_id).cards
    card = cards[0].to_dict()
    assert card['min_condition'] == exp
