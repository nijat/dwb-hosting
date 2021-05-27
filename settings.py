from os import environ, path,getenv
from dotenv import load_dotenv


load_dotenv(".env")
DEBUG = getenv("DEBUG", 'False').lower() in ('true', '1', 't')
WINDOWS_USER = getenv("WINDOWS_USER", 'False').lower() in ('true', '1', 't')
print("Debug mode is "+str(DEBUG))

if DEBUG is False:
    DB_DRIVER = "{SQL Server}"
else:
    DB_DRIVER = "FreeTDS"
    
IP = environ.get("IP")
PORT = environ.get("PORT")

SECRET_ID = environ.get("SECRET_ID")
SECRET_KEY = environ.get("SECRET_KEY")
EXPIRE_MINUTE = environ.get("EXPIRE_MINUTE", 60)

DB_SERVER = environ.get("DB_SERVER")
DB_DATABASE = environ.get("DB_DATABASE")
DB_USERNAME = environ.get("DB_USERNAME")
DB_PASSWORD = environ.get("DB_PASSWORD")
DB_PORT = environ.get("DB_PORT")



MAIN_FOLDER = str(environ.get("MAIN_FOLDER"))
DATABASE_FOLDER_NAME = environ.get("DATABASE_FOLDER_NAME")
DATABASE_FOLDER = str(MAIN_FOLDER) + str(DATABASE_FOLDER_NAME) + "/"
USERS_FOLDER = MAIN_FOLDER + "users/"
PS_GET_NEW_USER_URL = MAIN_FOLDER + "scripts/get_new_users.ps1"
DATABASE_FILENAME = "db.json"
USERS_DATABASE_FILENAME = "users.json"

MAIL_SEND = True
MAIL_USERNAME = environ.get("MAIL_USERNAME")
MAIL_PASSWORD = environ.get("MAIL_PASSWORD")
MAIL_SMTP = environ.get("MAIL_SMTP")
MAIL_PORT = environ.get("MAIL_PORT")
MAIL_FROM = environ.get("MAIL_FROM")
MAIL_SUBJECT = environ.get("MAIL_SUBJECT")

MAIL_ADMINISTRATOR = environ.get("MAIL_ADMINISTRATOR")
MAIL_ADMINISTRATOR_SUBJECT = environ.get("MAIL_ADMINISTRATOR_SUBJECT")

MAIL_NOTIFY = environ.get("MAIL_NOTIFY")

TIME_TO_CHECK_DOMAIN = 30
MAIN_DOMAIN_NAME = "DOMAIN_NAME"+ chr(92)
