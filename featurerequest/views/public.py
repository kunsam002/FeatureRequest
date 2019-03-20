"""
public.py

@Author: Olukunle Ogunmokun
@Date: 10th Dec, 2018

The public views required to sign up and get started
"""

from flask import Blueprint, render_template, abort, redirect, \
    flash, url_for, request, session, g, make_response, current_app, jsonify, g
from flask_login import logout_user, login_required, login_user, current_user
from datetime import date, datetime, timedelta
from featurerequest.models import *
from sqlalchemy import asc, desc, or_, and_, func
from featurerequest.forms import *
from crud_factory import utils
from featurerequest import login_manager
from flask_principal import Principal, Identity, AnonymousIdentity, identity_changed, PermissionDenied
from featurerequest.services import *
from featurerequest.services.authentication import authenticate
import base64
import time
import json
import urllib
import random
from pprint import pprint
import cgi
import hashlib

www = Blueprint('public', __name__)

ignored_args = ['id', 'date_created', 'last_updated']

captcha_verf_secret = "6Lfv0VkUAAAAAHe-8nm5H0XFJ3OOatgqI0jApcL4"
captcha_verf_url = "https://www.google.com/recaptcha/api/siteverify"

captcha_verf_secret = "6Lfv0VkUAAAAAHe-8nm5H0XFJ3OOatgqI0jApcL4"
captcha_verf_url = "https://www.google.com/recaptcha/api/siteverify"


@app.errorhandler(404)
def page_not_found(e):
    title = "404- Page Not Found"
    error_number = "404"
    error_title = "Page not found!"
    error_info = "The requested page cannot be found or does not exist. Please contact the Administrator."

    return render_template('main/error.html', **locals()), 404


@app.errorhandler(500)
def internal_server_error(e):
    title = "500- Internal Server Error"
    error_number = "500"
    error_title = "Server Error!"
    error_info = "There has been an Internal server Error. Please try again later or Contact the Administrator."

    return render_template('main/error.html', **locals()), 500


def object_length(data):
    return len(data)


def _list_sum(data):
    return sum(data)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@www.context_processor
def main_context():
    """ Include some basic assets in the startup page """

    today = date.today()
    current_year = today.strftime('%Y')
    minimum = min
    string = str
    number_format = utils.number_format
    length = object_length
    join_list = utils.join_list
    slugify = utils.slugify

    list_sum = _list_sum

    return locals()


# logout page
@www.route('/logout/')
def logout():
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(app, identity=AnonymousIdentity())

    resp = redirect(url_for('.index'))
    resp.set_cookie('current_user_id', "", expires=0)
    session.permanent = False
    return resp


@www.route('/login/', methods=["GET", "POST"])
def login():
    title = "Login"
    next_url = request.args.get("next") or url_for(".index")

    form = LoginForm()

    if form.validate_on_submit():
        data = form.data
        username = data["username"]
        password = data["password"]
        user = authenticate(username, password)

        if user is not None:
            login_user(user, remember=True, force=True)  # This is necessary to remember the user

            identity_changed.send(app, identity=Identity(user.id))

            # include the username and api_token in the session

            # logger.info(next_url)
            resp = redirect(next_url)

            # Transfer auth token to the frontend for use with api requests
            key = "%s:%s" % (user.id, user.get_auth_token())
            __xcred = base64.b64encode(key.encode())

            resp.set_cookie("__xcred", __xcred)
            resp.set_cookie("current_user_id", value=str(user.id))
            session.permanent = True

            user.update_last_login()
            return resp

        else:
            login_error = "The username or password is invalid"

    return render_template("main/login.html", **locals())


@www.route('/signup/', methods=["GET", "POST"])
def signup():
    title = "SignUp"
    next_url = request.args.get("next") or url_for(".index")

    form = SignUpForm()

    if form.validate_on_submit():
        data = form.data
        data["password"] = data.get("new_password")

        user = UserService.create(**data)

        if user is not None:
            login_user(user, remember=True, force=True)  # This is necessary to remember the user

            identity_changed.send(app, identity=Identity(user.id))

            # include the username and api_token in the session

            # logger.info(next_url)
            resp = redirect(next_url)

            # Transfer auth token to the frontend for use with api requests
            # __xcred = base64.b64encode("%s:%s" % (user.id, user.get_auth_token()))
            key = "%s:%s" % (user.id, user.get_auth_token())
            __xcred = base64.b64encode(key.encode())

            resp.set_cookie("__xcred", __xcred)
            resp.set_cookie("current_user_id", value=str(user.id))
            session.permanent = True
            return resp

        else:
            login_error = "The username or password is invalid"

    return render_template("main/signup.html", **locals())


