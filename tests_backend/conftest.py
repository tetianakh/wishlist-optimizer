import pytest

from wishlist_optimizer.application import create_app


@pytest.fixture
def app():
    app = create_app()
    return app
