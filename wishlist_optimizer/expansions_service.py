import asyncio
import logging

from flask import current_app

from wishlist_optimizer.models import Expansion
from wishlist_optimizer.mkm_api import HttpClient, MkmApi
from wishlist_optimizer.mkm_config import get_config

logger = logging.getLogger(__name__)


class ExpansionService:

    def find_by_names(self, names):
        result = (
            Expansion.query.filter_by(name=name).first()
            for name in set(names)
        )
        return [exp for exp in result if exp]

    def get_card_expansions(self, card_name):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client = HttpClient(loop, get_config(current_app))
        result = loop.run_until_complete(
            MkmApi(client).get_expansions(card_name)
        )
        loop.run_until_complete(client.close())
        return result
