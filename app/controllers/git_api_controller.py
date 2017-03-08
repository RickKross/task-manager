from urllib.parse import urlencode, urlsplit, parse_qsl
import requests
from flask import session

from uuid import uuid4
from app import CLIENT_ID, CLIENT_SECRET
from app.controllers.base_controller import d


def oauth_request_user_url():
    state = get_state()
    params = {
        'client_id': CLIENT_ID,
        'state': state,
        'scope': 'user, public_repo, repo, repo_deployment, delete_repo'
    }
    return 'https://github.com/login/oauth/authorize?' + urlencode(params)


def oauth_exchange_code_to_token(code):
    state = get_state()
    params = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
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
