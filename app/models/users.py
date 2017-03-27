from app import app, db, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), unique=True)
    name = db.Column(db.Unicode(128))
    email = db.Column(db.Unicode(128))
    api_url = db.Column(db.Unicode(256))
    github_url = db.Column(db.Unicode(256))
    avatar_url = db.Column(db.Unicode(256))

    def __init__(self, id, login, name, email, api_url, github_url, avatar_url):
        self.id = id
        self.login = login
        self.name = name
        self.email = email
        self.api_url = api_url
        self.github_url = github_url
        self.avatar_url = avatar_url

        g.s.add(self)
        g.s.commit()


