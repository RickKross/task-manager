import os

from flask import Blueprint, render_template
from flask import flash
from flask import request
from flask import session
from flask import url_for
from werkzeug.utils import secure_filename, redirect

from app import app, g
from app.controllers.base_controller import login_required
from app.controllers.git_api_controller import get_user
from app.models import Projects

profile_view = Blueprint('view', __name__, static_folder='static', template_folder='templates')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in g.ALLOWED_EXTENSIONS


@app.route('/user/<login>/projects', methods=['GET', 'POST'])
def projects(login):
    if not session.get('user'):
        return redirect(url_for('logout'))

    if request.method == 'POST':
        if request.form.get('name'):
            data = {k: v[0] if isinstance(v, list) else v for k, v in request.form.items() if k != 'avatar'}
            data['owner'] = session.get('user')

            file = request.files.get('avatar')
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                data['avatar_path'] = filepath
            Projects(**data)
            flash('its ok')

        return redirect(url_for('profile', login=login))
    projects = Projects.query.filter_by(owner=session.get('user')).all()
    content = {'title': "Проекты", 'user': session.get('user'), 'projects': projects}
    return render_template('user_projects.html', **content)


@app.route('/dashboard')
@login_required
def dashboard():
    get_user()
    if not (session.get('user') and session.get('user')['name']):
        return redirect(url_for('logout'))
    content = {'title': "Все тикеты", 'user': session.get('user')}
    return render_template('dash_content.html', **content)


@app.route('/calendar')
@login_required
def calendar():
    get_user()
    if not (session.get('user') and session.get('user')['name']):
        return redirect(url_for('logout'))

    content = {'title': "Календарь", 'user': session.get('user')}
    return render_template('calendar.html', **content)
