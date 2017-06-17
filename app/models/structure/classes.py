from sqlalchemy import BLOB
from sqlalchemy import LargeBinary
from sqlalchemy import TypeDecorator

from app import g


class UnicodeString(TypeDecorator, LargeBinary):
    """
    Потому что просто Unicode sux.
    В базе данные хранятся в байтах
    При доставании, декодируются в юникод
    """

    impl = BLOB()

    def process_bind_param(self, value, dialect):
        return value.encode()

    def process_result_value(self, value, dialect):
        return None if value is None else (value.decode() if type(value) is bytes else value)


class Base(object):
    __table_args__ = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    def __init__(self, s=g.s, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for k, v in kwargs:
            try:
                setattr(self, k, v)
            except:
                pass
            
        s.add(self)
        s.commit()

    @classmethod
    def _all(cls, filter):
        return g.s.query(cls).filter_by(**filter) if filter else g.s.query(cls)

    @classmethod
    def all(cls, **kwargs):
        return cls._all(kwargs)

    @classmethod
    def first(cls, **kwargs):
        return cls._all(kwargs).first()

    @classmethod
    def last(cls, **kwargs):
        return cls._all(kwargs).last()

    @classmethod
    def create(cls, **kwargs):
        o = cls(**kwargs)
        g.s.commit()
        return o
    
    def remove(self):
        g.s.delete(self)
        g.s.commit()
