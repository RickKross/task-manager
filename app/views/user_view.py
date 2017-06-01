import datetime
import os

from flask import Blueprint, render_template
from flask import flash
from flask import request
from flask import send_file
from flask import send_from_directory
from flask import url_for
from sqlalchemy import or_
from werkzeug.utils import secure_filename, redirect

from app import app, g
from app.controllers.calendar_controller import get_empty_days, autofinish_day, set_time, export_timesheet
from app.controllers.main_controller import login_required, init_user
from app.models import Projects, Files, Tasks, TaskUser

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
                filepath = os.path.join(g.UPLOAD_FOLDER, filename)
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

    tasks = g.s.query(Tasks).outerjoin(TaskUser, TaskUser.task_id == Tasks.id).filter(
        or_(TaskUser.user == g.user, Tasks.creator == g.user)).all()

    content = {'title': "Все задания", 'user': g.user, 'tasks': tasks}
    return render_template('dash_content.html', **content)


@app.route('/test1')
def test():
    app.d('hi there', color=31)
    app.d(os.path.join(g.UPLOAD_FOLDER, 'logo_1.jpg'))
    # return redirect(url_for('dashboard'))
    return send_from_directory(directory=g.UPLOAD_FOLDER, filename='logo_1.jpg', as_attachment=True)


@app.route('/calendar', methods=['GET', 'POST'])
@init_user
@login_required
def calendar():
    if not (g.user and g.user.name):
        return redirect(url_for('logout'))

    today = datetime.date.today()

    monday = today - datetime.timedelta(days=today.weekday())
    sunday = monday + datetime.timedelta(days=6)
    delta = app.i(request.values.get('d'))
    app.d(delta, color=31)

    weekday = -1 if delta else today.weekday()
    day_started = (g.user.last_started_day - monday).days if g.user.last_started_day else -1
    has_started_day = g.user.last_started_day

    weekdays = [(monday + datetime.timedelta(days=x)).strftime('%a, %d %b').replace('май', 'мая') for x in range(0, 7)]
    empty_days = get_empty_days(monday, weekday)
    errors = autofinish_day()

    if request.method == 'POST':
        action = request.values.get('action')
        if action == 'set_time':
            set_time(request.values)
        elif action == 'export':
            app.d('export')
            return send_file(export_timesheet(), attachment_filename="timesheet.xls", as_attachment=True)

    content = {'title': "Календарь", 'user': g.user}
    return render_template('calendar.html', **content)
