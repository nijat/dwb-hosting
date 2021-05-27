import pyodbc as db
from settings import DB_DATABASE, DB_DRIVER, DB_PASSWORD, DB_SERVER, DB_USERNAME

connectionstring = f"DRIVER={DB_DRIVER};SERVER={DB_SERVER};UID={DB_USERNAME};PWD={DB_PASSWORD};DATABASE={DB_DATABASE};Trusted_Connection=yes;"

connection = db.connect(connectionstring)
connection.autocommit = True

cursor = connection.cursor()
