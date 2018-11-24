import asyncio

import pytest

from wishlist_optimizer.application import create_app


@pytest.fixture(scope="session")
def app():
    app = create_app()
    return app


def amock(result):
    f = asyncio.Future()
    f.set_result(result)
    return f
