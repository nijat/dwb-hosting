from tinydb import Query, TinyDB
from tinydb.operations import delete
import os
from settings import USERS_DATABASE_FILENAME, USERS_FOLDER

db = TinyDB(USERS_DATABASE_FILENAME)
Users = Query()


def add_exist_users_to_db():
    listOfExistUsers = [x[1] for x in os.walk(USERS_FOLDER)][0]
    for username in listOfExistUsers:
        if not db.contains(Users.username == username):
            db.insert(
                {
                    "username": username,
                    "state": "finished",
                    "percentage": 100,
                    "error": "",
                }
            )


def db_create_user(username):
    if not db.contains(Users.username == username):
        db.insert(
            {"username": username, "state": "started", "percentage": 0, "error": ""}
        )


def user_exist(username):
    return db.contains(Users.username == username)


def delete_user(username):
    db.remove(Users.username == username)


def get_user(username):
    return db.search(Users.username == username)[0]

def get_user_list():
    return db.all()

def update_user(username, percentage=0, error=None, state="stopped", data=None):
    try:
        if percentage > 0 and percentage < 100 and error is None:
            state = "processing"
        if percentage == 0 and error is None:
            state = "started"
        if percentage == 100 and error is None:
            state = "completed"
        if error:
            state = "stopped"
        if not error:
            error = ""
        if data is None:
            db.upsert(
                {
                    "username": username,
                    "state": state,
                    "percentage": percentage,
                    "error": error,
                },
                Users.username == username,
            )
        else:
            db.upsert(
                {
                    "username": username,
                    "state": state,
                    "percentage": percentage,
                    "error": error,
                    "user_information": data,
                },
                Users.username == username,
            )
    except:
        pass
