from functools import wraps

from flask import redirect, session, url_for

from app import g
from app.controllers.git_api_controller import get_user


def is_logged():
    if session.get('token') is not None or session.get('user') is not None or (g.user is not None and g.user.name is not None):
        return True
    else:
        return False


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if is_logged():  # TODO or try_login
            return func(*args, **kwargs)
        else:
            # FIXME 403?
            return redirect(url_for('logout'))

    return wrapper


def init_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        get_user()
        return func(*args, **kwargs)

    return wrapper
