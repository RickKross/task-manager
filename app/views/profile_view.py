from flask import Blueprint

from app import app

profile_view = Blueprint('view', __name__, static_folder='static', template_folder='templates')

@app.route('/user/<login>')
def profile(login):
   return "Hi, %s" % login
