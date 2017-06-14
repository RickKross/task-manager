from flask import Blueprint, render_template, request, session, redirect, url_for

from app import app, g
from app.controllers.auth_controller import handle_login, handle_register
from app.controllers.git_api_controller import oauth_exchange_code_to_token, oauth_request_user_url

auth_view = Blueprint('auth_view', __name__, static_folder='static', template_folder='templates')


@app.route('/auth', methods=['GET'])
def auth_index():
    """
    Функция обработки запросов с данными авторизации, пришедших с GitHub (адрес настраивается в GitHub)
    """
    state = request.args.get('state')
    # проверяем ,что state текущего обмена у нас есть, а не пришел откуда-то с третьей стороны
    if state in session.get('state', ''):
        # получаем из запроса код и меняем его на токен доступа
        code = request.args.get('code')
        data = oauth_exchange_code_to_token(code)
        # если токен есть, сохраняем его  в сессии и переходим на главный экран
        if data and data.get('access_token'):
            session['token'] = data['access_token']
            return redirect(url_for('dashboard'))

    # если что-то пошло не так, разлогиниваем пользователя
    return redirect(url_for('logout'))


@app.route('/auth/github')
def auth_via_github():
    """
    При заходе на страницу '/auth/github' пользователя переадресует на GitHub для авторизации с помощью этого сервиса
    """
    return redirect(oauth_request_user_url())


@app.route('/auth/login', methods=['POST'])
def auth_login():
    # если авторизация успешна, переходим на гравный экран. иначе назад к авторизации
    if handle_login(request.values):
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('root'))


@app.route('/auth/register', methods=['POST'])
def auth_register():
    # если авторизация успешна, переходим на гравный экран. иначе назад к регистрации
    if handle_register(request.values):
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
