import os
from hashlib import md5
from urllib.request import urlopen, http

from flask import url_for
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import VARCHAR

from app import g, db

__all__ = ['Files']


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
    def save(path):
        filename = os.path.basename(path)
        data = ''
        try:
            with urlopen(path) as request:
                data = get_file_from_url(request)
        except ValueError:
            try:
                with open(path, 'rb') as file:
                    data = file.read()
            except FileNotFoundError:
                pass

        if not data:
            return None

        size = len(data)
        _hash = md5(data).hexdigest()
        files_by_size = Files.query.filter_by(size=size)

        if g.s.query(files_by_size.exists()).scalar():
            files_by_size = files_by_size.filter_by(hash=_hash)

        hashed_file = files_by_size.first()

        if not hashed_file:
            new_path = url_for('static') + filename
            with open(new_path, 'wb') as f:
                f.write(data)
            Files(new_path, size, _hash)
        else:
            return hashed_file
