from fastapi import Query, Depends
from typing import Optional, List
from datetime import datetime

from ......auth import requires_permissions, AccessToken
from ...._shared import username_context, get_model_by_name

from ...database import UsuarioAsyncDAO
from api.resources import APIResponse
from .docs import DELETE_MANY_RESPONSES, DELETE_MANY_SUMMARY
from ... import usuario_router

@usuario_router.delete("",
    response_model=APIResponse[int],
    response_description="Número de registros de usuario eliminados",
    operation_id="public_usuario_delete_many",
    summary=DELETE_MANY_SUMMARY,
    responses=DELETE_MANY_RESPONSES
)
async def usuario_delete_many(
    name: Optional[str] = Query(None, description="Filtrar por name. Nombre del usuario"),
    in_name: Optional[List[str]] = Query(None, description="Filtrar por múltiples valores de name"),
    email: Optional[str] = Query(None, description="Filtrar por email. Campo email de la tabla usuario"),
    in_email: Optional[List[str]] = Query(None, description="Filtrar por múltiples valores de email"),
    min_last_post_date: Optional[datetime] = Query(None, description="Valor mínimo para last_post_date (incluido)"),
    max_last_post_date: Optional[datetime] = Query(None, description="Valor máximo para last_post_date (incluido)"),
    token: AccessToken = Depends(requires_permissions("delete", "usuario")),
) -> APIResponse[int]:
    """
    Elimina múltiples Usuarios que coincidan con los filtros.
    """
    with username_context(token.preferred_username):
        result = await UsuarioAsyncDAO.delete_many(
            name=name,
            in_name=in_name,
            email=email,
            in_email=in_email,
            min_last_post_date=min_last_post_date,
            max_last_post_date=max_last_post_date,
        )

        message = f"{result} Usuarios eliminados exitosamente" if result > 0 else "No se encontraron registros que coincidan con los criterios"

        return APIResponse.success(
            data=result,
            message=message
        )
