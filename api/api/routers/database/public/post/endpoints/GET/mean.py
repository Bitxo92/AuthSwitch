from fastapi import Query, Path, Depends
from typing import Optional, List
from datetime import datetime

from ......auth import requires_permissions, AccessToken
from ...._shared import username_context, get_model_by_name

from ...database import PostAsyncDAO, AggRow, RLS
from api.resources import APIResponse, APIError, ErrorCode
from .docs import MEAN_RESPONSES, MEAN_SUMMARY
from ... import post_router

@post_router.get("/{field}/mean",
    response_model=APIResponse[List[AggRow]],
    operation_id="public_post_mean_field",
    summary=MEAN_SUMMARY,
    responses=MEAN_RESPONSES
)
async def post_mean_field(
    field: str = Path(..., description="Nombre del campo numérico para calcular la media"),
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
    token: AccessToken = Depends(requires_permissions("read", "post")),
) -> APIResponse[List[AggRow]]:
    """
    ## Resumen
    Calcula la media (promedio) de un campo numérico específico que coincida con los filtros.

    ## Parámetros
    - **field** (path): Nombre del campo numérico para calcular la media.

    ## Filtros Opcionales
    - **title**: Filtrar por title
    - **in_title**: Filtrar por múltiples valores de title (OR lógico)
    - **content**: Filtrar por content
    - **in_content**: Filtrar por múltiples valores de content (OR lógico)
    - **content_type**: Filtrar por content_type
    - **in_content_type**: Filtrar por múltiples valores de content_type (OR lógico)
    - **min_timestamp**: Filtrar por valor mínimo de timestamp (incluído)
    - **max_timestamp**: Filtrar por valor máximo de timestamp (incluído)
    - **author_id**: Filtrar por author_id
    - **in_author_id**: Filtrar por múltiples valores de author_id (OR lógico)

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
        result = await PostAsyncDAO.mean(
            agg_fields=[field],
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
                message=f"Error al calcular la media de '{field}'"
            )

        return APIResponse.success(
            data=result.rows,
            message=f"Media de '{field}' calculada exitosamente",
            meta=result.metadata
        )
