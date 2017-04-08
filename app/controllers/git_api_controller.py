import json
from urllib.parse import urlencode, urlsplit, parse_qsl
from uuid import uuid4

import requests
from flask import session

from app import g
from app.models.tables.users import Users
from app.utils import myprint


def oauth_request_user_url():
    params = {
        'client_id': g.CLIENT_ID,
        'state': get_state(),
        'scope': 'user, public_repo, repo, repo_deployment, delete_repo'
    }
    return 'https://github.com/login/oauth/authorize?' + urlencode(params)


def oauth_exchange_code_to_token(code):
    state = get_state()
    params = {
        'client_id': g.CLIENT_ID,
        'client_secret': g.CLIENT_SECRET,
        'state': state,
        'code': code
    }
    r = requests.post('https://github.com/login/oauth/access_token', data=params)
    if r.status_code == 200:
        data = dict(parse_qsl(urlsplit(r.text).path))
        return data
    else:
        return None


def get_state():
    state = session['state'] = session.get('state', str(uuid4()))
    return state


def get_user():
    if session.get('token'):
        if g.user and g.user.login:
            return g.user
        else:
            r = requests.get('https://api.github.com/user', {'access_token': session['token']})
            if r.status_code == 200 and r.text:
                r = json.loads(r.text)
                myprint(r, color=32)
                g.user = Users.query.filter_by(id=r['id']).first() or Users(id=r['id'],
                                                                            login=r['login'],
                                                                            name=r['name'],
                                                                            email=r['email'],
                                                                            api_url=r['url'],
                                                                            github_url=r['html_url'],
                                                                            avatar_url=r['avatar_url'])
            else:
                # TODO err with http code
                pass
    else:
        # TODO session token err
        pass