@www.route('/')
def index():
    title = "Home"
    users_count = User.query.count()
    requests_count = FeatureRequest.query.count()
    clients_count = Client.query.count()
    return render_template("main/index.html", **locals())


@www.route('/clients/')
def clients():
    try:
        page = int(request.args.get("page", 1))
        pages = request.args.get("pages")
    except:
        abort(404)
    title = "Clients"
    request_args = utils.copy_dict(request.args, {})

    query = Client.query

    results = query.paginate(page, 100, False)
    if results.has_next:
        # build next page query parameters
        request_args["page"] = results.next_num
        results.next_page = "%s%s" % ("?", urllib.urlencode(request_args))

    if results.has_prev:
        # build previous page query parameters
        request_args["page"] = results.prev_num
        results.previous_page = "%s%s" % ("?", urllib.urlencode(request.args))

    return render_template("main/clients.html", **locals())


@www.route('/requests/')
def all_requests():
    try:
        page = int(request.args.get("page", 1))
        pages = request.args.get("pages")
    except:
        abort(404)

    title = "Feature Requests"
    request_args = utils.copy_dict(request.args, {})

    query = FeatureRequest.query.join(Client).order_by(Client.name)

    results = query.paginate(page, 100, False)
    if results.has_next:
        # build next page query parameters
        request_args["page"] = results.next_num
        results.next_page = "%s%s" % ("?", urllib.urlencode(request_args))

    if results.has_prev:
        # build previous page query parameters
        request_args["page"] = results.prev_num
        results.previous_page = "%s%s" % ("?", urllib.urlencode(request.args))

    return render_template("main/requests.html", **locals())


@www.route('/product_areas/')
def product_areas():
    try:
        page = int(request.args.get("page", 1))
        pages = request.args.get("pages")
    except:
        abort(404)

    title = "Product Areas"
    request_args = utils.copy_dict(request.args, {})

    query = ProductArea.query

    results = query.paginate(page, 100, False)
    if results.has_next:
        # build next page query parameters
        request_args["page"] = results.next_num
        results.next_page = "%s%s" % ("?", urllib.urlencode(request_args))

    if results.has_prev:
        # build previous page query parameters
        request_args["page"] = results.prev_num
        results.previous_page = "%s%s" % ("?", urllib.urlencode(request.args))

    return render_template("main/product_areas.html", **locals())


@www.route('/requests/create/', methods=['GET', 'POST'])
@login_required
def create_request():
    title = "Create Feature Request"

    form = RequestForm()
    form.client_id.choices = [(0, "--- Choose a Client ---")] + [(i.id, i.name) for i in ClientService.query.all()]
    form.client_priority.choices = [(0, "--- Specify Request Priority ---")] + [(i, i) for i in range(1, 11)]
    form.product_area_code.choices = [(0, "--- Select a Product Area ---")] + [(i.code, i.name) for i in
                                                                               ProductAreaService.query.all()]

    if form.validate_on_submit():
        data = form.data
        data["user_id"] = current_user.id
        obj = FeatureRequestService.create(**data)

        return redirect(url_for('.all_requests'))

    return render_template("main/create_request.html", **locals())


@www.route('/requests/<int:id>/update/', methods=['GET', 'POST'])
@login_required
def update_request(id):
    title = "Update Feature Request"
    next_url = request.args.get("next") or url_for(".index")

    obj = FeatureRequestService.query.get(id)
    if not obj:
        abort(404)

    if obj.user_id != current_user.id:
        abort(404)

    form = RequestForm(obj=obj)
    form.client_id.choices = [(0, "--- Choose a Client ---")] + [(i.id, i.name) for i in ClientService.query.all()]
    form.client_priority.choices = [(0, "--- Specify Request Priority ---")] + [(i, i) for i in range(1, 11)]
    form.product_area_code.choices = [(0, "--- Select a Product Area ---")] + [(i.code, i.name) for i in
                                                                               ProductAreaService.query.all()]

    if form.validate_on_submit():
        data = form.data
        data["user_id"] = current_user.id
        obj = FeatureRequestService.update(obj.id, **data)

        return redirect(url_for('.all_requests'))

    return render_template("main/create_request.html", **locals())
