from fastapi import APIRouter

from api.dependencies.authentication.backend import auth_backend
from core.config import settings
from core.schemas.user import UserRead, UserCreate
from .routers_helper import routers_helper, google_oauth_client


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

router.include_router(
    router=routers_helper.get_oauth_router(
        google_oauth_client,
        auth_backend,
        settings.access_token.secret_key,
    ),
    prefix="/google",
    # tags=["Auth-With-Google"],
)

# /request-verify-token
# /verify
router.include_router(
    router=routers_helper.get_verify_router(UserRead),
)
