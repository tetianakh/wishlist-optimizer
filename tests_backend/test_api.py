import json

from wishlist_optimizer.models import Wishlist, User

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
    ).get_json()['wishlist']['id']


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
    wishlist_id = create_wishlist(client)
    resp = client.delete(f'/api/wishlists/{wishlist_id}')
    assert resp.status == '204 NO CONTENT'
    assert db_session.query(Wishlist).get(wishlist_id) is None


def test_add_card(db_session, client, user):
    empty_wishlist = {
        'name': 'name',
        'cards': []
    }
    wishlist_id = create_wishlist(client, empty_wishlist)
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


def test_bulk_add_cards(db_session, client, user):
    empty_wishlist = {
        'name': 'name',
        'cards': []
    }
    wishlist_id = create_wishlist(client, empty_wishlist)
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
