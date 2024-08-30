import logging
from typing import Optional

from fastapi import Request
from fastapi_users import (
    BaseUserManager,
    IntegerIDMixin,
    exceptions,
    models,
    schemas,
)
from fastapi_users.jwt import decode_jwt
import jwt

from core.config import settings
from core.models import User
from core.types.user_id import UserIdType

from core.authentication.auth_exceptions import (
    UserNameAlreadyExists,
    UserEmailAlreadyExists,
)
from core.authentication.security import OAuth2PasswordRequestForm


log = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, UserIdType]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user_by_username = await self.user_db.get_by_username(
            user_create.username
        )
        if existing_user_by_username is not None:
            raise UserNameAlreadyExists()

        existing_user_by_email = await self.user_db.get_by_email(user_create.email)
        if existing_user_by_email is not None:
            raise UserEmailAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user

    async def authenticate(
        self,
        credentials: OAuth2PasswordRequestForm,
    ) -> Optional[models.UP]:
        try:
            if credentials.username:
                user = await self.user_db.get_by_username(credentials.username)
            else:
                user = await self.user_db.get_by_email(credentials.email)

        except exceptions.UserNotExists:
            self.password_helper.hash(credentials.password)
            return None

        verified, updated_password_hash = self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        if not verified:
            return None

        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})

        return user

    async def on_after_register(
        self,
        user: User,
        request: Optional[Request] = None,
    ):
        log.warning(
            "User %r has registered.",
            user.id,
        )

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Optional[Request] = None,
    ):
        log.warning(
            "User %r has forgot their password. Reset token: %r",
            user.id,
            token,
        )

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Optional[Request] = None,
    ):
        log.warning(
            "Verification requested for user %r. Verification token: %r",
            user.id,
            token,
        )
