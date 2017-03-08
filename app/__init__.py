import pprint

from flask import Flask
# from flask_wtf import CsrfProtect
from flask import session

app = Flask(__name__)
# CONSTANTS
CLIENT_ID = 'fd3ec610b0a0f02435c3'
CLIENT_SECRET = '622c8b9ed8089369fbd3d4ccfb626a7891946689'
app.config.from_object('config')

from app.views.base_view import view
from app.views.auth_view import auth_view
from app.views.dashboard_view import dashboard_view
# db = SQLAlchemy(app)
# db.create_all()

# csrf = CsrfProtect()
# CsrfProtect(app)
# csrf.init_app(app)











