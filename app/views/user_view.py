import os

from flask import Blueprint, render_template
from flask import flash
from flask import request
from flask import session
from flask import url_for
from werkzeug.utils import secure_filename, redirect

from app import app, g
from app.controllers.base_controller import login_required, init_user
from app.controllers.git_api_controller import get_user
from app.models import Projects, Users, Files
from app.utils import myprint

profile_view = Blueprint('view', __name__, static_folder='static', template_folder='templates')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in g.ALLOWED_EXTENSIONS


@app.route('/user/<login>/projects', methods=['GET', 'POST'])
@init_user
@login_required
def projects(login):
    myprint(url_for('static', filename='limitless/css/icons/icomoon/styles.css'), color=34)
    user = session.get('user')

    if not user:
        return redirect(url_for('logout'))

    if request.method == 'POST':
        myprint(request.values, color=32)

        if request.values.get('name'):
            myprint(request.values.items(), color=31)
            data = {k: v[0] if isinstance(v, list) else v for k, v in request.values.items() if k != 'avatar'}
            data['owner_id'] = user['id']

            file = request.files.get('avatar')
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                with open(filepath, 'rb') as f:
                    file = Files.save(source_data=f.read(), filename=filename)
                    g.s.commit()

                myprint(file.__dict__, color=31)

                data['avatar'] = file
            data['active'] = 1

            myprint(data, color=33)
            Projects(**data)
            flash('its ok')

        return redirect(url_for('projects', login=login))
    projects = Projects.query.filter_by(owner_id=user['id'], active=1).order_by(Projects.id.desc()).all()
    myprint([el.__dict__ for el in projects], color=34)
    content = {'title': "Профиль", 'user': Users.query.filter_by(id=user['id']).first(), 'projects': projects}
    return render_template('user_projects.html', **content)


@app.route('/dashboard')
@init_user
@login_required
def dashboard():
    user = session.get('user')
    myprint(user)
    if not (user and user['name']):
        return redirect(url_for('logout'))
    content = {'title': "Все тикеты", 'user': Users.query.filter_by(id=user['id']).first()}
    return render_template('dash_content.html', **content)


@app.route('/calendar')
@init_user
@login_required
def calendar():
    user = session.get('user')
    if not (user and user['name']):
        return redirect(url_for('logout'))

    content = {'title': "Календарь", 'user': Users.query.filter_by(id=user['id']).first()}
    return render_template('calendar.html', **content)
