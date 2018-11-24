import redis
from rq import Queue
from flask import current_app

__queue = None
__connection = None


def get_queue():
    global __queue
    if not __queue:
        __queue = Queue(
            name='default',
            connection=get_connection()
        )
    return __queue


def get_connection():
    global __connection
    if __connection is None:
        __connection = redis.from_url(current_app.config['REDIS_URL'])
    return __connection
