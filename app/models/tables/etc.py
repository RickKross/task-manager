import os
import re
from hashlib import md5
from urllib.request import urlopen, http

from sqlalchemy import Column
from sqlalchemy import DATE
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import VARCHAR

from app import g, db, app
from app.utils import myprint

__all__ = ['Files', 'Calendar']


def get_file_from_url(request_obj):
    if not isinstance(request_obj, http.client.HTTPResponse):
        return None
    res = b''
    bs = 2 ** 13
    while True:
        block = request_obj.read(bs)
        if not block:
            break
        res += block
    return res


class Files(db.Model):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    path = Column(Text, nullable=False)

    size = Column(Integer)
    hash = Column(VARCHAR(50))

    def __init__(self, path, size=None, hash=None):

        self.path = path
        self.size = size
        self.hash = hash

        g.s.add(self)
        g.s.commit()

    @staticmethod
    def save(path='', source_data='', filename=''):
        data = ''
        if path and not source_data:

            filename = os.path.basename(path)
            try:
                with urlopen(path) as request:
                    data = get_file_from_url(request)
            except ValueError:
                try:
                    with open(path, 'rb') as file:
                        data = file.read()
                except FileNotFoundError:
                    pass

        data = source_data or data
        if not (data and filename):
            return None

        _, ext = os.path.splitext(filename)

        if not ext:
            filename += '.png'
        filename = re.sub('[^a-zA-Z0-9_\-\.]', '_', filename)

        size = len(data)
        _hash = md5(data).hexdigest()
        files_by_size = Files.query.filter_by(size=size)

        if g.s.query(files_by_size.exists()).scalar():
            files_by_size = files_by_size.filter_by(hash=_hash)

        hashed_file = files_by_size.first()

        if not hashed_file:

            new_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # new_path = url_for('static') + filename
            with open(new_path, 'wb') as f:
                f.write(data)
            file = Files(new_path.split('app')[1], size, _hash)
            g.s.commit()
            myprint(file.__dict__, color=32)
            return file

        else:
            return hashed_file


class Calendar(db.Model):
    __tablename__ = 'calendar'

    id = Column(Integer, primary_key=True)

    time = Column(Integer, nullable=False)
    date = Column(DATE, nullable=False)

    user_id = db.Column(Integer, db.ForeignKey('users.id'))
    user = db.relationship('Users')

    task_id = db.Column(Integer, db.ForeignKey('tasks.id'))
    task = db.relationship('Tasks')
