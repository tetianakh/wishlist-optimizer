import logging
from urllib import parse

import aiohttp

from flask import current_app
from requests_oauthlib import OAuth1

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
MTG = 1
CARD = 'Magic Single'


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
      response = self._get(url, params, headers)
      if response.status == 307:
        return await self._paginate(url, params, headers, field)
      return await self._process_response(response)

  async def _process_response(self, response):
      if response.status == 204:
        logger.info('No data for url %s', url)
        return None
      if response.status == 429:
        raise RateLimitReached()
      if response.status >= 400:
        logger.info('Made request for url %s with params %s', url, params)  # noqa
        logger.warning('Response %s: %s', response.status, await response.text())  # noqa
        response.raise_for_status()
      return await response.json().get(field)

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

      async with self._session.get(url, headers=headers) as response:
          logger.debug(response.headers)
          return response

  async def _paginate(self, url, params, headers, field):
      # maxResults=100 start=0
      params['maxResults'] = 100
      params['start'] = 0
      result = []
      response = await self._get(url, params, headers)
      batch = await self._process_response(response)
      while batch:
          result.extend(batch)
          params['start'] += params['maxResults']
          response = await self._get(url, params, headers)
          batch = await self._process_response(response)
      return result

  async def close(self):
      await self._session.close()


class MkmApi:
  def __init__(self, client):
      self._http = client

  async def find_product_ids(self, card_name):
      logger.info('Searching product ids for card %s', card_name)
      params = {
          'search': card_name.lower(),
          'exact': "true" if len(card_name) < 4 else "false",
          'idGame': MTG
      }

      data = await self._http.get(
          'products/find', params=params, headers={}, field='product'
      )
      if not data:
          return set()
      ids = {
          p['idProduct'] for p in data
          if self._matches(card_name, p)
      }
      logger.info('Card: %s, product ids: %s', card_name, ids)

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
          'count': full_data['count']
      }
