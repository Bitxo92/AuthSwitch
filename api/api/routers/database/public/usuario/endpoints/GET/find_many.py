from fastapi import Query, Depends
from typing import Optional, List, Literal
from datetime import datetime

from tai_alphi import Alphi
from ......auth import requires_permissions, AccessToken
from ...._shared import username_context, get_model_by_name

from ...database import UsuarioAsyncDAO, UsuarioRead, RLS
from api.resources import APIResponse, PaginatedResponse
from .docs import FIND_MANY_RESPONSES, FIND_MANY_SUMMARY, FIND_MANY_DESCRIPTION
from ... import usuario_router

logger = Alphi.get_logger_by_name("tai-api")

@usuario_router.get("",
    response_model=APIResponse[List[UsuarioRead]],
    response_description="Lista de registros de usuario obtenido exitosamente",
    operation_id="public_usuario_find_many",
    summary=FIND_MANY_SUMMARY,
    description=FIND_MANY_DESCRIPTION,
    responses=FIND_MANY_RESPONSES
)
async def usuario_find_many(
    limit: Optional[int] = Query(None, description="Número de registros a retornar.", gt=0),
    order_by: List[str] = Query(None, description="Lista de nombres de columnas para ordenar los resultados. Si no existen serán omitidas."),
    order: Optional[Literal["ASC", "DESC"]] = Query("ASC", description="Dirección de ordenamiento: 'ASC' para ascendente (por defecto), 'DESC' para descendente. Solo aplica si order_by está definido", regex="^(ASC|DESC)$"),
    offset: Optional[int] = Query(None, description="Número de registros a omitir desde el inicio. Útil para paginación. Debe ser un valor no negativo", ge=0),
    name: Optional[str] = Query(None, description="Filtrar por name. Nombre del usuario"),
    in_name: Optional[List[str]] = Query(None, description="Filtrar por múltiples valores de name"),
    email: Optional[str] = Query(None, description="Filtrar por email. Campo email de la tabla usuario"),
    in_email: Optional[List[str]] = Query(None, description="Filtrar por múltiples valores de email"),
    min_last_post_date: Optional[datetime] = Query(None, description="Valor mínimo para last_post_date (incluido)"),
    max_last_post_date: Optional[datetime] = Query(None, description="Valor máximo para last_post_date (incluido)"),
    includes: List[str] = Query(None, description="Lista de relaciones a incluir en la respuesta para obtener datos relacionados. Especifica los nombres de las relaciones que deseas expandir"),
    token: AccessToken = Depends(requires_permissions("read", "usuario")),
) -> APIResponse[List[UsuarioRead]]:
    rls = [
        RLS(
            target_model=model,
            target_column=col_name,
            values=conditions
        ) for schema_name, table_dict in (token.rls or {}).items()
        for table_name, col_dict in (table_dict or {}).items()
        for col_name, conditions in (col_dict or {}).items()
        if (
            (model := get_model_by_name(f"{schema_name}.{table_name}")) is not None 
        )
    ]

    with username_context(token.preferred_username):
        result = await UsuarioAsyncDAO.find_many(
            limit=limit,
            offset=offset,
            order_by=order_by,
            order=order,
            name=name,
            in_name=in_name,
            email=email,
            in_email=in_email,
            min_last_post_date=min_last_post_date,
            max_last_post_date=max_last_post_date,
            includes=includes,
            rls=rls
        )

        total = None
        if limit is not None or offset is not None:
            try:
                total = await UsuarioAsyncDAO.count(
                    name=name,
                    in_name=in_name,
                    email=email,
                    in_email=in_email,
                    min_last_post_date=min_last_post_date,
                    max_last_post_date=max_last_post_date,
                )
            except Exception as e:
                logger.warning(f"No se pudo obtener el total de registros: {str(e)}")

        return PaginatedResponse.success_paginated(
            data=result,
            total=total,
            limit=limit,
            offset=offset,
            message=f"Usuarios obtenidos exitosamente"
        )
