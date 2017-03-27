SECRET_KEY = 'you-will-never-guess'
SALT = 'SALT'

DB_USER = 'root'
DB_PASS = 'root'
DB_NAME = 'tm_diplom'
DB_HOST = 'localhost'


SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(DB_USER, DB_PASS, DB_HOST, DB_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = True