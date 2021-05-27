class ApiResponse:
    http_code = 200
    message = "Successful response"

    def __new__(self, data={}):
        return {"message": self.message, "status": "success", "data": data}


class CreateUserResponse(ApiResponse):
    message = ""


class UserExistResponse(ApiResponse):
    message = "User exists in the server"


class DeleteUserResponse(ApiResponse):
    message = "User and DB deleted"


class TokenResponse(ApiResponse):
    message = "Token generated"
