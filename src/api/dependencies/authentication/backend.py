from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy

from .strategy import get_jwt_strategy
from core.authentication.transport import bearer_transport


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
