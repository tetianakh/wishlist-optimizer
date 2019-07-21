from datetime import datetime
import redis
from rq import Queue
from rq_scheduler import Scheduler
from flask import current_app
from logging import getLogger

logger = getLogger(__name__)

__queue = None
__connection = None
QUEUE_NAME = 'default'
KEY = 'scheduled_job_id'


def get_queue():
    global __queue
    if not __queue:
        __queue = Queue(
            name=QUEUE_NAME,
            connection=get_connection()
        )
    return __queue


def get_connection():
    global __connection
    if __connection is None:
        __connection = redis.from_url(current_app.config['REDIS_URL'])
    return __connection


def setup_scheduler(func, repeat_every=60):
    r = get_connection()
    scheduled_job_id = r.get(KEY)

    scheduler = Scheduler(connection=r)
    if scheduled_job_id:
        logger.info(f'Canceling old job {scheduled_job_id}')
        scheduler.cancel(scheduled_job_id)  # schedule old job before scheduling a new one

    job = scheduler.schedule(
        scheduled_time=datetime.utcnow(),  # Time for first execution, in UTC timezone
        func=func,  # Function to be queued
        interval=repeat_every,  # Time before the function is called again, in seconds
        repeat=None  # Repeat this number of times (None means repeat forever)
    )
    logger.info(
        "Scheduled function %s to be executed every %s seconds" % (
            func.__name__, repeat_every
        )
    )
    r.set(KEY, job.id)
