"""
authswitch - RBAC Backend (Database)
Generado automáticamente por tai-api auth init

Implementación de operaciones RBAC usando DAOs async del schema auth.
"""
from __future__ import annotations
from typing import List, Optional

from .database import (
    auth_async_api as auth_api,
    UserCreate,
    UserRead,
    UserUpdateValues,
    UserRoleCreate,
)
from api.resources import (
    RecordNotFoundException,
)
from .rbac_models import RBACUser, RBACUserCreate, RBACUserUpdate, RBACRoleInfo, RBACRLS


def _user_to_rbac(user: UserRead, roles: Optional[List[str]] = None) -> RBACUser:
    """Convierte un UserRead a RBACUser."""
    if roles is None:
        roles = []
        for ur in (user.user_roles or []):
            if ur.role:
                roles.append(ur.role.name)
    return RBACUser(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        full_name=user.full_name,
        email=user.email,
        is_active=user.is_active,
        roles=roles,
        attributes=user.attributes,
    )


async def create_user(realm_name: str, data: RBACUserCreate) -> RBACUser:
    await auth_api.user.create(
        UserCreate(
            username=data.username,
            password=data.password,
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            is_active=data.is_active,
            attributes=data.attributes,
            realm_name=realm_name,
            user_roles=[
                UserRoleCreate(
                    user_name=data.username,
                    role_name=role_name,
                    realm_name=realm_name
                ) for role_name in data.roles]
        )
    )
    return await get_user(realm_name, data.username)


async def list_users(
    realm_name: str,
    limit: int = 100,
    offset: int = 0,
    is_active: Optional[bool] = None,
    username: Optional[str] = None,
    role: Optional[str] = None
) -> tuple[List[RBACUser], int]:
    users = await auth_api.user.find_many(
        realm_name=realm_name,
        limit=limit,
        offset=offset,
        is_active=is_active,
        username=username,
        includes=["user_roles.role"],
    )
    # PARCHE: Si se filtró por role, hay que filtrar manualmente porque el DAO no soporta ese filtro aún
    if role is not None:
        users = [u for u in users if any(ur.role and ur.role.name == role for ur in (u.user_roles or []))]
    
        total = len(users)
    else:
        total = await auth_api.user.count(realm_name=realm_name, is_active=is_active)
    return [_user_to_rbac(u) for u in users], total


async def get_user(realm_name: str, username: str) -> RBACUser:
    user = await auth_api.user.find(
        username=username,
        realm_name=realm_name,
        includes=["user_roles.role"],
    )
    if not user or user.realm_name != realm_name:
        raise RecordNotFoundException(f"Usuario '{username}' no encontrado en realm '{realm_name}'")
    return _user_to_rbac(user)


async def update_user(
    realm_name: str, username: str, data: RBACUserUpdate
) -> RBACUser:
    user = await auth_api.user.find(
        username=username,
        realm_name=realm_name,
        includes=["user_roles.role"],
    )
    if not user or user.realm_name != realm_name:
        raise RecordNotFoundException(f"Usuario '{username}' no encontrado en realm '{realm_name}'")

    updated_values = {}
    if data.first_name is not None:
        updated_values["first_name"] = data.first_name
    if data.last_name is not None:
        updated_values["last_name"] = data.last_name
    if data.email is not None:
        updated_values["email"] = data.email
    if data.is_active is not None:
        updated_values["is_active"] = data.is_active
    if data.password is not None:
        updated_values["password"] = data.password

    # Merge RLS attributes
    rls_attrs = data.attributes
    if rls_attrs is not None:
        current_attrs = user.attributes or {}
        current_attrs.update(rls_attrs)
        updated_values["attributes"] = current_attrs

    # Roles
    if data.roles is not None:
        old_roles_set = set(r.role.name for r in (user.user_roles or []) if r.role and r.role.name)
        new_roles_set = set(data.roles) if data.roles is not None else None
        for role_name in old_roles_set - new_roles_set:
            await remove_role(realm_name, username, role_name)
        for role_name in new_roles_set - old_roles_set:
            await assign_role(realm_name, username, role_name)

    if updated_values:
        await auth_api.user.update(
            username=username,
            realm_name=realm_name,
            updated_values=UserUpdateValues(**updated_values),
        )

    return await get_user(realm_name, username)


async def delete_user(realm_name: str, username: str) -> None:
    user = await auth_api.user.find(username=username, realm_name=realm_name)
    if not user or user.realm_name != realm_name:
        raise RecordNotFoundException(f"Usuario '{username}' no encontrado en realm '{realm_name}'")
    await auth_api.user.delete(username=username, realm_name=realm_name)


async def list_roles(realm_name: str) -> List[RBACRoleInfo]:
    roles = await auth_api.role.find_many(
        realm_name=realm_name,
        includes=["role_permissions.permission"],
    )
    result = []
    for role in roles:
        perms = []
        for rp in (role.role_permissions or []):
            if rp.permission:
                perms.append(rp.permission.name)
        result.append(RBACRoleInfo(
            name=role.name,
            description=role.description,
            permissions=perms,
            parent_role_name=role.parent_role_name,
        ))
    return result


async def assign_role(realm_name: str, username: str, role_name: str) -> None:
    user = await auth_api.user.find(username=username, realm_name=realm_name)
    if not user or user.realm_name != realm_name:
        raise RecordNotFoundException(f"Usuario '{username}' no encontrado en realm '{realm_name}'")

    role = await auth_api.role.find(name=role_name, realm_name=realm_name)
    if not role or role.realm_name != realm_name:
        raise RecordNotFoundException(f"Rol '{role_name}' no encontrado en realm '{realm_name}'")

    await auth_api.user_role.create(
        UserRoleCreate(user_name=username, role_name=role_name, realm_name=realm_name)
    )


async def remove_role(realm_name: str, username: str, role_name: str) -> None:
    user = await auth_api.user.find(username=username, realm_name=realm_name)
    if not user or user.realm_name != realm_name:
        raise RecordNotFoundException(f"Usuario '{username}' no encontrado en realm '{realm_name}'")

    user_roles = await auth_api.user_role.find_many(
        user_name=username,
        role_name=role_name,
        realm_name=realm_name,
    )
    if not user_roles:
        raise RecordNotFoundException(f"El usuario '{username}' no tiene el rol '{role_name}'")

    await auth_api.user_role.delete(id=user_roles[0].id)


async def list_rls(realm_name: str) -> List[RBACRLS]:
    rls_list = await auth_api.row_level_security.find_many(realm_name=realm_name)
    return [RBACRLS(
        target_schema=rls.schema_name,
        target_model=rls.table_name,
        target_field=rls.column_name,
    ) for rls in rls_list]