from fastapi import APIRouter

from api.dependencies.authentication.backend import auth_backend
from core.config import settings
from core.schemas.user import UserRead, UserCreate
from .routers_helper import routers_helper


router = APIRouter(
    prefix=settings.api.auth,
    tags=["Auth"],
)


router.include_router(
    router=routers_helper.get_auth_router(
        backend=auth_backend,
    ),
    prefix="/jwt",
)

router.include_router(
    router=routers_helper.get_register_router(
        user_schema=UserRead,
        user_create_schema=UserCreate,
    ),
)
