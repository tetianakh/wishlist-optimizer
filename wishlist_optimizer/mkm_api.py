from contextlib import contextmanager
import logging
import urllib

import aiohttp
from json.decoder import JSONDecodeError
from requests_oauthlib import OAuth1
import requests_oauthlib
from flask import current_app


logging.basicConfig(level=logging.DEBUG)
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

    async def a_find_product_ids(self, card_name):
        # url = '{}/products/find'.format(self._base_url)
        headers = {
            'Content-Type': 'application/json'
        }
        params = {
            'search': card_name,
            'exact': "true",
            'idGame': MTG
        }
        # with session(self._config, url) as api:
        #     resp = api.get(url, headers=headers, params=params)
        # resp.raise_for_status()
        # if resp.status_code == 204:
        #     return set()
        # try:
        #     return {p['idProduct'] for p in resp.json()['product']}
        # except JSONDecodeError:
        #     logger.warning(
        #         "Failed to parse response `%s`: `%s`",
        #         resp.status_code, resp.text
        #     )
        #     return set()
        data = await self._http.get(
            'products/find', params=params, headers=headers
        )
        if not data:
            return set()
        return {p['idProduct'] for p in data['product']}

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
        if resp.status_code == 204:
            return set()
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
        if resp.status_code == 204:
            return []
        try:
            articles = resp.json()['article']
        except JSONDecodeError:
            logger.warning(
                'Failed to parse articles response `%s`: `%s`',
                resp.status_code, resp.text
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
