from functools import wraps
from flask import redirect

username = "Guest"


def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if username == None or username == "Guest":
            return redirect('/login', code=302)
        return f(*args, **kwargs)

    return decorated_function
