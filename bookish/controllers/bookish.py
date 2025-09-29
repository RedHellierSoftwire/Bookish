from flask import request
from bookish.models.DB.books import Book, Copy
from bookish.models.DB.users import User
from bookish.models import db


def bookish_routes(app):
    @app.route('/healthcheck')
    def health_check():
        return {"status": "OK"}

    @app.route('/books')
    def handle_books():
        books = Book.query.all()
        bookResults = [book.serialize() for book in books]
        return {"books": bookResults}

    @app.route('/copies')
    def handle_copies():
        copies = Copy.query.all()
        copyResults = [copy.serialize() for copy in copies]
        return {"copies": copyResults}

    @app.route('/users')
    def handle_users():
        users = User.query.all()
        userResults = [user.serialize() for user in users]
        return {"users": userResults}
