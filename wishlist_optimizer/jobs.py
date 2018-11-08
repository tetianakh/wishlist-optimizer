import redis
from rq import Queue
from flask import current_app

from wishlist_optimizer.languages_service import LanguagesService
from wishlist_optimizer.mkm_api import MkmApi
from wishlist_optimizer.mkm_pricing_service import MkmPricingService


def get_pricing(wishlist):
    
    config = {
        "app_token": current_app.config['APP_TOKEN'],
        "app_secret": current_app.config['APP_SECRET'],
        "access_token": current_app.config['ACCESS_TOKEN'],
        "access_token_secret": current_app.config['ACCESS_TOKEN_SECRET'],
        "url": current_app.config['MKM_URL']
    }
    api = MkmApi(config)
    service = MkmPricingService(api, wishlist['cards'], LanguagesService())
    return service.run()


__queue = None


def get_queue():
    global __queue
    if not __queue:
        __queue = Queue(
            name='default',
            connection=redis.from_url(current_app.config['REDIS_URL'])
        )
    return __queue


def schedule_job(job, *args, **kwargs):
    task = get_queue().enqueue(job, *args, **kwargs)
    return _get_job_status(task)


def _get_job_status(job):
    return {
        'job_id': job.get_id(),
        'job_status': job.get_status(),
        'job_result': job.result,
    }


def check_job_status(job_id):
    task = get_queue().fetch_job(job_id)
    if not task:
        return None
    return _get_job_status(task)
