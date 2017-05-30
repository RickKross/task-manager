import os

from flask import Blueprint, render_template
from flask import flash
from flask import request
from flask import session
from flask import url_for
from sqlalchemy import or_
from werkzeug.utils import secure_filename, redirect

from app import app, g
from app.controllers.base_controller import login_required, init_user
from app.models import Projects, Users, Files, Tasks, TaskUser
from app.utils import myprint

profile_view = Blueprint('view', __name__, static_folder='static', template_folder='templates')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in g.ALLOWED_EXTENSIONS


@app.route('/user/<login>/', methods=['GET', 'POST'])
@init_user
@login_required
def profile(login):


    if not g.user:
        return redirect(url_for('logout'))

    if request.method == 'POST':
        if request.values.get('name'):
            data = {k: v[0] if isinstance(v, list) else v for k, v in request.values.items() if k != 'avatar'}
            data['owner'] = g.user

            file = request.files.get('avatar')
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                with open(filepath, 'rb') as f:
                    file = Files.save(source_data=f.read(), filename=filename)
                    g.s.commit()

                data['avatar'] = file
            data['active'] = 1

            Projects(**data)
            flash('its ok')

        return redirect(url_for('profile', login=login))
    projects = Projects.query.filter_by(owner=g.user, active=1).order_by(Projects.id.desc()).all()
    content = {'title': "Профиль", 'user': g.user, 'projects': projects}
    return render_template('user_projects.html', **content)


@app.route('/dashboard')
@init_user
@login_required
def dashboard():
    if not (g.user and g.user.name):
        return redirect(url_for('logout'))

    tasks = g.s.query(Tasks).outerjoin(TaskUser, TaskUser.task_id == Tasks.id).filter(or_(TaskUser.user == g.user, Tasks.creator == g.user)).all()

    content = {'title': "Все задания", 'user': g.user, 'tasks': tasks}
    return render_template('dash_content.html', **content)


@app.route('/calendar')
@init_user
@login_required
def calendar():
    if not (g.user and g.user.name):
        return redirect(url_for('logout'))

    content = {'title': "Календарь", 'user': g.user}
    return render_template('calendar.html', **content)
