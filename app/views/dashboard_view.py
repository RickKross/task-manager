from flask import Blueprint
from flask import render_template

from app import app
from app.controllers.base_controller import login_required

dashboard_view = Blueprint('dashboard_view', __name__, static_folder='static', template_folder='templates')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dash_content.html')
