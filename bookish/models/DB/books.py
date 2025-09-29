from sqlalchemy import ForeignKey
from bookish.app import db


class Book(db.Model):
    # This sets the name of the table in the database
    __tablename__ = 'books'

    # Here we outline what columns we want in our database
    isbn = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    author_first_name = db.Column(db.String())
    author_last_name = db.Column(db.String())

    def __init__(self, title, author_first_name, author_last_name):
        self.title = title
        self.author_first_name = author_first_name
        self.author_last_name = author_last_name

    def __repr__(self):
        return '<isbn {}, title {}, author {} {}>'.format(self.isbn, self.title, self.author_first_name, self.author_last_name)

    def serialize(self):
        return {
            'isbn': self.isbn,
            'title': self.title,
            'author_first_name': self.author_first_name,
            'author_last_name': self.author_last_name
        }


class Copy(db.Model):
    # This sets the name of the table in the database
    __tablename__ = 'copies'

    # Here we outline what columns we want in our database
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.Integer, ForeignKey('books.isbn'), nullable=False)
    checked_out_to = db.Column(db.Integer(), ForeignKey('users.id'))
    due_date = db.Column(db.Date())

    def __init__(self, isbn):
        self.isbn = isbn

    def __repr__(self):
        if (self.checked_out_to):
            return '<id {}, isbn {}, checked out to {}, due date {}>'.format(self.id, self.isbn, self.checked_out_to, self.due_date)
        return '<id {}, isbn {}, >'.format(self.id, self.isbn)

    def serialize(self):
        return {
            'id': self.id,
            'isbn': self.isbn,
            'checked_out_to': self.checked_out_to,
            'due_date': self.due_date
        }
