"""
Script para generar los DAOs del schema auth de tai-api.
Ejecutar una vez para pre-generar los archivos que se commitean en tai_api/rbac/database/.

Requisitos:
- tai-sql instalado
- Variable de entorno MAIN_DATABASE_URL (se usa solo para config, no conecta)

Uso:
python scripts/generate_auth_schema.py
"""
from __future__ import annotations
import os
from tai_sql import *
from tai_sql.generators import PythonClientGenerator


# Configurar el datasource
datasource(
    provider=env('MAIN_DATABASE_URL'),
    schema='auth',
    syntax='v2',
    operative_fields=False,
)


# ============================================================================
# ENUMS
# ============================================================================

class PermissionType(Enum):
    """Tipo de permiso: API (endpoints) o APP (funcionalidades de aplicación)"""
    API = 'api'
    APP = 'app'


# ============================================================================
# TABLAS
# ============================================================================

class Realm(Table):
    """Realm de autenticación — agrupa usuarios, roles y permisos"""
    __tablename__ = "realm"

    name: col[str] = column(primary_key=True, description="Nombre único del realm")
    description: col[str | None] = column(description="Descripción del realm")

    users: onetomany[User]
    roles: onetomany[Role]
    permissions: onetomany[Permission]

    def feed(self) -> list:
        return [
            Realm(name="main", description="Main Realm")
        ]


class User(Table):
    """Usuario de autenticación"""
    __tablename__ = "user"

    username: col[str] = column(primary_key=True, description="Nombre de usuario único")
    realm_name: col[str] = column(primary_key=True, description="Realm al que pertenece el usuario")

    first_name: col[str | None] = column(description="Nombre del usuario")
    last_name: col[str | None] = column(description="Apellido del usuario")
    password: col[str] = column(encrypt=True, description="Contraseña encriptada")
    email: col[str | None] = column(description="Correo electrónico")
    is_active: col[bool] = column(default=True, description="Usuario activo")
    session_id: col[str | None] = column(description="ID de sesión actual (para control de concurrencia)")
    password_expiration: col[datetime | None] = column(description="Fecha de expiración de la contraseña")
    attributes: col[dict | None] = column(description="Atributos adicionales del usuario (JSON)")

    realm: manytoone[Realm] = relation(fields=["realm_name"], references=["name"], backref="users")

    user_roles: onetomany[UserRole]

    def feed(self) -> list:
        return [
            User(
                username="admin",
                password=os.getenv("ADMIN_PWD", "admin"),
                email="admin@localhost",
                first_name="Admin",
                last_name="User",
                is_active=True,
                realm_name="main",
            )
        ]

    @calculated_column
    def full_name(self) -> str:
        return f"{self.first_name or ''} {self.last_name or ''}".strip() if self.first_name or self.last_name else None


class Role(Table):
    """Rol que agrupa permisos"""
    __tablename__ = "role"

    name: col[str] = column(primary_key=True, description="Nombre del rol")
    realm_name: col[str] = column(primary_key=True, description="Realm al que pertenece el rol")

    description: col[str | None] = column(description="Descripción del rol")
    attributes: col[dict | None] = column(description="Atributos adicionales del rol (JSON)")

    parent_role_name: col[str | None] = column(description="ID del rol padre para subroles (roles anidados)", self_reference="name")

    realm: manytoone[Realm] = relation(fields=["realm_name"], references=["name"], backref="roles")

    role_permissions: onetomany[RolePermission]
    user_roles: onetomany[UserRole]

    def feed(self) -> list:
        return [
            Role(
                name="Administrador",
                description="Rol de administrador con todos los permisos",
                realm_name="main",
                attributes={ },
            ),
        ]

class Permission(Table):
    """Permiso individual (API o APP)"""
    __tablename__ = "permission"

    name: col[str] = column(primary_key=True, description="Nombre del permiso (ej: usuario-read)")
    realm_name: col[str] = column(primary_key=True, description="Realm al que pertenece el permiso")

    description: col[str | None] = column(description="Descripción del permiso")
    type: col[PermissionType] = column(description="Tipo: api o app")
    attributes: col[dict | None] = column(description="Atributos adicionales (JSON)")

    realm: manytoone[Realm] = relation(fields=["realm_name"], references=["name"], backref="permissions")

    role_permissions: onetomany[RolePermission]

    def feed(self) -> list:
        return [
            Permission(
                name="sudo",
                description="Permiso total de superusuario",
                type=PermissionType.API.value,
                realm_name="main",
            ),
            Permission(
                name="main-admin",
                description="Administrador del realm main",
                type=PermissionType.API.value,
                realm_name="main",
            ),
        ]


class UserRole(Table):
    """Relación M2M entre User y Role"""
    __tablename__ = "user_role"

    id: col[bigint] = column(primary_key=True, autoincrement=True)
    user_name: col[str] = column(description="ID del usuario")
    role_name: col[str] = column(description="ID del rol")
    realm_name: col[str] = column(description="Realm al que pertenecen el usuario y el rol")

    user: manytoone[User] = relation(fields=["user_name","realm_name"], references=["username","realm_name"], backref="user_roles")
    role: manytoone[Role] = relation(fields=["role_name","realm_name"], references=["name","realm_name"], backref="user_roles")

    def feed(self) -> list:
        """Admin user con rol admin"""
        return [
            UserRole(user_name="admin", role_name="Administrador", realm_name="main"),  # admin-user → admin-role
        ]


class RolePermission(Table):
    """Relación M2M entre Role y Permission"""
    __tablename__ = "role_permission"

    id: col[bigint] = column(primary_key=True, autoincrement=True)
    role_name: col[str] = column(description="ID del rol")
    permission_name: col[str] = column(description="ID del permiso")
    realm_name: col[str] = column(description="Realm al que pertenecen el rol y el permiso")

    role: manytoone[Role] = relation(fields=["role_name","realm_name"], references=["name","realm_name"], backref="role_permissions")
    permission: manytoone[Permission] = relation(fields=["permission_name","realm_name"], references=["name","realm_name"], backref="role_permissions")

    def feed(self) -> list:
        """Admin role con permiso sudo"""
        return [
            RolePermission(role_name="Administrador", permission_name="sudo", realm_name="main"),  # admin-role → sudo
            RolePermission(role_name="Administrador", permission_name="main-admin", realm_name="main"),  # admin-role → main-admin
        ]


class RowLevelSecurity(Table):
    """Definición de reglas de seguridad a nivel de fila (RLS)"""
    __tablename__ = "row_level_security"

    realm_name: col[str] = column(primary_key=True, description="Realm al que pertenece la regla RLS")
    schema_name: col[str] = column(primary_key=True, description="Nombre del schema al que aplica la regla RLS")
    table_name: col[str] = column(primary_key=True, description="Nombre de la tabla a la que aplica la regla RLS")
    column_name: col[str] = column(primary_key=True, description="Nombre de la columna a la que se le aplica la regla RLS")