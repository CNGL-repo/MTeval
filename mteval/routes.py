from mteval import app

from flask import render_template, flash, redirect, url_for, request, make_response, send_from_directory
from flask.ext.login import request, current_user, LoginManager, logout_user, login_required
from forms import LoginForm, RegisterForm, EditTeamForm, CompetitionForm, CompetitionEditForm
from database import teamDB, compDB
import loginUtils
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
from urlparse import urlparse, urljoin
from werkzeug import secure_filename
import os


##UTILS
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def get_redirect_target():
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target

def safeRedirect(endpoint="index", **values):
    next = request.args.get("next")
    if is_safe_url(next):
        return redirect(next)
    target = get_redirect_target()
    return redirect(target or url_for(endpoint, **values))