from flask import Blueprint, redirect, render_template, url_for
from flask import session

from app import app
from app.controllers.base_controller import is_logged
view = Blueprint('view', __name__, static_folder='static', template_folder='templates')


@app.route('/')
def root():
    if is_logged():
        return redirect(url_for('dashboard'))
    else:
        return render_template('auth.html')

