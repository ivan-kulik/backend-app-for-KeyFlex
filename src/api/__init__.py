from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from core.config import settings
from .auth import router as auth_router
from .users import router as users_router
from .stats import router as stats_router
from .profiles import router as profile_router

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix=settings.api.prefix,
    dependencies=[Depends(http_bearer)],
)

router.include_router(auth_router)
router.include_router(users_router)
router.include_router(stats_router)
router.include_router(profile_router)
