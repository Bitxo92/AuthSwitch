from fastapi import Query, Depends
from typing import Optional, List
from datetime import datetime

from ......auth import requires_permissions, AccessToken
from ...._shared import username_context, get_model_by_name

from ...database import UsuarioAsyncDAO
from api.resources import APIResponse
from .docs import COUNT_RESPONSES, COUNT_SUMMARY
from ... import usuario_router

@usuario_router.get("/count",
    response_model=APIResponse[int],
    response_description="Número de registros de usuario según los filtros aplicados",
    operation_id="public_usuario_count",
    summary=COUNT_SUMMARY,
    responses=COUNT_RESPONSES
)
async def usuario_count(
    name: Optional[str] = Query(None, description="Filtrar por name. Nombre del usuario"),
    in_name: Optional[List[str]] = Query(None, description="Filtrar por múltiples valores de name"),
    email: Optional[str] = Query(None, description="Filtrar por email. Campo email de la tabla usuario"),
    in_email: Optional[List[str]] = Query(None, description="Filtrar por múltiples valores de email"),
    min_last_post_date: Optional[datetime] = Query(None, description="Valor mínimo para last_post_date (incluido)"),
    max_last_post_date: Optional[datetime] = Query(None, description="Valor máximo para last_post_date (incluido)"),
    token: AccessToken = Depends(requires_permissions("read", "usuario")),
) -> APIResponse[int]:
    """
    Cuenta el número de Usuarios que coinciden con los filtros.
    """
    with username_context(token.preferred_username):
        result = await UsuarioAsyncDAO.count(
            name=name,
            in_name=in_name,
            email=email,
            in_email=in_email,
            min_last_post_date=min_last_post_date,
            max_last_post_date=max_last_post_date,
        )

        return APIResponse.success(
            data=result,
            message="Conteo realizado exitosamente"
        )
