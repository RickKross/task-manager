from flask import Blueprint
from flask import render_template
from flask import session

from app import app, g
from app.controllers.base_controller import login_required
from app.controllers.git_api_controller import get_user
from app.utils import A, myprint

dashboard_view = Blueprint('dashboard_view', __name__, static_folder='static', template_folder='templates')


@app.route('/dashboard')
@login_required
def dashboard():
    get_user()
    content = {'title': "Dashboard", 'user': g.user.__dict__}
    return render_template('dash_content.html', **content)
