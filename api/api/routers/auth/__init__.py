"""
authswitch - Authentication Module
Generado automáticamente por tai-api auth init
"""
from fastapi import APIRouter
from .dependencies import requires_permissions, requires_permissions_from_realm, CurrentUser, get_current_user
from .login_router import router as l_router
from .jwt import AccessToken
from .rbac_router import router as r_router
from .docs_router import router as d_router

auth_router = APIRouter()
auth_router.include_router(l_router)
auth_router.include_router(r_router)
auth_router.include_router(d_router)

__all__ = [
    "requires_permissions",
    "requires_permissions_from_realm",
    "auth_router",
    "CurrentUser",
    "get_current_user",
]