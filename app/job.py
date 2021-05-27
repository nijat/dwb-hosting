import time
from threading import Thread, get_ident, enumerate
from .local_db import user_exist, delete_user, get_user, update_user, db_create_user
from .utils import create_db_process


def run_job(user):
    workThread = Thread(target=create_db_process, args=(user,))
    workThread.start()


def get_result(user):
    if not user_exist(user):
        db_create_user(user)
        run_job(user)
    response = get_user(user)
    return response
