import datetime
from functools import wraps

import jwt
from server import request
from settings import DATABASE_FILENAME, EXPIRE_MINUTE, SECRET_ID, SECRET_KEY
from tinydb import TinyDB

from .errors import CredentialMissing, TokenMissing, Unauthorized
from .response import TokenResponse

db = TinyDB(DATABASE_FILENAME)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if "token" in request.headers:
            token = request.headers["token"]
        if not token:
            raise TokenMissing
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except Exception:
            raise Unauthorized
        return f(*args, **kwargs)

    return decorator

def auth(token):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return True
    except Exception:
        return False


def auth_user():
    try:
        requested_secret_key = request.form["secret_key"]
        requested_secret_id = request.form["secret_id"]
    except Exception:
        raise CredentialMissing
    exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=int(EXPIRE_MINUTE))
    if requested_secret_id == SECRET_ID and requested_secret_key == SECRET_KEY:
        token = jwt.encode({"data": SECRET_ID, "exp": exp}, SECRET_KEY)
        data = {"token": token, "exp": exp}
        return TokenResponse(data=data)
    raise Unauthorized
