from typing import Annotated

from fastapi import APIRouter, status, Depends

from api.dependencies.stats_service import get_modes_stats_service
from core.config import settings
from core.models import User
from core.schemas.stats import (
    AddStatisticsData,
    GetModesStatsData,
    GetLastSessionsStatsData,
)
from core.services.stats import ModesStatsService
from .routers_helper import routers_helper


router = APIRouter(
    prefix=settings.api.stats,
    tags=["Statistics"],
)

current_active_verified_user = routers_helper.current_user(
    active=True,
    # verified=True,
)


@router.post("/add_stats", status_code=status.HTTP_201_CREATED)
async def add_statistics(
    user: Annotated[User, Depends(current_active_verified_user)],
    add_statistics_data: AddStatisticsData,
    modes_stats_service: Annotated[
        ModesStatsService,
        Depends(get_modes_stats_service),
    ],
):
    await modes_stats_service.add_stats_data(
        add_statistics_data,
        user,
    )


@router.get(
    "/get_modes_stats_data",
    status_code=status.HTTP_200_OK,
    response_model=GetModesStatsData,
)
async def get_modes_stats_data(
    user: Annotated[User, Depends(current_active_verified_user)],
    modes_stats_service: Annotated[
        ModesStatsService,
        Depends(get_modes_stats_service),
    ],
):
    modes_stats_data = await modes_stats_service.get_modes_stats_data(
        cur_user=user,
    )
    return modes_stats_data


@router.get(
    "/get_last_sessions_stats",
    status_code=status.HTTP_200_OK,
    response_model=GetLastSessionsStatsData,
)
async def get_last_sessions_stats(
    user: Annotated[User, Depends(current_active_verified_user)],
    modes_stats_service: Annotated[
        ModesStatsService,
        Depends(get_modes_stats_service),
    ],
):
    last_sessions_stats_data = await modes_stats_service.get_last_sessions_stats_data(
        cur_user=user,
    )
    return last_sessions_stats_data
