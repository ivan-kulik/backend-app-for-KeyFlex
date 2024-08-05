from fastapi_users.exceptions import FastAPIUsersException


class UserNameAlreadyExists(FastAPIUsersException):
    pass


class UserEmailAlreadyExists(FastAPIUsersException):
    pass
