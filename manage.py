#! /usr/bin/env python
# coding: utf-8

import os
import flask
from flask_migrate import Migrate, MigrateCommand

from factories import create_app, initialize_blueprints

from flask_script import Manager, prompt, prompt_pass, prompt_bool, prompt_choices

from multiprocessing import Process

FLASK_CONFIG = os.getenv("FLASK_CONFIG", "config.Config")
FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = os.getenv("FLASK_PORT", "5000")


# Required to map create_app function for FlaskGroup in cli
def make_app(*args, **kwargs):
    return create_app('featurerequest', FLASK_CONFIG, *args, **kwargs)


app = create_app('featurerequest', 'config.Config')

logger = app.logger

# Initializing script manager
manager = Manager(app)

migrate = Migrate(app, app.db)

manager.add_command('db', MigrateCommand)


@manager.command
def alembic(action, message=""):
    """ alembic integration using Flask-Alembic. Should provide us with more control over migrations """
    from featurerequest import alembic as _alembic
    import featurerequest.models
    from featurerequest import app

    if action == "migrate":
        app.logger.info("Generating migration")
        _alembic.revision(message)
        app.logger.info("Migration complete")

    elif action == "upgrade":
        app.logger.info("Executing upgrade")
        _alembic.upgrade()
        app.logger.info("Upgrade complete")

    elif action == 'update':
        app.logger.info("Executing upgrade")
        _alembic.upgrade()
        _alembic.revision("Generating migration")
        _alembic.upgrade()
        app.logger.info("Upgrade complete")


@manager.command
def setup_app():
    """ load startup data for a particular module """
    app = flask.current_app

    app.logger.info("Relax and Enjoy the Ride....")
    # For Database Update
    actions = ['upgrade', 'migrate', 'upgrade']
    for i in actions:
        alembic(action=i)

    with app.app_context():
        from featurerequest import db, models, logger
        from crud_factory import loader

        SETUP_DIR = app.config.get("SETUP_DIR")  # Should be present in config

        files = ['clients', 'product_areas']

        for name in files:
            filename = "%s.json" % name

            src = os.path.join(SETUP_DIR, filename)
            logger.info(src)

            loader.load_data(models, db, src)



@manager.command
def runserver():
    """ Start the server"""
    from featurerequest.views.public import www
    from featurerequest import api,swaggerui_blueprint,app

    initialize_blueprints(app, www)

    SWAGGER_URL = app.config.get("SWAGGER_URL")

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    port = int(os.environ.get('PORT', 5551))
    app.run(host='0.0.0.0', port=port)



if __name__ == "__main__":
    manager.run()
