from flask import Blueprint, redirect, render_template, url_for
from flask import session

from app import app
from app.controllers.base_controller import is_logged
from app.controllers.git_api_controller import oauth_request_user_url

view = Blueprint('view', __name__, static_folder='static', template_folder='templates')


@app.route('/')
def root():
    if is_logged():
        return redirect(url_for('dashboard'))
    else:
        return redirect(oauth_request_user_url())


@app.route('/clear-sesion')
def clear():
    session.clear()
    return redirect(url_for('root'))


