from fastapi_users import FastAPIUsers

from core.models import User
from core.types.user_id import UserIdType
from dependencies.authentication.user_manager import get_user_manager
from dependencies.authentication.backend import auth_backend


fastapi_users = FastAPIUsers[User, UserIdType](
    get_user_manager,
    [auth_backend],
)
