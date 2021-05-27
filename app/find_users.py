import csv
import subprocess
import sys

from tinydb import Query, TinyDB

from app.mailer import *
from app.utils import *
from settings import *

db = TinyDB(DATABASE_FILENAME)


def callPowershellCommandToGetUser():
    p = subprocess.Popen(
        [
            "powershell.exe",
            "C:\WebServer\dwb-hosting-concept\scripts\get_new_users.ps1",
        ],
        stdout=sys.stdout,
    )
    p.communicate()


def getNewUserOfDomain():
    User = Query()
    isfirstTimeLoadToDb = len(db) == 0
    with open("domain_users.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            isUserExist = len(db.search(User.name == row["Name"])) != 0
            if not isUserExist:
                db.insert({"name": row["Name"], "mail": row["UserPrincipalName"]})
                if not isfirstTimeLoadToDb:
                    return row["Name"], row["UserPrincipalName"]


def main():
    if DEBUG is False:
        callPowershellCommandToGetUser()
    user = getNewUserOfDomain()
    if user is not None:
        username = MAIN_DOMAIN_NAME + str(user[0])
        print(username)
        if not is_user_exist(user[0]):
            print("1")
            result = create_db_process(user[0])
        print("2")
        create_windows_user(username)
        print("3")
        grant_permission_db(username)
        print("4")
        run_procedure(username)
        print("5")
        sendMail(
            user[1],
            data={"username": username, "password": result[0], "ip": IP},
            template_name="mail_to_user",
        )
