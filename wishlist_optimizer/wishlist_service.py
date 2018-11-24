import logging
from wishlist_optimizer.models import Wishlist, Card, db


logger = logging.getLogger(__name__)


class ObjectNotFound(Exception):
    pass


class WishlistService:
    def __init__(self, languages_service, expansion_service):
        self._languages_service = languages_service
        self._expansion_service = expansion_service

    def get_wishlists(self, user_id):
        return [
            w.to_dict() for w
            in Wishlist.query.filter_by(user_id=user_id).all()
        ]

    def get_wishlist(self, user_id, wishlist_id):
        wl = Wishlist.query.get(wishlist_id)
        if not wl or wl.user_id != user_id:
            raise ObjectNotFound
        return wl.to_dict() if wl else None

    def create_wishlist(self, user_id, data):
        logger.debug("Creating wishlist: %s", data)
        wishlist = self._create_wishlist(user_id, data)
        self._save(wishlist)
        return wishlist.to_dict()

    def _create_wishlist(self, user_id, data):
        wishlist = Wishlist(name=data['name'], user_id=user_id)
        wishlist.cards = [self._create_card(c) for c in data['cards']]
        return wishlist

    def add_card(self, user_id, wishlist_id, data):
        logger.debug("Adding card to wishlist %s: %s", wishlist_id, data)
        wishlist = self._get_wishlist(user_id, wishlist_id)
        card = self._create_card(data)
        wishlist.cards.append(card)
        db.session.commit()
        return card.to_dict()

    def add_cards(self, user_id, wishlist_id, data):
        logger.info('Creating a batch of cards: %s', data)
        card_data = data.get('cards', [])
        new_cards = [self._create_card(d) for d in card_data]
        wishlist = self._get_wishlist(user_id, wishlist_id)
        wishlist.cards.extend(new_cards)
        db.session.commit()
        return wishlist.to_dict()

    def _get_wishlist(self, user_id, wishlist_id):
        wishlist = Wishlist.query.get(wishlist_id)
        if wishlist.user_id != user_id:
            raise ObjectNotFound
        return wishlist

    def _create_card(self, data):
        languages = self._languages_service.find_by_names(
            data.get('languages', [])
        )
        expansions = self._expansion_service.find_by_names(
            data.get('expansions', [])
        )
        return Card(
            name=data['name'].title(),
            quantity=data['quantity'],
            languages=languages,
            expansions=expansions,
        )

    def remove_card(self, user_id, card_id):
        logger.debug("Removing card %s", card_id)
        card = Card.query.get(card_id)
        if not card or card.wishlist.user_id != user_id:
            raise ObjectNotFound
        db.session.delete(card)
        db.session.commit()

    def remove_wishlist(self, user_id, wishlist_id):
        logger.info("Removing wishlist %s", wishlist_id)
        wishlist = Wishlist.query.get(wishlist_id)
        if wishlist.user_id != user_id:
            raise ObjectNotFound
        db.session.delete(wishlist)
        db.session.commit()

    def update_card(self, user_id, card_id, data):
        logger.debug("Updating card %s: %s", card_id, data)
        card = Card.query.get(card_id)
        if card.wishlist.user_id != user_id:
            raise ObjectNotFound
        card.name = data['name']
        card.quantity = data['quantity']
        card.languages = self._languages_service.find_by_names(
            data.get('languages', [])
        )
        card.expansions = self._expansion_service.find_by_names(
            data.get('expansions', [])
        )
        db.session.commit()
        return card.to_dict()

    def _save(self, obj):
        db.session.add(obj)
        db.session.commit()
