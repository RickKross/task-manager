import json
from urllib.parse import urlencode, urlsplit, parse_qsl
from uuid import uuid4

import requests
from flask import session
from flask import url_for
from werkzeug.routing import RequestRedirect

from app import g
from app.models import Files
from app.models.tables.users import Users


def oauth_request_user_url():
    """
    Функция генерации url, при переходе по которому 
    пользователю будет предложено авторизоваться в системе GitHub
    """
    # параметры запроса
    params = {
        'client_id': g.CLIENT_ID,  # id приложения (находится в настройках GitHub)
        'state': get_state(),
        
        # разрешения доступа (данные пользователя, данные репозиториев и тп)
        'scope': 'user, public_repo, repo, repo_deployment, delete_repo'  
    }
    return 'https://github.com/login/oauth/authorize?' + urlencode(params)


def oauth_exchange_code_to_token(code):
    """
    Функция обмена кода на токен доступа
    :param code: код
    :return: данные ответа от сервера GitHub, содержащие (при успешном обмене) токен доступа
    """
    state = get_state()
    # параметры запроса
    params = {
        'client_id': g.CLIENT_ID,
        'client_secret': g.CLIENT_SECRET,
        'state': state,
        'code': code
    }
    # отправляем запрос к GitHub
    r = requests.post('https://github.com/login/oauth/access_token', data=params)
    # если запрос успешен
    if r.status_code == 200:
        # достаем словарь данных из запроса и возвращаем его
        data = dict(parse_qsl(urlsplit(r.text).path))
        return data
    else:
        return None


def get_state():
    """
    Функция генерирует уникальное значение, использующееся для подтверждения обменов с GitHub:
    если в процессе запроса вернулся не переданный state, что-то не так
    """
    state = session['state'] = session.get('state', str(uuid4()))
    return state


def get_user():
    if session.get('user') and session.get('user')['login'] or g.user and g.user.login:
        return None

    if session.get('token'):
        r = requests.get('https://api.github.com/user', {'access_token': session['token']})
        if r.status_code == 200 and r.text:
            r = json.loads(r.text)

            user = Users.query.filter_by(id=r['id']).first()
            if user:
                g.user = user
                return None
            else:
                file = Files.save(r['avatar_url'])
                user = Users.create(id=r['id'],
                                    login=r['login'],
                                    password='',
                                    name=r['name'],
                                    email=r['email'],
                                    api_url=r['url'],
                                    github_url=r['html_url'],
                                    avatar=file)
                g.user = user
                session['user_need_password'] = {user.id: True}
                raise RequestRedirect(url_for('auth_set_password'))
        else:
            # TODO err with http code
            pass
    else:
        # TODO session token err
        pass
