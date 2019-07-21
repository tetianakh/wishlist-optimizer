from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import redis
from rq import Connection, Worker

from wishlist_optimizer.application import create_app
from wishlist_optimizer.models import db, Card, Wishlist, Language
from wishlist_optimizer import jobs
from wishlist_optimizer.redis import setup_scheduler


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
        setup_scheduler(jobs.populate_expansions)
        worker = Worker(app.config['QUEUES'])
        worker.work()


@manager.command
def populate_languages():
    db.session.add(Language(name='English', mkm_id=1))
    db.session.add(Language(name='French', mkm_id=2))
    db.session.add(Language(name='German', mkm_id=3))
    db.session.add(Language(name='Spanish', mkm_id=4))
    db.session.add(Language(name='Italian', mkm_id=5))
    db.session.add(Language(name='Simplified Chinese', mkm_id=6))
    db.session.add(Language(name='Japanese', mkm_id=7))
    db.session.add(Language(name='Portuguese', mkm_id=8))
    db.session.add(Language(name='Russian', mkm_id=9))
    db.session.add(Language(name='Korean', mkm_id=10))
    db.session.add(Language(name='Chinese', mkm_id=11))
    db.session.commit()


@manager.command
def populate_expansions():
    jobs.populate_expansions()


if __name__ == '__main__':
    manager.run()
