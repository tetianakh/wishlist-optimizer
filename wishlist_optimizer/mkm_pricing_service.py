import asyncio
import logging
import time

logger = logging.getLogger(__name__)


class MkmPricingService:
    def __init__(self, api, wishlist, languages_service):
        self._loop = asyncio.get_event_loop()
        self._api = api
        self._wishlist = wishlist
        self._languages_service = languages_service
        self._best_prices = {}

    async def _get_card_articles(self, card, product_id, language_id):
        if language_id is None:
            return card, await self._api.get_articles(product_id)
        return card, await self._api.get_articles(product_id, language_id)

    def _get_card_product_ids(self, cards):
        tasks = [self._api.find_product_ids(c['name']) for c in cards]
        results = self._loop.run_until_complete(asyncio.gather(*tasks))
        for card, product_ids in zip(cards, results):
            for product_id in product_ids:
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

        for card_name, card_offers in offers.items():
            quantity = card_offers['card']['quantity']
            self._calculate_best_prices(quantity, card_offers['offers'])

        result = list(self._best_prices.values())
        result.sort(
            key=lambda a: (a['total_count'], -a['total_price']),
            reverse=True
        )
        logger.info('FINISH run, lasted %s', time.time() - start)

        return result[:10]

    def _calculate_best_prices(self, card_count, offers):
        for seller_id, offer_list in offers.items():
            if seller_id not in self._best_prices:
                self._best_prices[seller_id] = {
                    'total_count': 0,
                    'total_price': 0,
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

    @staticmethod
    def _group_by_seller(articles):
        start = time.time()
        offers = {}
        for card, article in articles:
            card_name = card['name']
            seller_id = article['seller_id']
            if card_name not in offers:
                offers[card_name] = {'card': card, 'offers': {}}
            if seller_id not in offers[card_name]['offers']:
                offers[card_name]['offers'][seller_id] = []
            offers[card_name]['offers'][seller_id].append(article)
        logger.info('FINISH _group_by_seller, lasted %s', time.time() - start)
        return offers

    def _set_language_ids(self, card, language_id_map):
        language_ids = [language_id_map[name] for name in card['languages']]
        if len(language_ids) == len(language_id_map):
            # selecting all is the same as not selecting any
            language_ids = []
        card['language_ids'] = language_ids
