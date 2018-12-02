import asyncio
import logging
from collections import defaultdict
from itertools import groupby

from wishlist_optimizer.condition_service import ConditionService
from wishlist_optimizer.expansions_service import ExpansionService

logger = logging.getLogger(__name__)


class MkmPricingService:
    def __init__(self, loop, api, wishlist, languages_service):
        self._languages_service = languages_service
        self._loop = loop
        self._api = api
        self._wishlist = self._prep_wishlist(wishlist)
        logger.info(self._wishlist)
        self._total_card_count = sum(c['quantity'] for c in self._wishlist)
        self._best_prices = {}
        self._missing_cards = {}
        self._used_offers = defaultdict(int)

    def _prep_wishlist(self, cards):
        condition_service = ConditionService()
        expansion_service = ExpansionService()
        return [
            {
                'name': c['name'],
                'quantity': int(c['quantity']),
                'languages': [
                    l.name for l in self._languages_service.find_by_names(
                        c.get('languages', [])
                    )
                ],
                'expansions': [e.name for e in expansion_service.find_by_names(
                    c.get('expansions', [])
                )],
                'foil': c.get('foil'),
                'min_condition': condition_service.get_condition(c)
            }
            for c in cards
        ]

    async def _get_card_articles(self, card, product_id, language_id):
        if language_id is None:
            return card, await self._api.get_articles(
                product_id, foil=card['foil']
            )
        return card, await self._api.get_articles(
            product_id, language_id=language_id, foil=card['foil']
        )

    def _get_card_product_ids(self, cards):
        tasks = [
            self._api.get_product_ids(card['name'], card.get('expansions'))
            for card in cards
        ]
        results = self._loop.run_until_complete(asyncio.gather(*tasks))
        for card, product_ids in zip(cards, results):
            for product_id in product_ids:
                logger.info(
                    'Card: %s, product id: %s', card['name'], product_id
                )
                if card['language_ids']:
                    for lang_id in card['language_ids']:
                        yield card, product_id, lang_id
                else:
                    yield card, product_id, None

    def _get_articles(self, product_ids):
        tasks = [
            self._get_card_articles(c, p_id, l_id)
            for (c, p_id, l_id) in product_ids
        ]
        results = self._loop.run_until_complete(asyncio.gather(*tasks))

        for (card, articles) in results:
            for article in articles:
                yield card, article

    def run(self):
        language_id_map = self._languages_service.get_language_mkm_ids()
        for card in self._wishlist:
            self._set_language_ids(card, language_id_map)

        product_ids = self._get_card_product_ids(self._wishlist)
        articles = self._get_articles(product_ids)
        offers = self._group_by_seller(articles)

        for card in self._wishlist:
            card_key = self._card_to_key(card)
            if card_key not in offers:
                if card_key not in self._missing_cards:
                    card_name = self._get_name_from_key(card_key)
                    self._missing_cards[card_name] = 0
                self._missing_cards[card_name] += card['quantity']
                continue
            self._calculate_best_prices(
                card_key, card['quantity'], offers[card_key]
            )

        result = list(self._best_prices.values())
        result.sort(
            key=lambda a: (a['total_count'], -a['total_price']),
            reverse=True
        )

        best_prices = result[:10]
        self._update_missing_cards(best_prices)
        return best_prices

    def _calculate_best_prices(self, card_key, card_count, offers):
        for seller_id, offer_list in offers.items():

            if seller_id not in self._best_prices:
                self._best_prices[seller_id] = {
                    'total_count': 0,
                    'total_price': 0,
                    'found_cards': {},
                    'seller_id': offer_list[0]['seller_id'],
                    'seller_username': offer_list[0]['seller_username'],
                    'seller_url': offer_list[0]['seller_url'],
                    'seller_country': offer_list[0]['seller_country']
                }

            offer_list = sorted(offer_list, key=lambda o: o['price'])
            found_count = 0
            need_count = card_count
            for offer in offer_list:
                if found_count >= card_count:
                    break
                found = min(need_count, offer['count'] - self._used_offers[offer['id']])  # noqa
                self._best_prices[seller_id]['total_count'] += found
                self._best_prices[seller_id]['total_price'] += found * offer['price']  # noqa
                self._used_offers[offer['id']] += found
                found_count += found
                need_count -= found
            card_name = self._get_name_from_key(card_key)
            if card_name not in self._best_prices[seller_id]['found_cards']:
                self._best_prices[seller_id]['found_cards'][card_name] = 0
            self._best_prices[seller_id]['found_cards'][card_name] += found_count  # noqa

    def _get_name_from_key(self, card_key):
        for name, value in card_key:
            if name == 'name':
                return value
        raise ValueError(f'Failed to get name from key {card_key}')

    def _update_missing_cards(self, best_sellers):
        wishlist = defaultdict(int)
        for card in self._wishlist:
            wishlist[card['name']] += card['quantity']

        for seller in best_sellers:
            # remove found cards for all sellers
            found_cards = seller.pop('found_cards')
            if seller['total_count'] == self._total_card_count:
                # all cards have been found
                seller['missing_cards'] = []
                continue
            missing_cards = dict(self._missing_cards)

            for card_name, need in wishlist.items():
                found = found_cards.get(card_name, 0)
                if found < need:
                    missing_cards[card_name] = need - found

            seller['missing_cards'] = [
                {'name': k, 'quantity': v} for (k, v) in missing_cards.items()
            ]

    def _group_by_seller(self, articles):
        offers = defaultdict(dict)
        # sort data by card name and seller id
        articles = sorted(articles, key=lambda x: (self._card_to_key(x[0]), x[1]['seller_id']))  # noqa
        # group by card name
        for card_key, card_articles in groupby(articles, lambda x: self._card_to_key(x[0])):  # noqa
            # group by seller ID
            for seller_id, articles_by_seller in groupby(card_articles, lambda x: x[1]['seller_id']):  # noqa
                offers[card_key][seller_id] = [a[1] for a in articles_by_seller]  # noqa
        return offers

    @staticmethod
    def _card_to_key(card):
        result = []
        for key, value in card.items():
            if isinstance(value, list):
                value = tuple(value)
            result.append((key, value))
        return tuple(result)

    def _set_language_ids(self, card, language_id_map):
        language_ids = [language_id_map[name] for name in card['languages']]
        if len(language_ids) == len(language_id_map):
            # selecting all is the same as not selecting any
            language_ids = []
        card['language_ids'] = language_ids
