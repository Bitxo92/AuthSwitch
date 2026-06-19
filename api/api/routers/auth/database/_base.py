# Este archivo ha sido generado automáticamente por tai-sql
# No modifiques este archivo directamente

from __future__ import annotations
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import DeclarativeBase
import os
from cryptography.fernet import Fernet
import base64


class Base(DeclarativeBase):
    pass


# Configuración de encriptación
_secret_key = os.getenv('SECRET_KEY')
if not _secret_key:
    raise ValueError(
        f"Variable de entorno 'SECRET_KEY' no encontrada para encriptación. "
        f"Por favor, configure la variable de entorno 'SECRET_KEY' en su sistema "
        f"con una clave secreta segura antes de ejecutar la aplicación. "
        f"Ejemplo: export SECRET_KEY='su-clave-secreta-de-32-caracteres-aqui'"
    )

# Generar clave Fernet desde la clave secreta
_fernet_key = base64.urlsafe_b64encode(_secret_key.encode()[:32].ljust(32, b'\0'))
_cipher = Fernet(_fernet_key)

def encrypt_value(value: str) -> str:
    """Encripta un valor string"""
    if value is None:
        return None
    return _cipher.encrypt(value.encode()).decode()

def decrypt_value(value: str) -> str:
    """Desencripta un valor string"""
    if value is None:
        return None
    return _cipher.decrypt(value.encode()).decode()

