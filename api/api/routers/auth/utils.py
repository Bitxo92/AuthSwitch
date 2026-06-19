"""
authswitch - Utils
Generado automáticamente por tai-api set-auth

Este módulo contiene utilidades para la integración con database.
"""
from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime



class LoginRequest(BaseModel):
    """Modelo para la solicitud de login"""
    username: str
    password: str


class RefreshRequest(BaseModel):
    """Modelo para solicitud de refresh token"""
    refresh_token: str


class LoginData(BaseModel):
    """Modelo para la respuesta de login"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserData


class LogoutData(BaseModel):
    """Modelo para la respuesta de logout"""
    message: str = "Sesión cerrada"


class UserData(BaseModel):
    """Modelo para la información del usuario en la respuesta de login y refresh"""
    sub: Optional[str] = None
    preferred_username: str
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    permissions: Optional[List[str]] = None


class UserInfoData(BaseModel):
    """Modelo para la información del usuario"""
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    is_active: bool = True
    roles: Optional[List[str]] = None
    permissions: Optional[List[str]] = None
    password_expiration: Optional[datetime] = None


