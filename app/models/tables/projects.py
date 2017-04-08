import datetime
from sqlalchemy import Date
from sqlalchemy.orm import relationship

from app import db, g
from app.models.structure.classes import UnicodeString


class Projects(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(UnicodeString(1024))

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner = relationship('Users', backref='projects')

    # TODO projects <-> users assotiation

    def __init__(self, id, name, owner_id=None, owner=None):
        self.id = id
        self.name = name
        if owner:
            self.owner = owner
        elif owner_id:
            self.owner_id = owner_id

        g.s.add(self)
        g.s.commit()


# ticket(_id, name, date, state, priority="Normal", app="", description="", users=[])
class Tickets(db.Model):
    now = datetime.datetime.now()
    __tablename__ = 'Tickets'
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

    def __init__(self, id, name, state, priority='Normal', description='', project_id=None, project=None, deadline=None, commit=True):
        self.id = id
        self.name = name
        self.state = state
        self.priority = priority
        self.description = description

        if project_id:
            self.project_id = project_id
        elif project:
            self.project = project
        else:
            return

        if deadline and isinstance(deadline, datetime.datetime):
            self.dateDeadline = deadline

        g.s.add(self)
        if commit:
            g.s.commit()
