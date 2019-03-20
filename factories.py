"""
factories.py

@Author: Olukunle Ogunmokun
@Date: 10th Dec, 2018

This module contains application factories.
"""

from flask import Flask, send_from_directory
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from flask_restful import Api
from flask_alembic import Alembic

from flask_login import LoginManager
from flask_principal import Principal

from flask_assets import Environment, Bundle

from flask_swagger_ui import get_swaggerui_blueprint



def initialize_blueprints(app, *blueprints):
    """Registers a set of blueprints to an application"""

    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def create_app(app_name, config_obj, api_prefix='/api/v1'):
    """ Generates and configures the main application."""

    # Launching application
    app = Flask(app_name)  # So the engine would recognize the root package

    # Load Configuration
    app.config.from_object(config_obj)

    # Loading assets
    assets = Environment(app)
    assets.from_yaml('assets.yaml')
    app.assets = assets

    # Initializing bcrypt password encryption
    bcrypt = Bcrypt(app)
    app.bcrypt = bcrypt

    # Initializing Database
    db = SQLAlchemy(app)
    app.db = db

    # Initializing login manager
    login_manager = LoginManager()
    login_manager.login_view = app.config.get('LOGIN_VIEW', '.login')

    login_manager.session_protection = 'strong'
    login_manager.init_app(app)
    app.login_manager = login_manager

    # Initializing principal manager
    app.principal = Principal(app)

    app.swaggerui_blueprint = get_swaggerui_blueprint(
        app.config.get('SWAGGER_URL'),  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        app.config.get('API_URL'),
        config={  # Swagger UI config overrides
            'app_name': "Test application"
        },
        # oauth_config={ # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
        # 'clientId': "your-client-id",
        # 'clientSecret': "your-client-secret-if-required",
        # 'realm': "your-realms",
        # 'appName': "your-app-name",
        # 'scopeSeparator': " ",
        # 'additionalQueryStringParams': {'test': "hello"}
        # }
    )

    # Initializing Alembic
    alembic = Alembic()
    alembic.init_app(app)
    app.alembic = alembic

    api = Api(app, prefix=api_prefix)
    app.api = api

    # include an api_registry to the application
    app.api_registry = []  # a simple list holding the values to be registered

    return app
