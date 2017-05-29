from flask import Blueprint
dashboard_view = Blueprint('dashboard_view', __name__, static_folder='static', template_folder='templates')


