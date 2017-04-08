from sqlalchemy import String

from app import db, g

from app.models.structure.classes import UnicodeString


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(String(256), nullable=False)
    name = db.Column(UnicodeString(1024))
    email = db.Column(String(256))
    api_url = db.Column(String(256))
    github_url = db.Column(String(256))
    avatar_url = db.Column(String(256))

    def __init__(self, id, login, name, email, api_url, github_url, avatar_url, commit=True):
        self.id = id
        self.login = login
        self.name = name
        self.email = email
        self.api_url = api_url
        self.github_url = github_url
        self.avatar_url = avatar_url
        g.s.add(self)

        if commit:
            g.s.commit()


