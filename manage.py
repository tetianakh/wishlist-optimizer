from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import redis
from rq import Connection, Worker

from wishlist_optimizer.application import create_app
from wishlist_optimizer.models import db, Card, Wishlist

app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)

# provide a migration utility command
manager.add_command('db', MigrateCommand)


# enable python shell with application context
@manager.shell
def shell_ctx():
    return dict(
        app=app,
        db=db,
        Card=Card,
        Wishlist=Wishlist,
    )


@manager.command
def run_worker():
    redis_url = app.config['REDIS_URL']
    redis_connection = redis.from_url(redis_url)
    with Connection(redis_connection):
        worker = Worker(app.config['QUEUES'])
        worker.work()


if __name__ == '__main__':
    manager.run()
