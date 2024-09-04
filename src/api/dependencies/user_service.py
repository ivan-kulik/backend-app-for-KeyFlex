from core.repositories import UserRepo
from core.services import UserService


def get_user_service():
    return UserService(UserRepo)
