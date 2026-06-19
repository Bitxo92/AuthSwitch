from fastapi import Query, Path, Depends
from typing import Optional, List

from ......auth import requires_permissions, AccessToken
from ...._shared import username_context, get_model_by_name

from ...database import UserStatsAsyncDAO, AggRow, RLS
from api.resources import APIResponse, APIError, ErrorCode
from .docs import SUM_RESPONSES, SUM_SUMMARY
from ... import user_stats_router

@user_stats_router.get("/{field}/sum",
    response_model=APIResponse[List[AggRow]],
    operation_id="public_user_stats_sum_field",
    summary=SUM_SUMMARY,
    responses=SUM_RESPONSES
)
async def user_stats_sum_field(
    field: str = Path(..., description="Nombre del campo numérico a sumar"),
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
    token: AccessToken = Depends(requires_permissions("read", "user_stats")),
) -> APIResponse[List[AggRow]]:
    """
    ## Resumen
    Calcula la suma de un campo numérico específico que coincida con los filtros.

    ## Parámetros
    - **field** (path): Nombre del campo numérico a sumar.

    ## Filtros Opcionales
    - **user_id**: Filtrar por user_id
    - **in_user_id**: Filtrar por múltiples valores de user_id (OR lógico)
    - **min_user_id**: Filtrar por valor mínimo de user_id (incluído)
    - **max_user_id**: Filtrar por valor máximo de user_id (incluído)
    - **user_name**: Filtrar por user_name
    - **in_user_name**: Filtrar por múltiples valores de user_name (OR lógico)
    - **post_count**: Filtrar por post_count
    - **in_post_count**: Filtrar por múltiples valores de post_count (OR lógico)
    - **min_post_count**: Filtrar por valor mínimo de post_count (incluído)
    - **max_post_count**: Filtrar por valor máximo de post_count (incluído)

    """
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
        result = await UserStatsAsyncDAO.sum(
            agg_fields=[field],
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
            rls=rls
        )

        if not result.success:
            return APIResponse.error(
                errors=[
                    APIError(
                        code=ErrorCode.VALIDATION_ERROR,
                        message=error,
                        field=field
                    ) for error in result.errors
                ],
                message=f"Error al calcular la suma de '{field}'"
            )

        return APIResponse.success(
            data=result.rows,
            message=f"Suma de '{field}' calculada exitosamente",
            meta=result.metadata
        )
