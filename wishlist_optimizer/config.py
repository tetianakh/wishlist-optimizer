import os
import logging


class BaseConfig(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    QUEUES = ['default']
    GOOGLE_ISS = 'https://accounts.google.com'
    APP_TOKEN = os.getenv('MKM_APP_TOKEN')
    APP_SECRET = os.getenv('MKM_APP_SECRET')
    ACCESS_TOKEN = os.getenv('MKM_ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.getenv('MKM_ACCESS_TOKEN_SECRET')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')


class DevelopmentConfig(BaseConfig):
    LOG_LEVEL = logging.DEBUG
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    SQLALCHEMY_DATABASE_URI = 'postgres://localhost:5432/wishlists'
    REDIS_URL = 'redis://localhost:6379/0'
    DEBUG = True
    MKM_URL = "https://sandbox.cardmarket.com/ws/v2.0/output.json"
    MKM_USER_URL = "https://sandbox.cardmarket.com/en/Magic/Users"


class ProductionConfig(BaseConfig):
    LOG_LEVEL = logging.INFO
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    REDIS_URL = os.getenv('REDIS_URL')
    MKM_URL = "https://api.cardmarket.com/ws/v2.0/output.json"
    MKM_USER_URL = "https://www.cardmarket.com/en/Magic/Users"
