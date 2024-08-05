from typing import Type
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi_users import exceptions, models, schemas
from fastapi_users.manager import BaseUserManager, UserManagerDependency
from fastapi_users.router.common import ErrorModel
from fastapi.security import HTTPBearer

from api.dependencies.authentication.backend import auth_backend
from api.dependencies.authentication.user_manager import get_user_manager
from core.config import settings
from core.schemas.user import UserRead, UserCreate
from core.exceptions.user import (
    UserNameAlreadyExists,
    UserEmailAlreadyExists,
)
from core.errors.user import ErrorCode
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


def get_register_router(
    get_user_manager: UserManagerDependency[models.UP, models.ID],
    user_schema: Type[schemas.U],
    user_create_schema: Type[schemas.UC],
) -> APIRouter:
    register_router = APIRouter()

    @register_router.post(
        "/register",
        response_model=user_schema,
        status_code=status.HTTP_201_CREATED,
        name="register:register",
        responses={
            status.HTTP_400_BAD_REQUEST: {
                "model": ErrorModel,
                "content": {
                    "application/json": {
                        "examples": {
                            ErrorCode.REGISTER_USER_NAME_ALREADY_EXISTS: {
                                "summary": "A user with this name already exists.",
                                "value": {
                                    "detail": ErrorCode.REGISTER_USER_NAME_ALREADY_EXISTS
                                },
                            },
                            ErrorCode.REGISTER_USER_EMAIL_ALREADY_EXISTS: {
                                "summary": "A user with this email already exists.",
                                "value": {
                                    "detail": ErrorCode.REGISTER_USER_EMAIL_ALREADY_EXISTS
                                },
                            },
                            ErrorCode.REGISTER_INVALID_PASSWORD: {
                                "summary": "Password validation failed.",
                                "value": {
                                    "detail": {
                                        "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                                        "reason": "Password should be"
                                        "at least 3 characters",
                                    }
                                },
                            },
                        }
                    }
                },
            },
        },
    )
    async def register(
        request: Request,
        user_create: user_create_schema,
        user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
    ):
        try:
            created_user = await user_manager.create(
                user_create, safe=True, request=request
            )
        except UserNameAlreadyExists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.REGISTER_USER_NAME_ALREADY_EXISTS,
            )
        except UserEmailAlreadyExists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.REGISTER_USER_EMAIL_ALREADY_EXISTS,
            )
        except exceptions.InvalidPasswordException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                    "reason": e.reason,
                },
            )

        return schemas.model_validate(user_schema, created_user)

    return register_router


# /register
router.include_router(
    router=get_register_router(
        get_user_manager=get_user_manager,
        user_schema=UserRead,
        user_create_schema=UserCreate,
    ),
)
