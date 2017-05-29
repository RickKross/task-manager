import datetime

from sqlalchemy import Date
from sqlalchemy.orm import relationship

from app import db, g
from app.models.structure.classes import UnicodeString

__all__ = ['Projects', 'Tickets']


class Projects(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(UnicodeString(1024))
    companyName = db.Column(UnicodeString(1024))
    companyLocation = db.Column(UnicodeString(1024))
    link = db.Column(UnicodeString(1024))
    avatar_path = db.Column(UnicodeString(1024))
    description = db.Column(UnicodeString(4096))

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner = relationship('Users', backref='projects')

    # TODO projects <-> users assotiation

    def __init__(self, name, **kwargs):
        self.name = name

        for k, v in kwargs.items():
            setattr(self, k, v)

        g.s.add(self)
        g.s.commit()


# ticket(_id, name, date, state, priority="Normal", app="", description="", users=[])
class Tickets(db.Model):
    now = datetime.datetime.now()
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(UnicodeString(1024))
    state = db.Column(UnicodeString(512))
    priority = db.Column(UnicodeString(512))

    description = db.Column(UnicodeString(1000))

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    project = relationship('Projects', backref='tickets')

    # TODO tickets <-> users assotiation

    dateCreate = db.Column(Date, default=now)
    dateModify = db.Column(Date, default=now)

    dateDeadline = db.Column(Date, default=now + datetime.timedelta(days=7))

    def __init__(self, id, name, state, **kwargs):
        self.id = id
        self.name = name
        self.state = state

        for k, v in kwargs.items():
            setattr(self, k, v)

        g.s.add(self)
        g.s.commit()
