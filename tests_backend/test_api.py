from wishlist_optimizer.wishlist_service import WishlistService
from wishlist_optimizer.languages_service import LanguagesService
from wishlist_optimizer.expansions_service import ExpansionService

from wishlist_optimizer.models import Wishlist, User

import pytest


@pytest.fixture
def wishlist_service():
    languages_service = LanguagesService()
    expansion_service = ExpansionService()
    return WishlistService(languages_service, expansion_service)


def test_save_empty_wishlist(db_session, wishlist_service):
    user = User(sub='123abc')
    db_session.add(user)
    db_session.commit()
    wishlist = {
        'name': 'name',
        'cards': []
    }
    result = wishlist_service.create_wishlist(user.id, wishlist)
    saved = db_session.query(Wishlist).get(result['id'])
    assert saved.name == 'name'
