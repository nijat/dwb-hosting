from flask import Flask, request, render_template, jsonify
from flask_restful import Api, marshal
from flask_cors import CORS
from settings import *
from waitress import serve
import time
import threading

app = Flask(__name__, template_folder='templates')
api = Api(app)
CORS(app)

from app.view import *
from app.errors import *
from app.find_users import *
from app.local_db import *

def check_new_user():
    while True:
        main()
        time.sleep(TIME_TO_CHECK_DOMAIN)


if __name__ == "__main__":

    @app.errorhandler(ApiBaseError)
    @app.errorhandler(UsernameNotFound)
    @app.errorhandler(UserNotExist)
    @app.errorhandler(Unauthorized)
    @app.errorhandler(SqlErrorNewUserError)
    @app.errorhandler(FileError)
    @app.errorhandler(PermissionFolderError)
    @app.errorhandler(PasswordError)
    @app.errorhandler(RemoveFolderError)
    @app.errorhandler(SqlErrorDropDatabase)
    @app.errorhandler(SqlErrorPermissionDB)
    @app.errorhandler(SqlErrorUploadDB)
    @app.errorhandler(CredentialMissing)
    def handle_error(error):
        return error.to_dict(), getattr(error, "http_code")
    
    add_exist_users_to_db()
    x = threading.Thread(target=check_new_user)
    x.start()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    serve(app, host=IP, port=PORT, threads=2)
