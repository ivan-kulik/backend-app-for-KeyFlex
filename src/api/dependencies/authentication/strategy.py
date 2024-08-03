from fastapi_users.authentication import JWTStrategy

from core.config import settings


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.access_token.secret_key,
        lifetime_seconds=settings.access_token.lifetime_seconds,
    )
