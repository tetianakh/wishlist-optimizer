import os


class BaseConfig(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    QUEUES = ['default']
    APP_TOKEN = os.getenv('MKM_APP_TOKEN')
    APP_SECRET = os.getenv('MKM_APP_SECRET')
    ACCESS_TOKEN = os.getenv('MKM_ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.getenv('MKM_ACCESS_TOKEN_SECRET')


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    REDIS_URL = 'redis://localhost:6379/0'
    DEBUG = True
    MKM_URL = "https://sandbox.cardmarket.com/ws/v2.0/output.json"


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    REDIS_URL = os.getenv('REDIS_URL')
    MKM_URL = "https://api.cardmarket.com/ws/v2.0/output.json"
