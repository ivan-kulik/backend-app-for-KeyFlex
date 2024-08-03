from fastapi import APIRouter

from core.config import settings
from .routers_helper import routers_helper
from core.schemas.user import UserRead, UserUpdate

router = APIRouter(
    prefix=settings.api.users,
    tags=["Users"],
)

# /me and /{id}
router.include_router(
    router=routers_helper.get_users_router(
        UserRead,
        UserUpdate,
    ),
)
