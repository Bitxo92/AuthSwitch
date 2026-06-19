"""
authswitch - Login Router
Generado automáticamente por tai-api auth init

Endpoints de autenticación con JWT y base de datos.
"""
from __future__ import annotations
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

from .jwt import JWTHandler
from .dependencies import CurrentUser
from .database import AuthAsyncAPI, UserRead, UserUpdateValues, RoleRead
from api.resources import (
    APIResponse,
    InvalidCredentialsException,
    InvalidTokenException,
    DatabaseException,
)
from .utils import (
    LoginRequest,
    LoginData,
    LogoutData,
    RefreshRequest,
    UserData,
    UserInfoData,
)

router = APIRouter(prefix="/auth", tags=["Autenticación"])

auth_api = AuthAsyncAPI()


async def _load_user_permissions(user: UserRead) -> List[str]:
    """Carga los permisos del usuario a través de sus roles y sus ancestros."""

    user = await auth_api.user.find(
        username=user.username,
        realm_name=user.realm_name,
        includes=["user_roles"],
    )
    if not user or not user.user_roles:
        return []

    role_names = [r.role_name for r in user.user_roles if r.role_name]
    if not role_names:
        return []

    roles = await auth_api.role.find_many(
        in_name=role_names,
        includes=["role_permissions.permission"],
        tree_mode="ancestors",
    )
    if not roles:
        return []

    permissions: set[str] = set()

    for role in roles:
        perms = await _load_recursive_permissions(role)
        if perms:
            permissions.update(perms)

    return list(permissions)


async def _load_recursive_permissions(role: RoleRead) -> List[str]:
    """Carga recursivamente los permisos de un rol y sus subroles."""
    permissions = []
    if role.ancestors:
        for ancestor in role.ancestors:
            permissions.extend(await _load_recursive_permissions(ancestor))
    for rp in role.role_permissions or []:
        if rp.permission:
            permissions.append(rp.permission.name)
    return permissions


async def _authenticate_user(username: str, password: str, realm_name: str) -> tuple[UserRead, List[str]]:
    """Autentica un usuario contra la base de datos del schema auth."""

    user = await auth_api.user.find(
        username=username,
        realm_name=realm_name,
        includes=["user_roles.role"]
    )

    if not user or user.realm_name != realm_name:
        raise InvalidCredentialsException("Username/password inválidos")

    if not password == user.password:
        raise InvalidCredentialsException("Username/password inválidos")

    if not user.is_active:
        raise InvalidCredentialsException("Usuario deshabilitado")


    permissions = await _load_user_permissions(user)
    return user, permissions


# ============================================================================
# ENDPOINTS DE AUTENTICACIÓN
# ============================================================================

@router.post("/{realm_name}/login", response_model=APIResponse[LoginData])
async def login(realm_name: str, login_request: LoginRequest):
    user, permissions = await _authenticate_user(
        username=login_request.username,
        password=login_request.password,
        realm_name=realm_name,
    )

    session_id = JWTHandler.generate_session_id()
    await auth_api.user.update(
        username=user.username,
        realm_name=user.realm_name,
        updated_values=UserUpdateValues(session_id=session_id)
    )

    token_response = JWTHandler.create_tokens(
        username=user.username,
        realm_name=realm_name,
        session_id=session_id,
        permissions=permissions,
        attributes=user.attributes,
    )

    login_data = LoginData(
        access_token=token_response.access_token,
        refresh_token=token_response.refresh_token,
        token_type="bearer",
        user=UserData(
            sub=None,
            preferred_username=user.username,
            given_name=user.first_name,
            family_name=user.last_name,
            name=user.full_name,
            email=user.email,
            email_verified=True,
            permissions=permissions,
         ),
    )

    return APIResponse.success(data=login_data, message="Autenticación exitosa")


@router.post("/docslogin", include_in_schema=False, response_model=LoginData)
async def docs_login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Formato: username@realm
    raw = (form_data.username or "").strip()
    if "@" in raw:
        username, realm_name = raw.rsplit("@", 1)
    else:
        username, realm_name = raw, "main"

    user, permissions = await _authenticate_user(
        username=username, password=form_data.password, realm_name=realm_name
    )

    session_id = JWTHandler.generate_session_id()
    await auth_api.user.update(
        username=user.username,
        realm_name=user.realm_name,
        updated_values=UserUpdateValues(session_id=session_id)
    )

    token_response = JWTHandler.create_tokens(
        username=user.username,
        realm_name=user.realm_name,
        session_id=session_id,
        permissions=permissions,
        attributes=user.attributes,
    )

    return LoginData(
        access_token=token_response.access_token,
        refresh_token=token_response.refresh_token,
        token_type="bearer",
        user=UserData(
            sub=None,
            preferred_username=user.username,
            given_name=user.first_name,
            family_name=user.last_name,
            name=user.full_name,
            email=user.email,
            email_verified=True,
            permissions=permissions,
         ),
    )


@router.post("/logout", response_model=APIResponse[LogoutData])
async def logout(
    current_user: CurrentUser,
    refresh_request: RefreshRequest
):
    decoded_token = JWTHandler.decode_token(
        token=refresh_request.refresh_token,
        grant_type="refresh"
    )

    if decoded_token.session_id != current_user.session_id:
        raise InvalidTokenException()

    try:
        await auth_api.user.update(
            username=current_user.username,
            realm_name=current_user.realm_name,
            updated_values=UserUpdateValues(session_id=None)
        )
    except Exception as e:
        raise DatabaseException(f"Error en logout: {str(e)}")

    return APIResponse.success(
        data=LogoutData(),
        message="Sesión cerrada exitosamente"
    )


@router.post("/refresh", response_model=APIResponse[LoginData])
async def refresh_token(
    refresh_request: RefreshRequest,
):
    decoded_token = JWTHandler.decode_token(
        token=refresh_request.refresh_token,
        grant_type="refresh"
    )

    user = await auth_api.user.find(
        username=decoded_token.username,
        realm_name=decoded_token.realm_name,
        includes=["user_roles.role"]
    )
    permissions = await _load_user_permissions(user)

    token_response = JWTHandler.create_tokens(
        username=user.username,
        realm_name=user.realm_name,
        session_id=user.session_id,
        permissions=permissions,
        attributes=user.attributes,
    )

    refresh_data = LoginData(
        access_token=token_response.access_token,
        refresh_token=token_response.refresh_token,
        token_type="bearer",
        user=UserData(
            sub=None,
            preferred_username=user.username,
            given_name=user.first_name,
            family_name=user.last_name,
            name=user.full_name,
            email=user.email,
            email_verified=True,
            permissions=permissions,
        )
    )
    return APIResponse.success(data=refresh_data, message="Token refreshed successfully")


@router.get("/me", response_model=APIResponse[UserInfoData])
async def get_current_user_info(current_user: CurrentUser):
    permissions = await _load_user_permissions(current_user)

    user_roles = []
    for ur in (current_user.user_roles or []):
        if ur.role:
            user_roles.append(ur.role.name)

    user_info = UserInfoData(
        username=current_user.username,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        full_name=current_user.full_name,
        email=current_user.email,
        is_active=current_user.is_active,
        roles=user_roles,
        permissions=permissions,
    )

    return APIResponse.success(
        data=user_info,
        message="Información del usuario obtenida exitosamente"
    )