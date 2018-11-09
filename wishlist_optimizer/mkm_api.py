from contextlib import contextmanager
import logging
import urllib

import aiohttp
from requests_oauthlib import OAuth1
import requests_oauthlib
from flask import current_app


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
MTG = 1
CARD = 'Magic Single'


class HttpClient:
    def __init__(self, config):
        self._base_url = config.pop('url')
        logger.info("Base URL: %s", self._base_url)
        self._config = dict(config)
        self._client = OAuth1(
            config['app_token'],
            client_secret=config['app_secret'],
            resource_owner_key=config['access_token'],
            resource_owner_secret=config['access_token_secret']
        )

    async def get(self, url, params=None, headers=None):
        url = '{}/{}'.format(self._base_url, url)
        self._client.client.realm = url

        if params:
            url = '{}?{}'.format(
                url, urllib.parse.urlencode(params)
            )
        headers = headers or {}

        url, headers, _ = self._client.client.sign(
            url, 'GET', None, headers
        )
        headers = {
            k.decode('utf-8'): v.decode('utf-8') for k, v in headers.items()
        }
        url = url.decode('utf-8')

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                if response.status == 204:
                    return None
                return await response.json()


class MkmApi:
    def __init__(self, config):
        self._base_url = config['url']
        self._config = dict(config)
        self._http = HttpClient(config)
        logger.info("Base URL: %s", self._base_url)

    async def find_product_ids(self, card_name):
        headers = {
            'Content-Type': 'application/json'
        }
        params = {
            'search': card_name,
            'exact': "false",
            'idGame': MTG
        }
        data = await self._http.get(
            'products/find', params=params, headers=headers
        )
        if not data:
            return set()
        try:
            return {
                p['idProduct'] for p in data['product']
                if self._matches(card_name, p)
            }
        except KeyError:
            logger.warning('Failed to parse product id response: %s', data)
            return set()

    @staticmethod
    def _matches(card_name, product):
        product_name = product['enName'].lower()
        card_name = card_name.lower()
        return product['categoryName'] == CARD and (
            product_name == card_name
            or card_name + ' /' in product_name
            or '/ ' + card_name in product_name
        )

    async def get_articles(self, product_id, language_id=None):
        params = None
        if language_id:
            params = {'idLanguage': language_id}

        data = await self._http.get(
            'articles/{}'.format(product_id), params=params
        )
        if not data:
            return []
        try:
            articles = data['article']
        except KeyError:
            logger.warning(
                'Failed to parse articles response `%s`', data
            )

        return [self._get_article_data(a) for a in articles]

    def _get_article_data(self, full_data):
        username = full_data['seller']['username']
        seller_url = '{}/{}'.format(
            current_app.config['MKM_USER_URL'], username
        )
        return {
            'language': full_data['language']['idLanguage'],
            'price': full_data['price'],
            'seller_username': username,
            'seller_url': seller_url,
            'seller_id': full_data['seller']['idUser'],
            'count': full_data['count']
        }
