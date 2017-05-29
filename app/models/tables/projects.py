import datetime

from sqlalchemy import Column, Integer, VARCHAR, DATE, DATETIME, Text
from sqlalchemy.dialects.mysql import TINYINT

from app import db, g

__all__ = ['Projects', 'Releases', 'Tasks', 'TaskStates', 'TaskPrior', 'TaskUser']


# TODO META?


class Projects(db.Model):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(100), nullable=False, unique=True)
    active = Column(TINYINT(1), nullable=False, default=0)

    company_name = Column(VARCHAR(255))
    company_location = Column(VARCHAR(255))
    company_url = Column(VARCHAR(255))
    description = Column(Text)

    avatar_id = Column(Integer, db.ForeignKey('files.id'))
    avatar = db.relationship('Files')

    owner_id = db.Column(Integer, db.ForeignKey('users.id'))
    owner = db.relationship('Users', backref='projects')

    def __init__(self, name, **kwargs):
        self.name = name

        for k, v in kwargs.items():
            setattr(self, k, v)

        g.s.add(self)
        g.s.commit()


class Releases(db.Model):
    __tablename__ = 'releases'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(100), nullable=False)
    active = Column(TINYINT(1), nullable=False, default=0)
    deadline = Column(DATE)

    project_id = Column(Integer, db.ForeignKey('projects.id'))
    project = db.relationship('Projects')

    def __init__(self, name, **kwargs):
        self.name = name

        for k, v in kwargs.items():
            setattr(self, k, v)

        g.s.add(self)
        g.s.commit()


class Tasks(db.Model):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(100), nullable=False)
    active = Column(TINYINT(1), nullable=False, default=0)

    description = Column(Text)

    date_create = Column(DATETIME, nullable=False, default=datetime.datetime.now())
    date_modify = Column(DATETIME, nullable=False, default=datetime.datetime.now())
    date_deadline = Column(DATE)

    release_id = db.Column(Integer, db.ForeignKey('releases.id'))
    release = db.relationship('Releases', backref='tasks')

    state_id = db.Column(Integer, db.ForeignKey('tasks_states.id'))
    state = db.relationship('TaskStates', backref='tasks')

    priority_id = db.Column(Integer, db.ForeignKey('task_prior.id'))
    priority = db.relationship('TaskPrior', backref='tasks')

    creator_id = db.Column(Integer, db.ForeignKey('users.id'))
    creator = db.relationship('Users', backref='tasks')

    def __init__(self, name, **kwargs):
        self.name = name

        for k, v in kwargs.items():
            setattr(self, k, v)

        g.s.add(self)
        g.s.commit()


class TaskStates(db.Model):
    __tablename__ = 'tasks_states'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(50), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name
        g.s.add(self)
        g.s.commit()


class TaskPrior(db.Model):
    __tablename__ = 'task_prior'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(50), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name
        g.s.add(self)
        g.s.commit()


class TaskUser(db.Model):
    __tablename__ = 'tasks_users'
    id = Column(Integer, primary_key=True)

    task_id = db.Column(Integer, db.ForeignKey('tasks.id'), nullable=False)
    task = db.relationship('Tasks')

    user_id = db.Column(Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('Users')

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        g.s.add(self)
        g.s.commit()


class Comments(db.Model):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)

    date_create = Column(DATETIME)

    owner_id = db.Column(Integer, db.ForeignKey('users.id'))
    owner = db.relationship('Users')

    task_id = db.Column(Integer, db.ForeignKey('tasks.id'))
    task = db.relationship('Tasks')

    def __init__(self, text, **kwargs):
        self.text = text

        for k, v in kwargs.items():
            setattr(self, k, v)

        g.s.add(self)
        g.s.commit()


class CommentsFiles(db.Model):
    __tablename__ = 'comments_files'
    
    id = Column(Integer, primary_key=True)

    comment_id = db.Column(Integer, db.ForeignKey('comments.id'))
    comment = db.relationship('Comments')

    file_id = db.Column(Integer, db.ForeignKey('files.id'))
    file = db.relationship('Files')

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        g.s.add(self)
        g.s.commit()
