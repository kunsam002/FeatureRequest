"""
config.py

The file that will be used to specify each flask application's config
"""
import os
import socket

"""
config.py

Flask configuration script

"""


class Config(object):
    """ Default config object with specific parameters for flask. """

    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost/britecorerequest"
    SECRET_KEY = '\x91c~\xc0-\xe3\'f\xe19PxE\x93\xe8\x91`usu"\xd0\xb6\x01/\x0c\xed\\\xbd]nGtvH\x99ekw\xf8'
    SQLALCHEMY_ECHO = False

    SETUP_DIR = os.path.join(os.path.dirname(os.path.abspath(__name__)), "setup")
    STATIC_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__name__)), "featurerequest", "static")

    SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
    API_URL = 'http://petstore.swagger.io/v2/swagger.json'  # Our API url (can of course be a local resource)

