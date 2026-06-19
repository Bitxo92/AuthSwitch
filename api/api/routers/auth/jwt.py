"""
authswitch - JWT Token Handler
Generado automáticamente por tai-api auth init
"""
from __future__ import annotations
import os
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Literal
from pydantic import BaseModel
from api.resources import InvalidTokenException, TokenExpiredException

JWT_SECRET_KEY = os.getenv("SECRET_KEY")
if not JWT_SECRET_KEY:
    raise ValueError(
        "La clave secreta JWT no está configurada. "
        "Establezca la variable de entorno SECRET_KEY."
    )
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION = 5


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class AccessToken(BaseModel):
    username: str
    realm_name: str
    exp: datetime
    session_id: Optional[str] = None
    permissions: List[str] = []
    rls: Optional[dict] = None

    @property
    def preferred_username(self) -> str:
        return self.username

    @property
    def api_roles(self) -> List[str]:
        return self.permissions

    class Config:
        json_encoders = {
            datetime: lambda v: int(v.timestamp())
        }


class JWTHandler:

    @staticmethod
    def create_tokens(
        username: str,
        realm_name: str,
        session_id: Optional[str] = None,
        permissions: Optional[List[str]] = None,
        attributes: Optional[dict] = None,
    ) -> TokenResponse:
        access_expiration = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRATION)
        refresh_expiration = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRATION * 4)

        # Procesar atributos para extraer condiciones RLS
        rls_conditions = {}
        for attribute_key, attribute_value in (attributes or {}).items():
            keys = attribute_key.split(".")

            if keys[0] == "rls" and len(keys) >= 4:
                _, schema, resource, field = keys

                if not isinstance(attribute_value, list):
                    attribute_value = [str(attribute_value)]
                else:
                    attribute_value = [str(v) for v in attribute_value]

                if schema not in rls_conditions:
                    rls_conditions[schema] = {}

                if resource not in rls_conditions[schema]:
                    rls_conditions[schema][resource] = {}

                rls_conditions[schema][resource][field] = attribute_value


        access_payload = {
            "username": username,
            "realm_name": realm_name,
            "typ": "access",
            "exp": access_expiration,
            "session_id": session_id,
            "permissions": permissions or [],
            "rls": rls_conditions or {},
        }

        access_token = jwt.encode(access_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

        refresh_payload = {
            "username": username,
            "realm_name": realm_name,
            "typ": "refresh",
            "exp": refresh_expiration,
            "session_id": session_id,
        }

        refresh_token = jwt.encode(refresh_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )


    @staticmethod
    def decode_token(token: str, grant_type: Literal["access", "refresh"]) -> AccessToken:
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])

            if isinstance(payload.get("typ"), (str)):
                if payload["typ"] != grant_type:
                    raise InvalidTokenException(
                        f"Tipo de token inválido: se esperaba '{grant_type}' pero se recibió '{payload['typ']}'"
                    )

            if isinstance(payload.get("exp"), (int, float)):
                payload["exp"] = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)

            return AccessToken(**payload)

        except ExpiredSignatureError:
            raise TokenExpiredException("El token ha expirado")
        except JWTError:
            raise InvalidTokenException("Token inválido")
        except Exception as e:
            raise InvalidTokenException(f"Error al decodificar token: {str(e)}")

    @staticmethod
    def generate_session_id() -> str:
        return str(uuid.uuid4())