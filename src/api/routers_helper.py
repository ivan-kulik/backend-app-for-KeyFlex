from typing import Type

from fastapi import APIRouter
from fastapi_users import FastAPIUsers, schemas
from fastapi_users.authentication import AuthenticationBackend
from httpx_oauth.clients.google import GoogleOAuth2

from core.models import User
from core.authentication.routers import (
    get_register_router,
    get_auth_router,
    get_verify_router,
)
from core.types.user_id import UserIdType
from api.dependencies.authentication.user_manager import get_user_manager
from api.dependencies.authentication.backend import auth_backend
from core.config import settings


google_oauth_client = GoogleOAuth2(
    settings.google_oauth2.GOOGLE_OAUTH_CLIENT_ID,
    settings.google_oauth2.GOOGLE_OAUTH_CLIENT_SECRET,
)


class CustomFastAPIUsers(FastAPIUsers[User, UserIdType]):
    def get_register_router(
        self, user_schema: Type[schemas.U], user_create_schema: Type[schemas.UC]
    ) -> APIRouter:
        return get_register_router(
            self.get_user_manager, user_schema, user_create_schema
        )

    def get_auth_router(
        self, backend: AuthenticationBackend, requires_verification: bool = False
    ) -> APIRouter:
        return get_auth_router(
            backend,
            self.get_user_manager,
            self.authenticator,
            requires_verification,
        )

    def get_verify_router(self, user_schema: Type[schemas.U]) -> APIRouter:
        return get_verify_router(
            get_user_manager=self.get_user_manager,
            user_schema=user_schema,
        )


routers_helper = CustomFastAPIUsers(
    get_user_manager,
    [auth_backend],
)
