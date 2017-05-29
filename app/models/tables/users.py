from hashlib import sha512

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import VARCHAR
from sqlalchemy.dialects.mysql import TINYINT

from app import db, app, g

__all__ = ['Users', 'Groups']


class Users(db.Model):
    __tablename__ = 'users'

    avaible_columns = ['id', 'active', 'login', 'name', 'email', 'api_url', 'github_url', 'avatar_id', 'group_id']

    id = Column(Integer, primary_key=True)
    active = Column(TINYINT(1), nullable=False, default=0)

    login = Column(VARCHAR(50), nullable=False, unique=True)
    password_hash = Column(VARCHAR(256), nullable=False)
    email = Column(VARCHAR(256))

    name = Column(Text)
    github_url = Column(Text)
    api_url = Column(Text)

    avatar_id = Column(Integer, db.ForeignKey('files.id'))
    avatar = db.relationship('Files')

    def __init__(self, login, password, **kwargs):
        self.login = login

        password = sha512((password + login).encode()).hexdigest()
        password = sha512((password + app.config.get('SALT', '')).encode()).hexdigest()

        self.password_hash = password

        self.name = kwargs.pop('name', login)

        for k, v in kwargs.items():
            setattr(self, k, v)

        g.s.add(self)
        g.s.commit()

    @staticmethod
    def create(login, password, **kwargs):
        return Users(login, password, **kwargs)

    def set_password(self, password):
        password = sha512((password + self.login).encode()).hexdigest()
        password = sha512((password + app.config.get('SALT', '')).encode()).hexdigest()

        self.password_hash = password
        g.s.add(self)
        g.s.commit()

    def as_dict(self):
        return {k: getattr(self, k) for k in self.avaible_columns}


class Groups(db.Model):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(50))

    def __init__(self, name):
        self.name = name
        g.s.add(self)
        g.s.commit()


class UsersGroups(db.Model):
    __tablename__ = 'users_groups'

    id = Column(Integer, primary_key=True)
    user_id = db.Column(Integer, db.ForeignKey('users.id'))
    user = db.relationship('Users', backref='groups')  # Fixme?

    group_id = db.Column(Integer, db.ForeignKey('groups.id'))
    group = db.relationship('Groups')
