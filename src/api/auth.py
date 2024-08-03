from fastapi import APIRouter

from api.dependencies.authentication.backend import auth_backend
from core.config import settings
from core.schemas.user import UserRead, UserCreate
from .routers_helper import routers_helper

router = APIRouter(
    prefix=settings.api.auth,
    tags=["Auth"],
)

# /login and /logout
router.include_router(
    router=routers_helper.get_auth_router(
        auth_backend,
    ),
    prefix="/jwt",
)

# /register
router.include_router(
    router=routers_helper.get_register_router(
        UserRead,
        UserCreate,
    ),
)
