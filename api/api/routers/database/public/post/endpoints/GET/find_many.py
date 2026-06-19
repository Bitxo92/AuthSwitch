from fastapi import Query, Depends
from typing import Optional, List, Literal
from datetime import datetime

from tai_alphi import Alphi
from ......auth import requires_permissions, AccessToken
from ...._shared import username_context, get_model_by_name

from ...database import PostAsyncDAO, PostRead, RLS
from api.resources import APIResponse, PaginatedResponse
from .docs import FIND_MANY_RESPONSES, FIND_MANY_SUMMARY, FIND_MANY_DESCRIPTION
from ... import post_router

logger = Alphi.get_logger_by_name("tai-api")

@post_router.get("",
    response_model=APIResponse[List[PostRead]],
    response_description="Lista de registros de post obtenido exitosamente",
    operation_id="public_post_find_many",
    summary=FIND_MANY_SUMMARY,
    description=FIND_MANY_DESCRIPTION,
    responses=FIND_MANY_RESPONSES
)
async def post_find_many(
    limit: Optional[int] = Query(None, description="Número de registros a retornar.", gt=0),
    order_by: List[str] = Query(None, description="Lista de nombres de columnas para ordenar los resultados. Si no existen serán omitidas."),
    order: Optional[Literal["ASC", "DESC"]] = Query("ASC", description="Dirección de ordenamiento: 'ASC' para ascendente (por defecto), 'DESC' para descendente. Solo aplica si order_by está definido", regex="^(ASC|DESC)$"),
    offset: Optional[int] = Query(None, description="Número de registros a omitir desde el inicio. Útil para paginación. Debe ser un valor no negativo", ge=0),
    title: Optional[str] = Query(None, description="Filtrar por title. Campo title de la tabla post"),
    in_title: Optional[List[str]] = Query(None, description="Filtrar por múltiples valores de title"),
    content: Optional[str] = Query(None, description="Filtrar por content. Contenido del post"),
    in_content: Optional[List[str]] = Query(None, description="Filtrar por múltiples valores de content"),
    content_type: Optional[str] = Query(None, description="Filtrar por content_type. Campo content_type de la tabla post"),
    in_content_type: Optional[List[str]] = Query(None, description="Filtrar por múltiples valores de content_type"),
    min_timestamp: Optional[datetime] = Query(None, description="Valor mínimo para timestamp (incluido)"),
    max_timestamp: Optional[datetime] = Query(None, description="Valor máximo para timestamp (incluido)"),
    author_id: Optional[int] = Query(None, description="Filtrar por author_id"),
    in_author_id: Optional[List[int]] = Query(None, description="Filtrar por múltiples valores de author_id"),
    includes: List[str] = Query(None, description="Lista de relaciones a incluir en la respuesta para obtener datos relacionados. Especifica los nombres de las relaciones que deseas expandir"),
    token: AccessToken = Depends(requires_permissions("read", "post")),
) -> APIResponse[List[PostRead]]:
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
        result = await PostAsyncDAO.find_many(
            limit=limit,
            offset=offset,
            order_by=order_by,
            order=order,
            title=title,
            in_title=in_title,
            content=content,
            in_content=in_content,
            content_type=content_type,
            in_content_type=in_content_type,
            min_timestamp=min_timestamp,
            max_timestamp=max_timestamp,
            author_id=author_id,
            in_author_id=in_author_id,
            includes=includes,
            rls=rls
        )

        total = None
        if limit is not None or offset is not None:
            try:
                total = await PostAsyncDAO.count(
                    title=title,
                    in_title=in_title,
                    content=content,
                    in_content=in_content,
                    content_type=content_type,
                    in_content_type=in_content_type,
                    min_timestamp=min_timestamp,
                    max_timestamp=max_timestamp,
                    author_id=author_id,
                    in_author_id=in_author_id,
                )
            except Exception as e:
                logger.warning(f"No se pudo obtener el total de registros: {str(e)}")

        return PaginatedResponse.success_paginated(
            data=result,
            total=total,
            limit=limit,
            offset=offset,
            message=f"Posts obtenidos exitosamente"
        )
