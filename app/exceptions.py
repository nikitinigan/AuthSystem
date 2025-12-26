from fastapi import HTTPException

class UsersException(HTTPException):
    status_code : int = 500
    detail: str  = ""
    
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class NotFoundException(UsersException):
    status_code = 404
    detail = "No data found"
    
class IncorrectEmailOrPasswordException(UsersException):
    status_code = 401
    detail = "Incorrect email or password"

class ForbiddenRoleException(UsersException):
    status_code = 403
    detail = "Forbidden: insufficient role"

class TokenAbsentException(UsersException):
    status_code = 401
    detail = "Token is absent"

class TokenExpiredException(UsersException):
    status_code = 401
    detail = "Token expired"

class IncorrectTokenFormatException(UsersException):
    status_code = 401
    detail = "Incorrect token format"

class UserIsNotPresentException(UsersException):
    status_code = 401
    detail = "User is not present"

class UserAlreadyExistsException(UsersException):
    status_code = 409
    detail = "User already exists"

class IncorrectEmailOrPasswordException(UsersException):
    status_code = 401
    detail = "Incorrect email or password"

class PasswordsDoNotMatchException(UsersException):
    status_code = 400
    detail = "Passwords do not match"

class PasswordTooShortException(UsersException):
    status_code = 400
    detail = "Password is too short. Minimum length is 6 characters"

class NoDataToUpdateException(UsersException):
    status_code = 400
    detail = "No data provided for update"

class MockException(HTTPException):
    status_code = 500
    detail = ""
    
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class ProjectNotFoundException(MockException):
    status_code = 404
    detail = "Project not found"

class ProjectAccessDeniedException(MockException):
    status_code = 403
    detail = "Access to project denied"

class CannotDeleteProjectException(MockException):
    status_code = 403
    detail = "Only admin can delete projects"