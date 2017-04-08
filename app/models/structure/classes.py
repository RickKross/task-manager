from sqlalchemy import BINARY
from sqlalchemy import Binary
from sqlalchemy import TypeDecorator


class UnicodeString(TypeDecorator, Binary):
    """
    Потому что просто Unicode sux.
    В базе данные хранятся в байтах
    При доставании, декодируются в юникод
    """

    impl = BINARY()

    def process_bind_param(self, value, dialect):
        return value.encode()

    def process_result_value(self, value, dialect):
        return None if value is None else (value.decode() if type(value) is bytes else value)
