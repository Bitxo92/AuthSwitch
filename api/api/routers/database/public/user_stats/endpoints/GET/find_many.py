from fastapi import Query, Depends
from typing import Optional, List, Literal

from tai_alphi import Alphi
from ......auth import requires_permissions, AccessToken
from ...._shared import username_context, get_model_by_name

from ...database import UserStatsAsyncDAO, UserStatsRead, RLS
from api.resources import APIResponse, PaginatedResponse
from .docs import FIND_MANY_RESPONSES, FIND_MANY_SUMMARY, FIND_MANY_DESCRIPTION
from ... import user_stats_router

logger = Alphi.get_logger_by_name("tai-api")

@user_stats_router.get("",
    response_model=APIResponse[List[UserStatsRead]],
    response_description="Lista de registros de user_stats obtenido exitosamente",
    operation_id="public_user_stats_find_many",
    summary=FIND_MANY_SUMMARY,
    description=FIND_MANY_DESCRIPTION,
    responses=FIND_MANY_RESPONSES
)
async def user_stats_find_many(
    limit: Optional[int] = Query(None, description="Número de registros a retornar.", gt=0),
    order_by: List[str] = Query(None, description="Lista de nombres de columnas para ordenar los resultados. Si no existen serán omitidas."),
    order: Optional[Literal["ASC", "DESC"]] = Query("ASC", description="Dirección de ordenamiento: 'ASC' para ascendente (por defecto), 'DESC' para descendente. Solo aplica si order_by está definido", regex="^(ASC|DESC)$"),
    offset: Optional[int] = Query(None, description="Número de registros a omitir desde el inicio. Útil para paginación. Debe ser un valor no negativo", ge=0),
    user_id: Optional[int] = Query(None, description="Filtrar por user_id. Campo user_id de la tabla user_stats"),
    in_user_id: Optional[List[int]] = Query(None, description="Filtrar por múltiples valores de user_id"),
    min_user_id: Optional[int] = Query(None, description="Valor mínimo para user_id (incluido)"),
    max_user_id: Optional[int] = Query(None, description="Valor máximo para user_id (incluido)"),
    user_name: Optional[str] = Query(None, description="Filtrar por user_name. Campo user_name de la tabla user_stats"),
    in_user_name: Optional[List[str]] = Query(None, description="Filtrar por múltiples valores de user_name"),
    post_count: Optional[int] = Query(None, description="Filtrar por post_count. Campo post_count de la tabla user_stats"),
    in_post_count: Optional[List[int]] = Query(None, description="Filtrar por múltiples valores de post_count"),
    min_post_count: Optional[int] = Query(None, description="Valor mínimo para post_count (incluido)"),
    max_post_count: Optional[int] = Query(None, description="Valor máximo para post_count (incluido)"),
    includes: List[str] = Query(None, description="Lista de relaciones a incluir en la respuesta para obtener datos relacionados. Especifica los nombres de las relaciones que deseas expandir"),
    token: AccessToken = Depends(requires_permissions("read", "user_stats")),
) -> APIResponse[List[UserStatsRead]]:
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
        result = await UserStatsAsyncDAO.find_many(
            limit=limit,
            offset=offset,
            order_by=order_by,
            order=order,
            user_id=user_id,
            in_user_id=in_user_id,
            min_user_id=min_user_id,
            max_user_id=max_user_id,
            user_name=user_name,
            in_user_name=in_user_name,
            post_count=post_count,
            in_post_count=in_post_count,
            min_post_count=min_post_count,
            max_post_count=max_post_count,
            includes=includes,
            rls=rls
        )

        total = None
        if limit is not None or offset is not None:
            try:
                total = await UserStatsAsyncDAO.count(
                    user_id=user_id,
                    in_user_id=in_user_id,
                    min_user_id=min_user_id,
                    max_user_id=max_user_id,
                    user_name=user_name,
                    in_user_name=in_user_name,
                    post_count=post_count,
                    in_post_count=in_post_count,
                    min_post_count=min_post_count,
                    max_post_count=max_post_count,
                )
            except Exception as e:
                logger.warning(f"No se pudo obtener el total de registros: {str(e)}")

        return PaginatedResponse.success_paginated(
            data=result,
            total=total,
            limit=limit,
            offset=offset,
            message=f"UserStatss obtenidos exitosamente"
        )
