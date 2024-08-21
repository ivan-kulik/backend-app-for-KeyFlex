from typing import Type

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi_users import exceptions, models, schemas
from fastapi_users.manager import BaseUserManager, UserManagerDependency
from fastapi_users.router.common import ErrorModel

from core.authentication.auth_errors import ErrorCode
from core.authentication.auth_exceptions import (
    UserNameAlreadyExists,
    UserEmailAlreadyExists,
)
from api.dependencies.stats_service import get_modes_stats_service
from api.dependencies.profile_service import get_profile_service
from core.services.stats import ModesStatsService
from core.services.profile import ProfileService


def get_register_router(
    get_user_manager: UserManagerDependency[models.UP, models.ID],
    user_schema: Type[schemas.U],
    user_create_schema: Type[schemas.UC],
) -> APIRouter:
    """Generate a router with the register route."""
    router = APIRouter()

    @router.post(
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
                            ErrorCode.REGISTER_USER_EMAIL_ALREADY_EXISTS: {
                                "summary": "A user with this email already exists.",
                                "value": {
                                    "detail": ErrorCode.REGISTER_USER_EMAIL_ALREADY_EXISTS
                                },
                            },
                            ErrorCode.REGISTER_USER_NAME_ALREADY_EXISTS: {
                                "summary": "A user with this name already exists.",
                                "value": {
                                    "detail": ErrorCode.REGISTER_USER_NAME_ALREADY_EXISTS
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
        modes_stats_service: ModesStatsService = Depends(get_modes_stats_service),
        profile_service: ProfileService = Depends(get_profile_service),
    ):
        try:
            created_user = await user_manager.create(
                user_create, safe=True, request=request
            )
            await modes_stats_service.create_stats_data_row(created_user.username)
            await profile_service.create_profile(created_user.username)
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

    return router
