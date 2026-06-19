"""
authswitch - RBAC Models
Generado automáticamente por tai-api auth init

Modelos Pydantic unificados para la API de gestión RBAC.
Independientes del backend de autenticación (Database / Keycloak).
"""
from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Any, Dict, Optional, List


class RBACUserCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    username: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    is_active: bool = True
    roles: List[str] = []

    @property
    def attributes(self) -> Dict[str, Any]:
        """Construye el dict de attributes a partir de los campos RLS."""
        attrs: Dict[str, Any] = {}
        return attrs


class RBACUserUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    roles: Optional[List[str]] = None

    @property
    def attributes(self) -> Optional[Dict[str, Any]]:
        """Construye el dict de attributes a partir de los campos RLS definidos (no None)."""
        attrs: Dict[str, Any] = {}
        has_any = False
        return attrs if has_any else None


class RBACUser(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    is_active: bool = True
    roles: List[str] = []

    @model_validator(mode="before")
    @classmethod
    def _extract_rls_from_attributes(cls, data: Any) -> Any:
        """Extrae campos RLS del dict attributes al nivel superior del modelo."""
        if isinstance(data, dict):
            attributes = data.pop("attributes", None) or {}
        return data


class RBACRoleInfo(BaseModel):
    name: str
    description: Optional[str] = None
    permissions: List[str] = []
    parent_role_name: Optional[str] = None


class RBACRLS(BaseModel):
    target_schema: str
    target_model: str
    target_field: str