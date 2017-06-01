from flask import Blueprint, render_template, request, session, redirect, url_for

from app import app, g
from app.controllers.auth_controller import handle_login, handle_register
from app.controllers.git_api_controller import oauth_exchange_code_to_token, oauth_request_user_url

auth_view = Blueprint('auth_view', __name__, static_folder='static', template_folder='templates')


@app.route('/auth', methods=['GET'])
def auth_index():
    if request.method == 'GET':
        state = request.args.get('state')
        if state in session.get('state', ''):
            code = request.args.get('code')
            data = oauth_exchange_code_to_token(code)
            if data and data.get('access_token'):
                session['token'] = data['access_token']

                return redirect(url_for('dashboard'))
            else:
                pass  # FIXME auth error
                return render_template('auth.html', myvar='auth error')
        else:
            return render_template('auth.html', myvar='403')


@app.route('/auth/github')
def auth_via_github():
    return redirect(oauth_request_user_url())


@app.route('/auth/login', methods=['POST'])
def auth_login():
    status = handle_login(request.values)
    if status:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('root'))


@app.route('/auth/register', methods=['POST'])
def auth_register():
    status = handle_register(request.values)
    if status:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('root'))


@app.route('/auth/set_password', methods=['GET', 'POST'])
def auth_set_password():
    if request.method == 'GET':
        content = {'user_id': g.user and g.user.id}
        return render_template('set_password.html', **content)
    elif request.method == 'POST':

        password = request.values.get('password')
        if g.user and session.get('user_need_password') and session.get('user_need_password')[str(g.user.id)] and password:
            g.user.set_password(password)
    return redirect(url_for('root'))


@app.route('/auth/logout', methods=['GET'])
def logout():
    session.clear()
    g.user = None
    return redirect('/')
