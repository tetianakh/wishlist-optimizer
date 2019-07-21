web: gunicorn runserver:app
worker: python manage.py run_worker
scheduler: rqscheduler --url $REDIS_URL
