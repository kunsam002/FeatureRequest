# Imports
from flask import current_app as app
import os
from datetime import datetime, timedelta
from sqlalchemy.event import listens_for
from sqlalchemy.engine import Engine
from sqlalchemy.pool import Pool
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Logger
logger = app.logger

# Bcrypt
bcrypt = app.bcrypt

# Database
db = app.db

# Alembic
alembic = app.alembic

# API
api = app.api

# Login Manager
login_manager = app.login_manager

# Authorization Principal
principal = app.principal

swaggerui_blueprint = app.swaggerui_blueprint

