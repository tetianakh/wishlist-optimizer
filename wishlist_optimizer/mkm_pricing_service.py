import asyncio
import logging
import time
from collections import defaultdict

logger = logging.getLogger(__name__)


class MkmPricingService:
    def __init__(self, loop, api, wishlist, languages_service):
        self._loop = loop
        self._api = api
        self._wishlist = [
            {
                'name': c['name'],
                'quantity': int(c['quantity']),
                'languages': c.get('languages', []),
                'expansions': c.get('expansions')
            }
            for c in wishlist
        ]
        self._total_card_count = sum(c['quantity'] for c in self._wishlist)
        self._languages_service = languages_service
        self._best_prices = {}
        self._missing_cards = {}

    async def _get_card_articles(self, card, product_id, language_id):
        if language_id is None:
            return card, await self._api.get_articles(product_id)
        return card, await self._api.get_articles(product_id, language_id)

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
        start = time.time()
        language_id_map = self._languages_service.get_language_mkm_ids()
        for card in self._wishlist:
            self._set_language_ids(card, language_id_map)

        product_ids = self._get_card_product_ids(self._wishlist)
        articles = self._get_articles(product_ids)

        offers = self._group_by_seller(articles)

        # for card_name, card_offers in offers.items():
        for card in self._wishlist:
            name = card['name']
            if name not in offers:
                if name not in self._missing_cards:
                    self._missing_cards[name] = 0
                self._missing_cards[name] += card['quantity']
                continue
            self._calculate_best_prices(
                name, card['quantity'], offers[name]
            )

        result = list(self._best_prices.values())
        result.sort(
            key=lambda a: (a['total_count'], -a['total_price']),
            reverse=True
        )
        logger.info('FINISH run, lasted %s', time.time() - start)

        best_prices = result[:10]
        self._update_missing_cards(best_prices)
        return best_prices

    def _calculate_best_prices(self, card_name, card_count, offers):
        for seller_id, offer_list in offers.items():
            if seller_id not in self._best_prices:
                self._best_prices[seller_id] = {
                    'total_count': 0,
                    'total_price': 0,
                    'found_cards': {},
                    'seller_id': offer_list[0]['seller_id'],
                    'seller_username': offer_list[0]['seller_username'],
                    'seller_url': offer_list[0]['seller_url']
                }

            offer_list = sorted(offer_list, key=lambda o: o['price'])
            found_count = 0
            need_count = card_count
            for offer in offer_list:
                if found_count >= card_count:
                    break
                found = min(need_count, offer['count'])
                self._best_prices[seller_id]['total_count'] += found
                self._best_prices[seller_id]['total_price'] += found * offer['price']  # noqa
                found_count += found
                need_count -= found
            if card_name not in self._best_prices[seller_id]['found_cards']:
                self._best_prices[seller_id]['found_cards'][card_name] = 0
            self._best_prices[seller_id]['found_cards'][card_name] += found_count  # noqa

    def _update_missing_cards(self, best_sellers):
        wishlist = defaultdict(int)
        for card in self._wishlist:
            wishlist[card['name']] += card['quantity']

        for seller in best_sellers:
            if seller['total_count'] == self._total_card_count:
                # all cards have been found
                seller['missing_cards'] = []
                continue
            missing_cards = dict(self._missing_cards)
            found_cards = seller.pop('found_cards')
            for card_name, need in wishlist.items():
                found = found_cards.get(card_name, 0)
                if found < need:
                    missing_cards[card_name] = need - found

            seller['missing_cards'] = [
                {'name': k, 'quantity': v} for (k, v) in missing_cards.items()
            ]

    @staticmethod
    def _group_by_seller(articles):
        start = time.time()
        offers = {}
        for card, article in articles:
            card_name = card['name']
            seller_id = article['seller_id']
            if card_name not in offers:
                offers[card_name] = {}  # noqa
            if seller_id not in offers[card_name]:
                offers[card_name][seller_id] = []
            offers[card_name][seller_id].append(article)
        logger.info('FINISH _group_by_seller, lasted %s', time.time() - start)
        return offers

    def _set_language_ids(self, card, language_id_map):
        language_ids = [language_id_map[name] for name in card['languages']]
        if len(language_ids) == len(language_id_map):
            # selecting all is the same as not selecting any
            language_ids = []
        card['language_ids'] = language_ids
