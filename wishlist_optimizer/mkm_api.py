import logging
from json import JSONDecodeError
from urllib import parse

import aiohttp

from flask import current_app
from requests_oauthlib import OAuth1

from wishlist_optimizer.cache import ttl_cache
from wishlist_optimizer.config import PRODUCTS_CACHE_TTL, ARTICLES_CACHE_TTL


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
MTG = 1
CARD = 'Magic Single'
MAX_RESULTS = 1000


class RateLimitReached(RuntimeError):
    pass


class HttpClient:
    def __init__(self, loop, config):
        self._base_url = config.pop('url')
        logger.info("Base URL: %s", self._base_url)
        self._config = dict(config)
        self._session = aiohttp.ClientSession(
            loop=loop, headers={
                'Content-Type': 'application/json'
            }
        )

    async def get(self, url, params, headers, field):
        response = await self._get(url, params, headers)
        if response.status == 307:
            return await self._paginate(url, params, headers, field)
        return await self._process_response(response, field)

    async def _process_response(self, response, field):
        if response.status == 204:
            return None
        if response.status == 429:
            logger.warning("Rate limit was reached.")
            raise RateLimitReached()
        if response.status >= 400:
            logger.warning('Error response: %s', response)
            response.raise_for_status()
        try:
            return (await response.json()).get(field)
        except JSONDecodeError as e:
            logger.exception(e)
            return None

    async def _get(self, url, params, headers):
        oauth = OAuth1(
            self._config['app_token'],
            client_secret=self._config['app_secret'],
            resource_owner_key=self._config['access_token'],
            resource_owner_secret=self._config['access_token_secret']
        )
        url = '{}/{}'.format(self._base_url, url)
        oauth.client.realm = url

        if params:
            url = '{}?{}'.format(url, parse.urlencode(params))
        headers = headers or {}

        url, headers, _ = oauth.client.sign(url, 'GET', None, headers)
        headers = {
            k.decode('utf-8'): v.decode('utf-8') for k, v in headers.items()
        }

        url = url.decode('utf-8')
        logger.debug('Request headers: %s', headers)

        async with self._session.get(
                url, headers=headers, allow_redirects=False) as response:
            logger.debug(response.headers)
            logger.info('Received response %s', response.status)
            await response.text()

        return response

    async def _paginate(self, url, params, headers, field):
        # maxResults=100 start=0
        params = params or {}
        params['maxResults'] = MAX_RESULTS
        params['start'] = 0
        result = []
        response = await self._get(url, params, headers)
        batch = await self._process_response(response, field)
        while batch:
            result.extend(batch)
            params['start'] += params['maxResults']
            response = await self._get(url, params, headers)
            batch = await self._process_response(response, field)
        return result

    async def close(self):
        await self._session.close()


class MkmApi:
    def __init__(self, client):
        self._http = client

    async def get_all_expansions(self):
        logger.info('Getting all expansions')
        url = 'games/%s/expansions' % MTG
        data = await self._http.get(
            url, params={}, headers={}, field='expansion'
        )
        if not data:
            logger.info('No expansions were found!')
            return []
        return [{'name': e['enName'], 'code': e['abbreviation']} for e in data]

    async def get_expansions(self, card_name):
        logger.info('Getting expansions for card %s', card_name)
        data = await self._get_product_data(card_name)
        return [p['expansionName'] for p in data]

    async def get_product_ids(self, card_name, expansions):
        logger.info('Searching product ids for card %s', card_name)
        data = await self._get_product_data(card_name)
        if expansions:
            expansions = set(expansions)
            ids = [p['idProduct'] for p in data if p['expansionName'] in expansions]  # noqa
        else:
            ids = [p['idProduct'] for p in data]
        logger.info('Card: %s, product ids: %s', card_name, ids)
        return ids

    @ttl_cache(PRODUCTS_CACHE_TTL)
    async def _get_product_data(self, card_name):
        params = {
            'search': card_name.lower(),
            'exact': "true" if len(card_name) < 4 else "false",
            'idGame': MTG
        }

        data = await self._http.get(
            'products/find', params=params, headers={}, field='product'
        ) or []
        return [p for p in data if self._matches(card_name, p)]

    def _matches(self, card_name, product):
        if product['categoryName'] != CARD:
            # not a card, skip it
            return False
        product_name = product['enName'].lower()
        card_name = card_name.lower()
        if product_name == card_name:
            return True
        if '/' in product_name:
            # flip card or a split card, check if we have the name for one
            # side only
            if card_name + ' /' in product_name or '/ ' + card_name in product_name:  # noqa
                return True
            # flip/split cards can have one or two slashes
            # and may or may not have spaces around them
            card_name = self._remove_slashes_and_spaces(card_name)
            product_name = self._remove_slashes_and_spaces(product_name)
            return card_name == product_name
        return False

    @staticmethod
    def _remove_slashes_and_spaces(card_name):
        return card_name.replace(' ', '').replace('/', '')

    @ttl_cache(ARTICLES_CACHE_TTL)
    async def get_articles(self, product_id, language_id=None, foil=None):
        params = {}
        if language_id:
            params['idLanguage'] = language_id
        if foil is not None:
            params['isFoil'] = 'true' if foil else 'false'

        url = 'articles/{}'.format(product_id)

        data = await self._http.get(
            url, params=params, headers={}, field='article'
        )
        if not data:
            return []
        return [self._get_article_data(a) for a in data]

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
            'seller_country': full_data['seller']['address']['country'],
            'count': full_data['count'],
            'id': full_data['idArticle'],
        }
