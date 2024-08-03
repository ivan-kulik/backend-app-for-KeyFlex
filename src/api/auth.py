from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from api.dependencies.authentication.backend import auth_backend
from core.config import settings
from core.schemas.user import UserRead, UserCreate
from .routers_helper import routers_helper

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix=settings.api.auth,
    tags=["Auth"],
    dependencies=[Depends(http_bearer)],
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
