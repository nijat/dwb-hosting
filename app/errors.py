class ApiBaseError(Exception):
    http_code = 400
    message = "Internal Server error"

    def to_dict(self):
        return {"message": self.message, "status": "error", "data": []}


class UsernameNotFound(ApiBaseError):
    message = "Username not found in request"


class UserNotExist(ApiBaseError):
    message = "User does not exist in the server"


class UsernameNotCorrectError(ApiBaseError):
    message = "Username is not correct"


class Unauthorized(ApiBaseError):
    http_code = 401
    message = "The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required"


class SqlErrorNewUserError(Exception):
    message = "Couldn't create new user in the SQL Server"


class FileError(Exception):
    message = "Couldn't copy files of user"


class PermissionFolderError(Exception):
    message = "Cannot grant permission for folder"


class PasswordError(Exception):
    message = "Couldn't create new password for user"


class RemoveFolderError(ApiBaseError):
    message = "User's folder couldn't removed"


class SqlErrorDropDatabase(ApiBaseError):
    message = "Couldn't drop user's database in the SQL Server"


class SqlErrorProcedure(Exception):
    message = "Couldn't run SetUserProjects procedure"


class SqlErrorPermissionDB(Exception):
    message = "Couldn't grant the permission to the user in SQL Server"


class SqlErrorUploadDB(Exception):
    message = "Couldn't upload mdf files to the SQL Server"


class SqlErrorNewUserWinError(Exception):
    message = "Couldn't create new windows user in the SQL Server"


class TokenMissing(ApiBaseError):
    http_code = 401
    message = "Token is missing"


class CredentialMissing(ApiBaseError):
    http_code = 404
    message = "Credentials are missing (secret_key, secret_id)"


class InvalidToken(ApiBaseError):
    http_code = 401
    message = "Invalid Token"
