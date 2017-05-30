import errno
import os

from flask import Flask
from flask import redirect
from flask import session
from flask import url_for
from flask_sqlalchemy import SQLAlchemy

from .utils import A, myprint

app = Flask(__name__, static_folder='static')
app.config.from_object('config.DevConf')

g = A()
g.CLIENT_ID = app.config.get('CLIENT_ID')
g.CLIENT_SECRET = app.config.get('CLIENT_SECRET')
g.ALLOWED_EXTENSIONS = app.config.get('ALLOWED_EXTENSIONS')
g.UPLOAD_FOLDER = app.config.get('UPLOAD_FOLDER')


if not os.path.isdir(g.UPLOAD_FOLDER):
    try:
        os.makedirs(g.UPLOAD_FOLDER)
        os.chmod(g.UPLOAD_FOLDER, 777)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(g.UPLOAD_FOLDER):
            pass
        else:
            raise

db = SQLAlchemy(app)
db.create_all()

g.s = db.session

from app.views.base_view import view
from app.views.auth_view import auth_view
from app.views.dashboard_view import dashboard_view
from app.views.user_view import profile_view
from app.views import get_user_from_db


@app.before_request
def be4_request():
    user = session.get('user')
    if not user and g.user:
        return
    if not (g.user and g.user.id == user['id']) and user:
        g.user = get_user_from_db(user['id'])

# csrf = CsrfProtect()
# CsrfProtect(app)
# csrf.init_app(app)
