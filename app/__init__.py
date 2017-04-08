from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.utils import A

app = Flask(__name__)
app.config.from_object('config')

g = A()  # cuz global context sux .-.
g.user = ''
g.CLIENT_ID = 'fd3ec610b0a0f02435c3'
g.CLIENT_SECRET = '622c8b9ed8089369fbd3d4ccfb626a7891946689'

db = SQLAlchemy(app)
db.create_all()

g.s = db.session

from app.views.base_view import view
from app.views.auth_view import auth_view
from app.views.dashboard_view import dashboard_view
from app.views.profile_view import profile_view

# csrf = CsrfProtect()
# CsrfProtect(app)
# csrf.init_app(app)











