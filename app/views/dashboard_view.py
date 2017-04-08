from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for

from app import app, g
from app.controllers.base_controller import login_required
from app.controllers.git_api_controller import get_user
from app.utils import A, myprint

dashboard_view = Blueprint('dashboard_view', __name__, static_folder='static', template_folder='templates')


@app.route('/dashboard')
@login_required
def dashboard():
    get_user()
    if not (g.user and g.user.name):
        return redirect(url_for('logout'))
    myprint(g.user.__dict__)
    content = {'title': "Dashboard", 'user': g.user.__dict__}
    return render_template('dash_content.html', **content)
