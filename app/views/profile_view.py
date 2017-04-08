from flask import Blueprint, render_template

from app import app, g
from app.controllers.git_api_controller import get_user

profile_view = Blueprint('view', __name__, static_folder='static', template_folder='templates')


@app.route('/user/<login>')
def profile(login):
    if not g.user:
        get_user()
    content = {'title': "Profile", 'user': g.user.__dict__}
    return render_template('profile.html', **content)
