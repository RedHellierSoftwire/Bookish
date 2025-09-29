from flask import request, Blueprint
from bookish.models.DB.users import User
from bookish.models import db

blueprint = Blueprint('user', __name__, url_prefix='/users')

@blueprint.route('/', methods=['GET'])
def get_users():
    users = db.session.execute(db.select(User).order_by(User.first_name)).scalars().all()
    userResults = [user.serialize() for user in users]
    return {"users": userResults}

