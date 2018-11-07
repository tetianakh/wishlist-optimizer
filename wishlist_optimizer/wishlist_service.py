import logging
from wishlist_optimizer.models import Wishlist, Card, db

logger = logging.getLogger(__name__)


class WishlistService:
    def get_wishlists(self):
        return [w.to_dict() for w in Wishlist.query.all()]

    def get_wishlist(self, wishlist_id):
        return Wishlist.query.get(wishlist_id).to_dict()

    def create_wishlist(self, data):
        logger.debug("Creating wishlist: %s", data)
        wishlist = self._create_wishlist(data)
        self._save(wishlist)
        return wishlist.to_dict()

    def replace_wishlist(self, wishlist_id, data):
        old_wishlist = Wishlist.query.get(wishlist_id)
        new_wishlist = self._create_wishlist(data)
        new_wishlist.id = wishlist_id
        new_wishlist.created_at = old_wishlist.created_at
        db.session.delete(old_wishlist)
        db.session.commit()
        self._save(new_wishlist)
        return new_wishlist.to_dict()

    def _create_wishlist(self, data):
        wishlist = Wishlist(name=data['name'])
        wishlist.cards = [
            Card(name=c['name'].title(), quantity=c['quantity'])
            for c in data['cards']
        ]
        return wishlist

    def add_card(self, wishlist_id, data):
        logger.debug("Adding card to wishlist %s: %s", wishlist_id, data)
        wishlist = Wishlist.query.get(wishlist_id)
        card = Card(name=data['name'], quantity=data['quantity'])
        wishlist.cards.append(card)
        db.session.commit()
        return card.to_dict()

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
