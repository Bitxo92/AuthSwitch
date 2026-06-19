from fastapi import Query, Path, Depends
from typing import Optional, List

from ......auth import requires_permissions, AccessToken
from ...._shared import username_context, get_model_by_name

from ...database import CommentAsyncDAO, AggRow, RLS
from api.resources import APIResponse, APIError, ErrorCode
from .docs import SUM_RESPONSES, SUM_SUMMARY
from ... import comment_router

@comment_router.get("/{field}/sum",
    response_model=APIResponse[List[AggRow]],
    operation_id="public_comment_sum_field",
    summary=SUM_SUMMARY,
    responses=SUM_RESPONSES
)
async def comment_sum_field(
    field: str = Path(..., description="Nombre del campo numérico a sumar"),
    content: Optional[str] = Query(None, description="Filtrar por content. Contenido del comentario"),
    in_content: Optional[List[str]] = Query(None, description="Filtrar por múltiples valores de content"),
    post_id: Optional[int] = Query(None, description="Filtrar por post_id"),
    in_post_id: Optional[List[int]] = Query(None, description="Filtrar por múltiples valores de post_id"),
    token: AccessToken = Depends(requires_permissions("read", "comment")),
) -> APIResponse[List[AggRow]]:
    """
    ## Resumen
    Calcula la suma de un campo numérico específico que coincida con los filtros.

    ## Parámetros
    - **field** (path): Nombre del campo numérico a sumar.

    ## Filtros Opcionales
    - **content**: Filtrar por content
    - **in_content**: Filtrar por múltiples valores de content (OR lógico)
    - **post_id**: Filtrar por post_id
    - **in_post_id**: Filtrar por múltiples valores de post_id (OR lógico)

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
        result = await CommentAsyncDAO.sum(
            agg_fields=[field],
            content=content,
            in_content=in_content,
            post_id=post_id,
            in_post_id=in_post_id,
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
