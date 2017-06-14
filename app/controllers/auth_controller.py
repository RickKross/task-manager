from hashlib import sha512

from flask import session

from app import app, g
from app.models import Users


def handle_login(data):
    """
    Функция авторизации пользователя
    :param data: параметры запроса
    :return: True в случае успешной авторизации; False в случае неудачной
    """
    # достаем параметры авторизации
    login = data.get('login')
    password = data.get('password')

    if login and password:
        # хешируем пароль
        password = sha512((password + login).encode()).hexdigest()
        password = sha512((password + app.config.get('SALT', '')).encode()).hexdigest()
        # досьаем из БД пользователя с переданным логином и хешем пароля
        user = Users.query.filter_by(login=login, password_hash=password).first()
        if user:
            # если такой пользователь есть, сохраняем его в сессии
            g.user = user
            return True
    return False


def handle_register(data):
    """
    Функция регистрации пользователя
    :param data: параметры запроса
    :return: True в случае успешной регистрации; False в случае неудачной
    """
    # получаем ключевые для регистрации параметры из запроса
    login = data.get('login')
    password = data.get('password')
    email = data.get('email')

    # если они все на месте, пробуем создать пользователя
    if login and password and email:
        try:
            user = Users.create(login, password, email=email)
            g.s.commit()
            if user:
                # заносим пользователя в данные сессии
                g.user = user
                return True
        except Exception:
            pass
    return False
