# DWB SaaS Service

## Description
This repository is used to maintain the different scripts and code used for the DWB hosting concept

## Installation
Clone the repository to the windows server, then run command below to install libraries
```bash
python -m pip install -r requirements.txt
```

Change environment (**.env**) file
```bash
DEBUG=True
IP=134.76.8.142
PORT=5000
DB_SERVER=""
DB_DATABASE="master"
DB_USERNAME=""
DB_PASSWORD=""
DB_PORT=1433
MAIN_FOLDER=""
TOKEN=""

SECRET_ID=""
SECRET_KEY=""
EXPIRE_MINUTE=60

DATABASE_FOLDER_NAME="database"


MAIL_USERNAME = ""
MAIL_PASSWORD = ""
MAIL_SMTP = ""
MAIL_PORT = 587
MAIL_FROM = ""
MAIL_SUBJECT = "Account Created"

MAIL_ADMINISTRATOR = ""
MAIL_ADMINISTRATOR_SUBJECT = ""
```

Run script for testing purposes
```bash
python server.py
```

## Windows HowTos

* Microsoft SQL Server Management Studio
    * Used for looking at the DBs and tables
    * Data Base were on "Pending Recovery"-Mode
        * delete obsolete DBs and restarted SQL Server

## API
Check API is working or not 
```bash
curl --location --request GET 'http://0.0.0.0:5000/'
```
 Request to get TOKEN
```bash
curl --location --request POST 'http://0.0.0.0:5000/token' --form 'secret_id=""' --form 'secret_key=""'
```

 Create new user with DB (SQL Authentication)
```bash
curl --location --header "token:" --request POST 'http://0.0.0.0:5000/create_db' --form 'username=username'
```
Delete user and DBs
```bash
curl --location --header "token:" --request POST 'http://0.0.0.0:5000/delete_db' --form 'username=username'
```
Check user exist or not
```bash
curl --location --header "token:" --request POST 'http://0.0.0.0:5000/check_user_exist' --form 'username=username'
```

## Connect to Database
* **Username** and **Password** given from API
* Server/IP: **0.0.0.0**
* PORT: **1433**