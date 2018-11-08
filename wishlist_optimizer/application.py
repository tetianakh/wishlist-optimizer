import logging
import os

import requests
from flask import Flask, render_template
from flask_cors import CORS


def create_app(app_name='WISHLIST_OPTIMIZER'):
    app = Flask(
        app_name, static_folder="./dist/static", template_folder="./dist"
    )
    app_settings = os.getenv(
        'APP_SETTINGS',
        'wishlist_optimizer.config.DevelopmentConfig'
    )
    app.config.from_object(app_settings)

    from wishlist_optimizer.api import api
    app.register_blueprint(api, url_prefix="/api")

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        if app.debug:
            return requests.get('http://localhost:8080/{}'.format(path)).text
        return render_template("index.html")

    from wishlist_optimizer.models import db
    db.init_app(app)

    logging.basicConfig(level=logging.DEBUG)

    CORS(app)

    return app
