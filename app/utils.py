import os
import random
import shutil
import string
import subprocess

from settings import *

from .mailer import *

if DEBUG is False:
    from app.db import cursor

from app.decorator import *
from app.errors import *
from app.local_db import db_create_user, update_user

database_folder_list = [
    "DiversityAgents",
    "DiversityCollection",
    "DiversityDescriptions",
    "DiversityProjects",
    "DiversityReferences",
    "DiversitySamplingPlots",
    "DiversityScientificTerms",
    "DiversityTaxonNames",
]


@exception(FileError)
def copy_db_files(db_files_list, username):
    for folder in database_folder_list:
        files = os.listdir(DATABASE_FOLDER + folder)
        list_files = {}
        for f in files:
            if ".mdf" in f or ".MDF" in f:
                list_files["mdf"] = (
                    USERS_FOLDER + username + "/" + folder + "/" + f
                ).replace("/", "\\")
            if ".ldf" in f or ".LDF" in f:
                list_files["ldf"] = (
                    USERS_FOLDER + username + "/" + folder + "/" + f
                ).replace("/", "\\")
            list_files["db_name"] = folder
        db_files_list.append(list_files)


@exception(SqlErrorNewUserError)
def create_user(username, password):
    cursor.execute("CREATE LOGIN [" + username + "] WITH PASSWORD = '" + password + "'")
    cursor.execute("CREATE USER [" + username + "] FOR LOGIN [" + username + "]")


@exception(SqlErrorNewUserWinError)
def create_windows_user(username):
    try:
        cursor.execute("CREATE LOGIN [" + username + "] FROM WINDOWS")
        cursor.execute("CREATE USER [" + username + "] FOR LOGIN [" + username + "]")
    except Exception as e:
        print("type is:" + e.__class__.__name__)


def create_user_folder(username):
    os.path.join(USERS_FOLDER, username)
    try:
        shutil.copytree(DATABASE_FOLDER, USERS_FOLDER + username)
    except Exception:
        pass


@exception(PermissionFolderError)
def grant_permission_folder(username):
    args = ["icacls", USERS_FOLDER, "/grant:r", "Users:(OI)(CI)MF"]
    subprocess.check_call(args)


@exception(PasswordError)
def get_random_password_string(length):
    password_characters = string.ascii_letters + string.digits
    password = "".join(random.choice(password_characters) for i in range(length))
    return password


@exception(SqlErrorUploadDB)
def upload_db(db_files_list, username):
    for path in db_files_list:
        database_name = path["db_name"] + "_" + fix_username(username)
        sql1 = "CREATE DATABASE [" + database_name
        sql2 = "] ON (Filename = '{pathMDF}'), (Filename = '{pathLDF}')".format(
            pathMDF=path["mdf"], pathLDF=path["ldf"]
        )
        sql3 = " FOR Attach"
        sql = sql1 + sql2 + sql3
        cursor.execute(sql)


@exception(SqlErrorPermissionDB)
def grant_permission_db(username):
    for i in database_folder_list:
        sql1 = "use [" + i + "_" + fix_username(username) + "];"
        sql2 = "create user [" + username + "] from login [" + username + "];"
        sql3 = "exec sp_addrolemember 'db_owner', [" + username + "];"
        sql = sql1 + " " + sql2 + " " + sql3
        cursor.execute(sql)


@exception(SqlErrorProcedure)
def run_procedure(username):
    for i in database_folder_list:
        sql1 = "USE [" + i + "_" + fix_username(username) + "];"
        sql2 = "EXECUTE [dbo].[SetUserProjects] [" + username + "];"
        sql = sql1 + sql2
        cursor.execute(sql)


@exception(SqlErrorDropDatabase)
def delete_database(username):
    sql = "USE Master; DROP DATABASE  IF EXISTS "
    for db_name in database_folder_list:
        sql = sql + " [" + db_name + "_" + fix_username(username) + "],"
    sql = sql[:-1]
    sql = sql + " ;"
    cursor.execute(sql)
    sql = "Use Master; DROP login [" + username + "]"
    cursor.execute(sql)
    sql = "USE Master; DROP user [" + username + "]"
    cursor.execute(sql)


def is_user_exist(username):
    return os.path.isdir(USERS_FOLDER + username)


def remove_db_files(username):
    dir_path = USERS_FOLDER + username
    try:
        shutil.rmtree(dir_path)
    except Exception:
        pass


def fix_username(username):
    username = username.replace(".", "_", 1)
    username = username.replace(MAIN_DOMAIN_NAME, "")
    return username


def create_local_windows_user(username):
    run("New-LocalUser -Name " + username + " -Description -NoPassword")


def run(self, cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return completed


def create_db_process(username):
    try:
        db_create_user(username)
        db_files_list = []
        update_user(username, percentage=10)
        password = get_random_password_string(15)
        update_user(username, percentage=20)
        copy_db_files(db_files_list, username)
        update_user(username, percentage=30)
        create_user_folder(username)
        update_user(username, percentage=40)
        grant_permission_folder(username)
        update_user(username, percentage=50)
        upload_db(db_files_list, username)
        update_user(username, percentage=60)
        create_user(username, password)
        update_user(username, percentage=70)
        grant_permission_db(username)
        update_user(username, percentage=80)
        run_procedure(username)
        if WINDOWS_USER:
            create_local_windows_user(username)
        sendMail(
            MAIL_NOTIFY,
            data={"username": username, "password": password, "ip": IP},
            template_name="mail_to_user",
        )
        update_user(
            username,
            percentage=100,
            data={
                "password": password,
                "ip": IP,
                "databases": list(
                    map(
                        lambda x: x["db_name"] + "_" + fix_username(username),
                        db_files_list,
                    )
                ),
            },
        )
        return password
    except ValueError:
        update_user(username, error=str("SQL related error, couldn't create user"))
    except Exception as e:
        update_user(username, error=str(e.message))
