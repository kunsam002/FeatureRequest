#! /usr/bin/env python
# coding: utf-8

import os
import flask
from flask_migrate import Migrate, MigrateCommand

from feature_request.factories import create_app, initialize_blueprints

from flask_script import Manager, prompt, prompt_pass, prompt_bool, prompt_choices

FLASK_CONFIG = os.getenv("FLASK_CONFIG", "config.Config")
FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = os.getenv("FLASK_PORT", "5000")


# Required to map create_app function for FlaskGroup in cli
def make_app(*args, **kwargs):
    return create_app('feature_request', FLASK_CONFIG, *args, **kwargs)


app = create_app('feature_request', 'config.Config')

logger = app.logger

# Initializing script manager
manager = Manager(app)

migrate = Migrate(app, app.db)

manager.add_command('db', MigrateCommand)


@manager.command
def setup_app():
    """ load startup data for a particular module """
    app = flask.current_app

    app.logger.info("Relax and Enjoy the Ride....")

    with app.app_context():
        from feature_request import app, models
        db, logger = app.db, app.logger
        from crud_factory import loader
        from feature_request.services import UserService

        db.create_all()

        SETUP_DIR = app.config.get("SETUP_DIR")  # Should be present in config

        files = ['clients', 'product_areas']

        for name in files:
            filename = "%s.json" % name

            src = os.path.join(SETUP_DIR, filename)
            logger.info(src)

            loader.load_data(models, db, src)

        user_data = dict(name="Olukunle Ogunmokun",username="kunsam002",password="1234@Abcd",email="kunsam002@gmail.com")
        UserService.create(**user_data)



if __name__ == "__main__":
    manager.run()
