"""
Endpoints de documentación protegida con HTTP Basic Auth
Generado automáticamente por tai-api
"""
import os
import secrets
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

router = APIRouter(tags=["docs"])

security = HTTPBasic(auto_error=False)
DOCS_USERNAME = "admin"
DOCS_PASSWORD = os.getenv("API_DOCS_PWD", "admin")

def verify_docs_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales requeridas",
            headers={"WWW-Authenticate": "Basic"},
        )
    correct_username = secrets.compare_digest(credentials.username, DOCS_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, DOCS_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Basic"},
        )

@router.get("/docs", include_in_schema=False)
async def get_docs(_=Depends(verify_docs_credentials)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="authswitch - Docs")

@router.get("/redoc", include_in_schema=False)
async def get_redoc(_=Depends(verify_docs_credentials)):
    return get_redoc_html(openapi_url="/openapi.json", title="authswitch - ReDoc")