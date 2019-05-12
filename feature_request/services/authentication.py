"""
authentication.py

@Author: Olukunle Ogunmokun
@Date: April 2019

Authentication service for managing verifying credentials & permissions
"""
from flask_login import current_user
from flask_principal import identity_changed, UserNeed, RoleNeed
from sqlalchemy import or_
from feature_request.models import *

login_manager = app.login_manager


@login_manager.user_loader
def load_user(user_id):
    """
    Retrieves a user using the id stored in the session.

    :param userid: The user id (fetched from the session)

    :returns: the logged in user or None

    """
    return User.query.get(user_id)


@identity_changed.connect_via(app)
def on_identity_loaded(sender, identity):
    """
    Loads a current user's roles into the identity context
    """

    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, "id"):
        identity.provides.add(UserNeed(current_user.id))

    # Assuming the current user has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(current_user, "roles"):
        user_roles = current_user.roles.split(",") if current_user.roles else []
        for user_role in user_roles:
            identity.provides.add(RoleNeed(user_role.role.name))


def authenticate(username, password, **kwargs):
    """
    Fetch a user based on the given username and password.

    :param username: the username (or email address) of the user
    :param password: password credential
    :param kwargs: additional parameters required

    :returns: a user object or None
    """
    # user_login_attempted.send(username)

    user = User.query.filter(or_(func.lower(User.username) == username.lower(),
                                 func.lower(User.email) == username.lower())).first()
    if user and user.check_password(password):
        return user
    return None


def authenticate_admin(username, password, **kwargs):
    """
    Fetch a user based on the given username and password.

    :param username: the username (or email address) of the user
    :param password: password credential
    :param kwargs: additional parameters required

    :returns: a user object or None
    """
    # user_login_attempted.send(username)
    user = User.query.filter(or_(func.lower(User.username) == username.lower(),
                                 func.lower(User.email) == username.lower())).first()

    if user and user.check_password(password):
        return user
    return None


def require_basic_auth(realm="FeatureRequest API"):
    """ Sends a 401 Authorization required response that enables basic auth """

    message = "Could not authorize your request. Provide the proper login credentials to continue."

    headers = {"WWW-Authenticate": "Basic realm='%s'" % realm}
    status = 401

    return message, status, headers  # body, status and headers


def check_basic_auth(username, auth_token, **kwargs):
    """
    Fetch a user based on the given username and token key given.
    This is used along with HTTP Basic Authentication

    :param username: the username (or email address) of the user
    :param auth_token: authentication token generated for the user
    :returns: a user object or None
    """

    user = User.query.filter(
        or_(func.lower(User.username) == username.lower(), func.lower(User.email) == username.lower())).first()

    if user and auth_token == user.get_auth_token():
        return user
    else:
        return None


def check_user_auth(username, auth_token, **kwargs):
    """
    Fetch a client based on the given username and token key given.
    This is client along with HTTP Basic Authentication

    :param username: the username (or email address) of the user
    :param auth_token: authentication token generated for the user
    :returns: a user object or None
    """

    user = User.query.filter(or_(User.username == username, User.email == username)).first()
    if user and auth_token == user.get_auth_token():
        return user
    else:
        return None


def get_activity_user():
    """ Load the current user to log an activity for this user. If there is no flask context, log the user as the default system user """

    system_username = app.config.get("SYSTEM_USERNAME", None)

    if not system_username:
        raise Exception("SYSTEM_USERNAME configuration MUST be set")
    try:
        if current_user.id:
            return current_user
        else:
            return User.query.filter(func.lower(User.username) == system_username.lower()).first()
    except:
        return User.query.filter(func.lower(User.username) == system_username.lower()).first()
