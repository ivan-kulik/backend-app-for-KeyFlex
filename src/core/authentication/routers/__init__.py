__all__ = (
    "get_auth_router",
    "get_register_router",
    "get_verify_router",
)

from .auth import get_auth_router
from .register import get_register_router
from .verify import get_verify_router
