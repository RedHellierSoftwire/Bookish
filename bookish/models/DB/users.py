from bookish.app import db
from sqlalchemy import ForeignKey
import bcrypt

class User(db.Model):
    # This sets the name of the table in the database
    __tablename__ = 'users'

    # Here we outline what columns we want in our database
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<id {}, username {}>'.format(self.id, self.username)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username
        }

class UserAuth(db.Model):
    __tablename__ = 'user_auth'

    user_id = db.Column(db.Integer, ForeignKey('users.id'), primary_key=True)
    password = db.Column(db.String(), nullable=False)
    salt = db.Column(db.String(), nullable=False)

    def __init__(self, user_id, password):
        self.user_id = user_id
        encoded_password = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(encoded_password, salt)
        self.password = hashed_password
        self.salt = salt
    
    def serialize(self):
        return {
            'user_id': self.user_id,
            'password': self.password,
            'salt': self.salt
        }
    
    def check_password(self, password_to_check):
        encoded_password_to_check = password_to_check.encode('utf-8')
        hashed_password_to_check = bcrypt.hashpw(encoded_password_to_check, self.salt)
        return bcrypt.checkpw(hashed_password_to_check, self.password)