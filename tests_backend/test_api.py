import json
import time

import jwt

from wishlist_optimizer.wishlist_service import WishlistService
from wishlist_optimizer.languages_service import LanguagesService
from wishlist_optimizer.expansions_service import ExpansionService

from wishlist_optimizer.models import Wishlist, User

from . import USER_ID

import pytest


@pytest.fixture
def user(db_session):
    u = User(sub='123abc', id=USER_ID)
    db_session.add(u)
    db_session.commit()
    return u


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
        wishlist = {
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
        resp = client.post(
            '/api/wishlists',
            data=json.dumps(wishlist),
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