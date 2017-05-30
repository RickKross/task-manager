import pprint
from functools import wraps

from flask import redirect, session, url_for

from app.controllers.git_api_controller import get_user


def d(v, color=30, end='\n'):
    print("\033[1;%sm" % color, end=end)
    pprint.pprint(v)
    print('\033[1;37m ', end=end)


def is_logged():
    if session.get('token') is not None or session.get('user') is not None:
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
            return redirect(url_for('root'))

    return wrapper


def init_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        dest = get_user()
        if dest:
            return redirect(dest)
        else:
            return func(*args, **kwargs)

    return wrapper
