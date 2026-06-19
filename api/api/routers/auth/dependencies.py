"""
authswitch - Authentication Dependencies
Generado automáticamente por tai-api auth init
"""
from __future__ import annotations
import os
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated, Literal, Callable
from datetime import datetime, timezone

from .jwt import JWTHandler, AccessToken
from .database import AuthAsyncAPI, UserRead
from api.resources import (
    UnAuthorizedException,
    SessionInvalidatedException,
    RecordNotFoundException,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/docslogin")

auth_api = AuthAsyncAPI()


def requires_permissions(
    action: Literal["admin", "read", "write", "update", "delete"],
    resource: str,
) -> Callable:
    def fake_permission_dependency() -> AccessToken:
        return AccessToken(
            username="anonymous",
            exp=datetime.now(timezone.utc),
            permissions=["sudo"],
        )

    def permission_dependency(
        token: Annotated[str, Depends(oauth2_scheme)],
    ) -> AccessToken:
        payload = JWTHandler.decode_token(token, "access")

        if "sudo" in payload.api_roles or f"{resource}-admin" in payload.api_roles or f"allresources-{action}" in payload.api_roles:
            return payload

        required_perm = f"{resource}-{action}"

        if required_perm not in payload.api_roles:
            raise UnAuthorizedException(
                "Permisos insuficientes",
                details={
                    "required_permission": required_perm,
                    "user_permissions": payload.api_roles,
                },
            )

        return payload

    if not os.getenv("RBAC_ENABLED", "false").lower() == "true":
        return fake_permission_dependency

    return permission_dependency


def requires_permissions_from_realm(
    action: Literal["admin", "read", "write", "update", "delete"],
) -> Callable:
    def fake_permission_dependency() -> AccessToken:
        return AccessToken(
            username="anonymous",
            exp=datetime.now(timezone.utc),
            permissions=["sudo"],
        )

    def permission_dependency(
        realm_name: str,
        token: Annotated[str, Depends(oauth2_scheme)],
    ) -> AccessToken:
        payload = JWTHandler.decode_token(token, "access")

        if "sudo" in payload.api_roles or f"{realm_name}-admin" in payload.api_roles or f"allrealms-{action}" in payload.api_roles:
            return payload

        required_perm = f"{realm_name}-{action}"

        if required_perm not in payload.api_roles:
            raise UnAuthorizedException(
                "Permisos insuficientes",
                details={
                    "required_permission": required_perm,
                    "user_permissions": payload.api_roles,
                },
            )

        return payload

    if not os.getenv("RBAC_ENABLED", "false").lower() == "true":
        return fake_permission_dependency

    return permission_dependency


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserRead:
    payload: AccessToken = JWTHandler.decode_token(token, "access")

    user = await auth_api.user.find(
        username=payload.username,
        realm_name=payload.realm_name,
        includes=["user_roles.role"]
    )

    if not user:
        raise RecordNotFoundException("Usuario no encontrado")

    if user.session_id != payload.session_id:
        raise SessionInvalidatedException()

    return user


CurrentUser = Annotated[UserRead, Depends(get_current_user)]