import asyncio
import logging
from urllib import parse

import aiohttp
from requests_oauthlib import OAuth1
from flask import current_app


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
MTG = 1
CARD = 'Magic Single'

# Headers: {'Content-Type': 'application/json', 'Authorization': 'OAuth realm="https://sandbox.cardmarket.com/ws/v2.0/output.json/articles/302060", oauth_nonce="61001251082361672621541852230", oauth_timestamp="1541852230", oauth_version="1.0", oauth_signature_method="HMAC-SHA1", oauth_consumer_key="HBTyJZWg2AP72Eeb", oauth_token="fIaHnvPL6WahfROzClbGDFM7FKDGhfPF", oauth_signature="0FG0qpyDYwILsqY3l0WWVc1ISpo%3D"'}

# Signing: signature base string: GET&https%3A%2F%2Fsandbox.cardmarket.com%2Fws%2Fv2.0%2Foutput.json%2Farticles%2F302060&oauth_consumer_key%3DHBTyJZWg2AP72Eeb%26oauth_nonce%3D61001251082361672621541852230%26oauth_signature_method%3DHMAC-SHA1%26oauth_timestamp%3D1541852230%26oauth_token%3DfIaHnvPL6WahfROzClbGDFM7FKDGhfPF%26oauth_version%3D1.0

# Bomat
# Signing: signature base string: GET&https%3A%2F%2Fsandbox.cardmarket.com%2Fws%2Fv2.0%2Foutput.json%2Farticles%2F292941&oauth_consumer_key%3DHBTyJZWg2AP72Eeb%26oauth_nonce%3D182538589866251113811541852381%26oauth_signature_method%3DHMAC-SHA1%26oauth_timestamp%3D1541852381%26oauth_token%3DfIaHnvPL6WahfROzClbGDFM7FKDGhfPF%26oauth_version%3D1.0

# Headers: {'Content-Type': 'application/json', 'Authorization': 'OAuth realm="https://sandbox.cardmarket.com/ws/v2.0/output.json/articles/292941", oauth_nonce="182538589866251113811541852381", oauth_timestamp="1541852381", oauth_version="1.0", oauth_signature_method="HMAC-SHA1", oauth_consumer_key="HBTyJZWg2AP72Eeb", oauth_token="fIaHnvPL6WahfROzClbGDFM7FKDGhfPF", oauth_signature="JDN1oDJh9IHWaTPQk79s3acTu%2B8%3D"'}


class HttpClient:
    def __init__(self, config):
        self._base_url = config.pop('url')
        logger.info("Base URL: %s", self._base_url)
        self._config = dict(config)
        self._session = aiohttp.ClientSession(loop=asyncio.get_event_loop(), headers={
            'Content-Type': 'application/json'
        })
        # self._client = OAuth1(
        #     config['app_token'],
        #     client_secret=config['app_secret'],
        #     resource_owner_key=config['access_token'],
        #     resource_owner_secret=config['access_token_secret']
        # )

    async def get(self, url, params=None, headers=None):
        oauth = OAuth1(
            self._config['app_token'],
            client_secret=self._config['app_secret'],
            resource_owner_key=self._config['access_token'],
            resource_owner_secret=self._config['access_token_secret']
        )
        url = '{}/{}'.format(self._base_url, url)
        oauth.client.realm = url

        if params:
            url = '{}?{}'.format(
                url, parse.urlencode(params)
            )
        headers = headers or {}

        url, headers, _ = oauth.client.sign(
            url, 'GET', None, headers
        )
        headers = {
            k.decode('utf-8'): v.decode('utf-8') for k, v in headers.items()
        }

        url = url.decode('utf-8')
        logger.debug('Headers: %s', headers)

        async with self._session.get(url, headers=headers) as response:
            logger.debug(response.headers)
            # text = await response.text()
            # logger.info('%s `%s`: %s', url, text, response.status)
            # response.raise_for_status()
            if response.status == 204:
                logger.info('No data for url %s', url)
                return None
            if response.status >= 400:
                logger.info('Making request for url %s with params %s', url, params)
                logger.warning('Response %s: %s', response.status, await response.text())
                return None
            return await response.json()

    # def sign(self, method, url, params, headers):
    #     method = method.upper()
    #     encoded_url = urllib.parse.quote_plus(url)
    #     base_string = f'{method}&{encoded_url}&'
    #
    # def _decode_signature(self, given_header):
    #     authorization_byte = given_header['Authorization']
    #     authorization_string = authorization_byte  # .decode()
    #     signature_position = authorization_string.find('oauth_signature="') + len('oauth_signature="')
    #     sub_string_signature = authorization_string[signature_position:]
    #
    #     decoded_sub_string_signature = parse.unquote(sub_string_signature)
    #     authorization_string = authorization_string[:signature_position]
    #     authorization_string = "{}{}".format(authorization_string, decoded_sub_string_signature)
    #
    #     return authorization_string
    async def close(self):
      await self._session.close()


class MkmApi:
    def __init__(self, config):
        self._http = HttpClient(config)


    async def find_product_ids(self, card_name):
        logger.info('Searching product ids for card %s', card_name)
        params = {
          'search': card_name.lower(),
          'exact': "true" if len(card_name) < 4 else "false",
          'idGame': MTG
        }

        data = await self._http.get(
            'products/find', params=params
        )
        if not data:
            return set()
        try:
            ids = {
                p['idProduct'] for p in data['product']
                if self._matches(card_name, p)
            }
            logger.info('Card: %s, product ids: %s', card_name, ids)
            return ids
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
        url = 'articles/{}'.format(product_id)

        data = await self._http.get(
            url, params=params
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

    async def close(self):
        await self._http.close()
