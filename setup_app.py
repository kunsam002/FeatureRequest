import os
import flask
import click
from flask import Flask

app = Flask(__name__)

@app.cli.command()
def setup_app():
    app = flask.current_app

    app.logger.info("Relax and Enjoy the Ride....")

    with app.app_context():
        from feature_request import models, app
        db,logger=app.db,app.logger
        from crud_factory import loader

        SETUP_DIR = app.config.get("SETUP_DIR")  # Should be present in config

        files = ['clients', 'product_areas']

        for name in files:
            filename = "%s.json" % name

            src = os.path.join(SETUP_DIR, filename)
            logger.info(src)

            loader.load_data(models, db, src)


FLASK_CONFIG = os.getenv("FLASK_CONFIG", "config.Config")
FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = os.getenv("PORT", "5000")

if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT)
