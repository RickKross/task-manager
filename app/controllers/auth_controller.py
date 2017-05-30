from hashlib import sha512

from flask import session

from app import app, g
from app.models import Users
from app.utils import myprint


def handle_login(data):
    login = data.get('login')
    password = data.get('password')

    if login and password:
        password = sha512((password + login).encode()).hexdigest()
        password = sha512((password + app.config.get('SALT', '')).encode()).hexdigest()
        user = Users.query.filter_by(login=login, password_hash=password).first()
        if user:
            session['user'] = user.as_dict()
            return True
    return False


def handle_register(data):
    login = data.get('login')
    password = data.get('password')
    email = data.get('email')

    if login and password and email:
        try:
            user = Users.create(login, password, email=email)
            g.s.commit()
            if user:
                session['user'] = user.as_dict()
                return True
        except Exception as e:
            myprint(e, color=35)
    return False
