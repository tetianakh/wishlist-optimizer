import logging
from collections import defaultdict
import json


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MkmPricingService:
    def __init__(self, api, wishlist, languages_service):
        self._api = api
        self._wishlist = wishlist
        self._languages_service = languages_service
        self._best_prices = {}

    def get_offers(self, card_name, card_languages):
        language_id_map = self._languages_service.get_language_mkm_ids()
        language_ids = [language_id_map[name] for name in card_languages]
        if len(language_ids) == len(language_id_map):
            language_ids = []  # selecting all is the same as not selecting any

        product_ids = self._api.find_product_ids(card_name)
        logger.info(
            "Card: `%s`, product ids: %s, language ids: %s",
            card_name, product_ids, language_ids
        )
        offers = defaultdict(list)
        for product_id in product_ids:
            if not language_ids:
                articles = self._api.get_articles(product_id)
            else:
                articles = []
                for language_id in language_ids:
                    articles += self._api.get_articles(product_id, language_id)
            for article in articles:
                offers[article['seller_id']].append(article)
        return offers

    def run(self):
        for card in self._wishlist:
            offers = self.get_offers(card['name'], card['languages'])

            self.calculate_best_prices(card['quantity'], offers)
        result = list(self._best_prices.values())

        result.sort(
            key=lambda a: (a['total_count'], -a['total_price']),
            reverse=True
        )
        return result[:10]

    def calculate_best_prices(self, card_count, offers):
        for seller_id, offer_list in offers.items():
            if seller_id not in self._best_prices:
                self._best_prices[seller_id] = {
                    'total_count': 0,
                    'total_price': 0,
                    'seller_id': offer_list[0]['seller_id'],
                    'seller_username': offer_list[0]['seller_username']
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
