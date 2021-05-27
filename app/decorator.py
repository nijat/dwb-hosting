import re
from functools import wraps

from server import request

from app.errors import UsernameNotCorrectError, UsernameNotFound


def check_username(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        username = request.form["username"]
        if username is None:
            raise UsernameNotFound
        pattern = re.compile("^[a-zA-Z]([._-]?[a-zA-Z0-9]+)*$")
        if not pattern.search(username):
            raise UsernameNotCorrectError
        if len(username) < 3 or len(username) > 30:
            raise UsernameNotCorrectError
        username
        return f(*args, **kwargs)

    return decorated_function


def exception(Exceptions):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                raise Exceptions
            raise Exceptions

        return wrapper

    return decorator
