from flask import jsonify, request, Blueprint
from bookish.models.DB.users import User, UserAuth
from bookish.models import db

blueprint = Blueprint('user', __name__, url_prefix='/users')

@blueprint.route('/', methods=['GET'])
def get_users():
    users = db.session.execute(db.select(User).order_by(User.first_name)).scalars().all()
    userResults = [user.serialize() for user in users]
    return {"users": userResults}

@blueprint.route('/authenticate', methods=["POST"])
def authenticate_user():
    request_body = request.get_json()
    if not request_body or not 'username' in request_body or not 'password' in request_body:
        return jsonify({"error": "Missing username or password"}), 400
    
    username = request_body['username']
    password = request_body['password']

    user = db.session.execute(db.select(User).where(User.username == username)).scalar()
    if not user:
        return jsonify({"error": "Username does not exist"}), 404
    
    user_auth = db.session.execute(db.select(UserAuth).where(UserAuth.user_id == user.id)).scalar()
    if not user_auth:
        return jsonify({"error": "Authentication Issue, please contact helpdesk@bookish.co.uk for further assistance."}), 404
    if not user_auth.check_password(password):
        return jsonify({"error": "Incorrect password"}), 401
    
    return {"status": "OK"}, 200

@blueprint.route('/register', methods=["POST"])
def register_user():
    request_body = request.get_json()
    if not request_body or not 'username' in request_body or not 'password' in request_body:
        return jsonify({"error": "Missing username or password"}), 400
    
    username = request_body['username']
    last_name
    password = request_body['password']
    
    user = User(username)
    db.session.add(user)
    db.session.commit()
    
    user_auth = UserAuth(user.id, password)
    db.session.add(user_auth)
    db.session.commit()
    
    return {"status": "OK"}, 200

