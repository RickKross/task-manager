from app.models import Users


def get_user_from_db(_id):
    return Users.query.filter_by(id=_id).first()