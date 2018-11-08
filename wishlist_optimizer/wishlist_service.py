import logging
from wishlist_optimizer.models import Wishlist, Card, db, Language

logger = logging.getLogger(__name__)


class WishlistService:
    def __init__(self, languages_service):
        self._languages_service = languages_service

    def get_wishlists(self):
        return [w.to_dict() for w in Wishlist.query.all()]

    def get_wishlist(self, wishlist_id):
        return Wishlist.query.get(wishlist_id).to_dict()

    def create_wishlist(self, data):
        logger.debug("Creating wishlist: %s", data)
        wishlist = self._create_wishlist(data)
        self._save(wishlist)
        return wishlist.to_dict()

    def _create_wishlist(self, data):
        wishlist = Wishlist(name=data['name'])
        wishlist.cards = [self._create_card(c) for c in data['cards']]
        return wishlist

    def add_card(self, wishlist_id, data):
        logger.debug("Adding card to wishlist %s: %s", wishlist_id, data)
        wishlist = Wishlist.query.get(wishlist_id)
        card = self._create_card(data)
        wishlist.cards.append(card)
        db.session.commit()
        return card.to_dict()

    def _create_card(self, data):
        languages = self._languages_service.find_by_name(data['languages'])
        return Card(
            name=data['name'].title(),
            quantity=data['quantity'],
            languages=[l for l in languages if l]
        )

    def remove_card(self, card_id):
        logger.debug("Removing card %s", card_id)
        card = Card.query.get(card_id)
        db.session.delete(card)
        db.session.commit()

    def update_card(self, card_id, data):
        logger.debug("Updating card %s: %s", card_id, data)
        card = Card.query.get(card_id)
        card.name = data['name']
        card.quantity = data['quantity']
        db.session.commit()
        return card.to_dict()

    def _save(self, obj):
        db.session.add(obj)
        db.session.commit()
