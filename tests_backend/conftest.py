import asyncio

import pytest

from wishlist_optimizer.application import create_app
from wishlist_optimizer.models import db


@pytest.fixture(scope="session")
def app():
    app = create_app(config_name='TestingConfig')
    return app


@pytest.yield_fixture(scope="session")
def database(app):
    with app.app_context():
        db.create_all()
        yield db


@pytest.fixture(scope='session')
def _db(app, database):
    return database


def amock(result):
    f = asyncio.Future()
    f.set_result(result)
    return f
