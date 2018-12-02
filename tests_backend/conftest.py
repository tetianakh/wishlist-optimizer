import asyncio

import pytest
from flask.testing import FlaskClient

from wishlist_optimizer.application import create_app
from wishlist_optimizer.models import db, Language, Expansion


@pytest.fixture(scope="session")
def app():
    app = create_app(config_name='TestingConfig')
    app.test_client_class = FlaskClient
    app.testing = True
    return app


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.yield_fixture(scope="session")
def database(app, request):
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add(Language(name='English', mkm_id=1))
        db.session.add(Language(name='French', mkm_id=2))
        db.session.add(Language(name='German', mkm_id=3))
        db.session.add(Expansion(name='Kaladesh', code='KLD'))
        db.session.add(Expansion(name='Dominaria', code='DOM'))
        db.session.commit()
        yield db
        db.drop_all()


@pytest.fixture(scope='session')
def _db(app, database):
    return database


def amock(result):
    f = asyncio.Future()
    f.set_result(result)
    return f
