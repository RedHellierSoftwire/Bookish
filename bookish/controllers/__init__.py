from bookish.controllers.user import user_routes
from bookish.controllers.bookish import bookish_routes


def register_controllers(app):
    bookish_routes(app)
    user_routes(app)
