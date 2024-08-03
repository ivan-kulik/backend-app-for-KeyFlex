from fastapi import APIRouter

from core.config import settings
from .routers_helper import routers_helper
from api.dependencies.authentication.backend import auth_backend


router = APIRouter(
    prefix=settings.api.auth,
    tags=["Auth"],
)

router.include_router(
    router=routers_helper.get_auth_router(auth_backend),
    prefix="/jwt",
)
