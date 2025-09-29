from flask import jsonify, request
from bookish.models.DB.users import User, UserAuth
from bookish.models import db

def user_routes(app):
    @app.route('/users', methods=['GET'])
    def get_users():
        users = db.session.execute(db.select(User).order_by(User.first_name)).scalars().all()
        userResults = [user.serialize() for user in users]
        return {"users": userResults}

    @app.route('/users/authenticate', methods=["POST"])
    def authenticate_user():
        request_body = request.form
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

    @app.route('/users/register', methods=["POST"])
    def register_user():
        print("registering User")
        request_body = request.form
        print("registering User json")
        if not request_body or not 'username' in request_body or not 'password' in request_body:
            return jsonify({"error": "Missing username or password"}), 400
        
        username = request_body['username']
        password = request_body['password']

        user = User(username)
        db.session.add(user)
        db.session.commit()
        
        user_auth = UserAuth(user.id, password)
        db.session.add(user_auth)
        db.session.commit()

        print(username)
        
        return jsonify({"status": "OK"}), 200

