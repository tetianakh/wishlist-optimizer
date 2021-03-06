import logging
from logging.config import dictConfig
import os

import requests
from flask import Flask, render_template, send_from_directory
from flask_cors import CORS


def create_app(app_name='WISHLIST_OPTIMIZER', config_name=None):
    app = Flask(
        app_name, static_folder="./dist/static", template_folder="./dist"
    )

    config_name = config_name or 'DevelopmentConfig'
    app_settings = os.getenv(
        'APP_SETTINGS',
        'wishlist_optimizer.config.%s' % config_name
    )
    app.config.from_object(app_settings)

    configure_logging(
        log_level=app.config['LOG_LEVEL'], log_format=app.config['LOG_FORMAT']
    )

    from wishlist_optimizer.api import api
    app.register_blueprint(api, url_prefix="/api")
    from wishlist_optimizer.auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        if app.debug:
            return requests.get('http://localhost:8080/{}'.format(path)).text
        return render_template("index.html")

    @app.route('/favicon.ico')
    def favicon():
        print(app.template_folder)
        return send_from_directory(
            app.template_folder,
            'favicon.ico',
            mimetype='image/vnd.microsoft.icon'
        )

    from wishlist_optimizer.models import db
    db.init_app(app)

    CORS(app)

    return app


def configure_logging(log_level, log_format):
    # logging.basicConfig(
    #     level=log_level, format=log_format
    # )
    logging_config = dict(
        version=1,
        disable_existing_loggers=False,
        formatters={
            'fmt': {'format': log_format}
        },
        handlers={
            'default': {
                'class': 'logging.StreamHandler',
                'formatter': 'fmt',
                'level': log_level
            }
        },
        loggers={
            '': {
                'handlers': ['default'],
                'level': log_level,
                'propagate': True
            },
            'rq.worker': {
                'handlers': ['default'],
                'level': 'INFO',
                'propagate': False
            },
            'oauthlib.oauth1.rfc5849': {
                'handlers': ['default'],
                'level': 'INFO',
                'propagate': False
            }
        }
    )

    dictConfig(logging_config)
