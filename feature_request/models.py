"""
models.py

@Author: Olukunle Ogunmokun
@Date: 3rd Oct, 2018

"""
import hashlib
import inspect as pyinspect
import sys
from datetime import datetime, timedelta
import json
from flask.helpers import url_for
from sqlalchemy import func, event, desc, asc
from sqlalchemy import inspect, UniqueConstraint, desc
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property, Comparator
from sqlalchemy.orm import dynamic
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.collections import InstrumentedList
from crud_factory.utils import slugify, id_generator, token_generator
from socket import gethostname, gethostbyname
from werkzeug.security import generate_password_hash, check_password_hash

from feature_request import app

db, logger, bcrypt = app.db, app.logger, app.bcrypt


def slugify_from_name(context):
    """
    An sqlalchemy processor that works with default and on update
    field parameters to automatically slugify the name parameters in the model
    """
    return slugify(context.current_parameters['name'])


def slugify_from_title(context):
    """
    An sqlalchemy processor that works with default and on update
    field parameters to automatically slugify the title parameters in the model
    """
    return slugify(context.current_parameters['title'])


def generate_token_code(context):
    return hashlib.md5(
        "%s:%s:%s" % (
            context.current_parameters["user_id"], context.current_parameters["email"], datetime.utcnow())).hexdigest()


def generate_email_hash(context):
    return hashlib.md5("%s:%s" % (context.current_parameters["email"], datetime.utcnow())).hexdigest()


class AppMixin(object):
    """ Mixin class for general attributes and functions """

    @property
    def pk(self):
        """ generic way to retrieve the identity of a model object """
        pk_name = inspect(self.__class__).primary_key[0].name
        return getattr(self, pk_name)

    @classmethod
    def primary_key(cls):
        """ generic way to retrieve the identity of a model object """
        pk_name = inspect(cls).primary_key[0].name
        return getattr(cls, pk_name)

    @declared_attr
    def date_created(cls):
        return db.Column(db.DateTime, default=datetime.utcnow, index=True)

    @declared_attr
    def last_updated(cls):
        return db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    def as_dict(self, include_only=None, exclude=["is_deleted"], extras=["pk"], child=None, child_include=[], level=0):
        """ Retrieve all values of this model as a dictionary """
        data = inspect(self)

        level = level + 1

        if include_only is None:
            include_only = data.attrs.keys() + extras

        else:
            include_only = include_only + extras

        _dict = dict([(k, getattr(self, k)) for k in include_only if isinstance(getattr(self, k),
                                                                                (hybrid_property, InstrumentedAttribute,
                                                                                 InstrumentedList,
                                                                                 dynamic.AppenderMixin)) is False and k not in exclude])

        for key, obj in _dict.items():

            if isinstance(obj, db.Model) and level < 1:
                _dict[key] = obj.as_dict(level=level)

            if isinstance(obj, (list, tuple)):
                items = []
                for item in obj:
                    inspect_item = inspect(item)
                    items.append(
                        dict([(k, getattr(item, k)) for k in inspect_item.attrs.keys() + extras if
                              k not in exclude and hasattr(item, k)]))

                for item in items:
                    obj = item.get(child)
                    if obj:
                        item[child] = obj.as_dict(extras=child_include)
        return _dict

    def level_dict(self, include_only=None, exclude=["is_deleted"], extras=[], child=None, child_include=[]):
        data = self.as_dict(include_only=include_only, exclude=exclude, extras=extras, child=child,
                            child_include=child_include)
        for key, value in data.items():
            if type(data.get(key)) == dict:
                data.pop(key)
        return data


class UserMixin(AppMixin):
    """ Mixin class for Shop related attributes and functions """

    @declared_attr
    def user_id(cls):
        return db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)

    @declared_attr
    def user(cls):
        return db.relationship("User", foreign_keys=cls.user_id)


