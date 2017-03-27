from flask import Blueprint, render_template, request, session, redirect, url_for

from app import app
from app.controllers.base_controller import d
from app.controllers.git_api_controller import oauth_exchange_code_to_token
from app.utils import myprint

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


@app.route('/auth/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('root'))
