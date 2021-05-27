from flask import json, jsonify, session, redirect, url_for
from werkzeug.exceptions import HTTPException

from server import app, request, render_template
from settings import *

from .auth import *
from .decorator import *
from .errors import *
from .job import get_result
from .local_db import delete_user, user_exist, get_user_list
from .mailer import *
from .response import *
from .utils import *


@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps(
        {
            "message": "Method not allowed or endpoint does not exist",
            "status": "error",
            "data": [],
        }
    )
    response.content_type = "application/json"
    return response

@app.route("/")
def index():
    if "token" in request.cookies and auth(request.cookies.get('token')):
            return redirect(url_for("admin"))
    return render_template('login.html')

@app.route("/admin")
def admin():
    if "token" not in request.cookies or not auth(request.cookies.get('token')):
        return redirect("/")           
    return render_template('admin_new.html')


@app.route("/token" , methods=["POST"])
def token():
    return auth_user()

@app.route("/user_list")
@token_required
def user_list():
    return ApiResponse(data=get_user_list())

@app.route("/check_user_exist", methods=["POST"])
@token_required
@check_username
def check_user_exist():
    username = request.form["username"]
    if user_exist(username):
        return UserExistResponse()
    else:
        raise UserNotExist


@app.route("/delete_db", methods=["POST"])
@token_required
@check_username
def delete_db():
    username = request.form["username"]
    delete_database(username)
    delete_database(MAIN_DOMAIN_NAME + username)
    remove_db_files(username)
    delete_user(username)
    return DeleteUserResponse()


@app.route("/create_db", methods=["POST"])
@token_required
@check_username
def create_db():
    username = request.form["username"]
    try:
        data = get_result(username)
    except:
        return jsonify(
            {
                "message": "User couldn't create, delete user, and resent it",
                "status": "error",
                "data": [],
            }
        )
    if data["state"] == "finished":
        return UserExistResponse()
    # sendMail(MAIL_ADMINISTRATOR, " please move that user to the gwdg_RDS_GFBIO", subject= MAIL_ADMINISTRATOR_SUBJECT)
    return CreateUserResponse(data=data)
