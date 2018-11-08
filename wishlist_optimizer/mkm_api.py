from contextlib import contextmanager
import logging

from json.decoder import JSONDecodeError
import requests_oauthlib


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@contextmanager
def session(config, realm):
    yield requests_oauthlib.OAuth1Session(
        config['app_token'],
        client_secret=config['app_secret'],
        resource_owner_key=config['access_token'],
        resource_owner_secret=config['access_token_secret'],
        realm=realm
    )


MTG = 1


class MkmApi:
    def __init__(self, config):
        self._base_url = config['url']
        self._config = dict(config)
        logger.info("Base URL: %s", self._base_url)

    def find_product_ids(self, card_name):
        url = '{}/products/find'.format(self._base_url)
        headers = {
            'Content-Type': 'application/json'
        }
        params = {
            'search': card_name,
            'exact': "true",
            'idGame': MTG
        }
        with session(self._config, url) as api:
            resp = api.get(url, headers=headers, params=params)
        resp.raise_for_status()
        try:
            return {p['idProduct'] for p in resp.json()['product']}
        except JSONDecodeError:
            logger.warning(
                "Failed to parse response `%s`: `%s`",
                resp.status_code, resp.text
            )
            return set()

    def get_articles(self, product_id, language_id=None):
        base_url = '{}/articles/{}'.format(self._base_url, product_id)

        url = base_url
        if language_id:
            url = '{}?idLanguage={}'.format(base_url, language_id)

        with session(self._config, base_url) as api:
            resp = api.get(url)
        resp.raise_for_status()
        articles = []
        try:
            articles = resp.json()['article']
        except JSONDecodeError:
            logger.warning(
                'Failed to parse articles response `%s`: `%s`',
                resp.status_code, resp.text
            )

        return [self._get_article_data(a) for a in articles]

    def _get_article_data(self, full_data):
        return {
            'language': full_data['language']['idLanguage'],
            'price': full_data['price'],
            'seller_username': full_data['seller']['username'],
            'seller_id': full_data['seller']['idUser'],
            'count': full_data['count']
        }
