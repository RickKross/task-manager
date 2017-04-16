import os

from flask import Blueprint, render_template
from flask import flash
from flask import request
from flask import url_for
from werkzeug.utils import secure_filename, redirect

from app import app, g
from app.controllers.git_api_controller import get_user
from app.models import Projects
from app.utils import myprint
from config import ALLOWED_EXTENSIONS

profile_view = Blueprint('view', __name__, static_folder='static', template_folder='templates')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/user/<login>', methods=['GET', 'POST'])
def profile(login):
    if not g.user:
        return redirect(url_for('logout'))

    if request.method == 'POST':
        if request.form.get('name'):
            data = {k: v[0] if isinstance(v, list) else v for k, v in request.form.items() if k != 'avatar'}
            data['owner'] = g.user

            file = request.files.get('avatar')
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                data['avatar_path'] = filepath
            myprint(data, color=31)
            Projects(**data)
            flash('its ok')

        return redirect(url_for('profile', login=login))
    projects = Projects.query.filter_by(owner=g.user).all()
    content = {'title': "Profile", 'user': g.user.__dict__, 'projects': projects}
    return render_template('profile.html', **content)
