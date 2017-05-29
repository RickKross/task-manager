from hashlib import sha512

from sqlalchemy import String

from app import db, app, g
from app.models.structure.classes import UnicodeString

__all__ = ['Users']


class Users(db.Model):
    __tablename__ = 'users'

    avaible_columns = ['id', 'login', 'name', 'email', 'api_url', 'github_url', 'avatar_url']

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(String(64), nullable=False, unique=True)
    password_hash = db.Column(String(256))
    name = db.Column(UnicodeString(1024))
    email = db.Column(String(256), unique=True)
    api_url = db.Column(String(256))
    github_url = db.Column(String(256))
    avatar_url = db.Column(String(256))

    def __init__(self, login, password, email, commit=True, **kwargs):
        self.login = login

        password = sha512((password + login).encode()).hexdigest()
        password = sha512((password + app.config.get('SALT', '')).encode()).hexdigest()

        self.password_hash = password

        self.name = kwargs.pop('name', login)
        self.email = email

        for k, v in kwargs.items():
            setattr(self, k, v)

        g.s.add(self)
        if commit:
            g.s.commit()

    @staticmethod
    def create(login, password, email, **kwargs):
        return Users(login, password, email, **kwargs)

    def set_password(self, password):

        password = sha512((password + self.login).encode()).hexdigest()
        password = sha512((password + app.config.get('SALT', '')).encode()).hexdigest()

        self.password_hash = password
        g.s.add(self)
        g.s.commit()

    def as_dict(self):
        return {k: getattr(self, k) for k in self.avaible_columns}