class User(AppMixin, db.Model):
    extra_fields = ["full_name", "approx_name", "name"]

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200), unique=True)
    first_name = db.Column(db.String(200), nullable=True)
    last_name = db.Column(db.String(200), nullable=True)
    name = db.Column(db.String(300), nullable=False)
    gender = db.Column(db.String(200), nullable=True)  # Male or Female
    phone = db.Column(db.String(200), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    password = db.Column(db.Text, unique=False)
    is_admin = db.Column(db.Boolean, default=False)

    login_count = db.Column(db.Integer, default=0, index=True)
    last_login_at = db.Column(db.DateTime, index=True)
    current_login_at = db.Column(db.DateTime, index=True)
    last_login_ip = db.Column(db.String(200), index=True)
    current_login_ip = db.Column(db.String(200), index=True)

    referral_code = db.Column(db.String(200), index=True)

    @property
    def approx_name(self):
        _name = self.name.split(" ")
        _first = _name[0]

        _last = " %s." % _name[1][0].upper() if len(_name) > 1 else ""

        return "%s%s" % (_first, _last)

    @property
    def full_name(self):
        return self.name

    def get_id(self):
        """ For login manager """
        return self.id

    def update_last_login(self):
        if self.current_login_at is None and self.last_login_at is None:
            self.current_login_at = self.last_login_at = datetime.now()
            self.current_login_ip = self.last_login_ip = gethostbyname(gethostname())

        if self.current_login_at != self.last_login_at:
            self.last_login_at = self.current_login_at
            self.last_login_ip = self.current_login_ip
            self.current_login_at = datetime.now()
            self.current_login_ip = gethostbyname(gethostname())

        if self.last_login_at == self.current_login_at:
            self.current_login_at = datetime.now()
            self.current_login_ip = gethostbyname(gethostname())

        self.login_count += 1
        db.session.add(self)
        db.session.commit()

    def is_authenticated(self):
        """ For login manager """
        return True

    def get_auth_token(self):
        """ Returns the user's authentication token """
        key = "%s:%s" % (self.email, self.password)
        return hashlib.sha256(key.encode()).hexdigest()

    @property
    def auth_token(self):
        "retrieve the auth token for a user within the platform"
        return self.get_token()

    def is_active(self):
        """ Returns if the user is active or not. Overridden from UserMixin """
        return self.is_enabled

    def encrypt_password(self, password):
        """
        Generates a password from the plain string

        :param password: plain password string
        """

        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks the given password against the saved password

        :param password: password to check
        :type password: string

        :returns True or False
        :rtype: bool

        """
        return check_password_hash(self.password, password)

    def set_password(self, new_password):
        """
        Sets a new password for the user

        :param new_password: the new password
        :type new_password: string
        """

        self.encrypt_password(new_password)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.name


class Client(AppMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), index=True)  # A short, descriptive name of the feature request.
    slug = db.Column(db.String(200), nullable=False, default=slugify_from_name)
    address = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)

    phone = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)

    def __unicode__(self):
        return self.title

    def __repr__(self):
        return '<Client %r>' % self.name


class ProductArea(AppMixin, db.Model):
    code = db.Column(db.String(200), nullable=False, index=True, primary_key=True, default=slugify_from_name)

    name = db.Column(db.String(200), index=True)  # A short, descriptive name of the feature request.
    description = db.Column(db.Text, nullable=True)

    def __unicode__(self):
        return self.title

    def __repr__(self):
        return '<ProductArea %r>' % self.name

    @property
    def featured_requests(self):
        return db.session.query(FeatureRequest).filter(FeatureRequest.product_area_code == self.code).all()


class FeatureRequest(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), index=True)  # A short, descriptive name of the feature request.
    slug = db.Column(db.String(200), nullable=False, default=slugify_from_title)
    description = db.Column(db.Text, nullable=True)  # A long description of the feature request.

    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    client = db.relationship("Client",
                             foreign_keys="FeatureRequest.client_id")  # Associated client to the request being raised

    client_priority = db.Column(db.Integer, nullable=True)  # A numbered priority according to the client.
    target_date = db.Column(db.DateTime,
                            default=datetime.now())  # The date that the client is hoping to have the feature.

    product_area_code = db.Column(db.String(200), db.ForeignKey('product_area.code'), nullable=False)
    product_area = db.relationship("ProductArea",
                                   foreign_keys="FeatureRequest.product_area_code")  # Product Area sector

    def __unicode__(self):
        return self.title

    @property
    def name(self):
        return self.title

    def __repr__(self):
        return '<FeatureRequest %r>' % self.title
