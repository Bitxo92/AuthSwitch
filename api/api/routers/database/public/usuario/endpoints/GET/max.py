from fastapi import Query, Path, Depends
from typing import Optional, List
from datetime import datetime

from ......auth import requires_permissions, AccessToken
from ...._shared import username_context, get_model_by_name

from ...database import UsuarioAsyncDAO, AggRow, RLS
from api.resources import APIResponse, APIError, ErrorCode
from .docs import MAX_RESPONSES, MAX_SUMMARY
from ... import usuario_router

@usuario_router.get("/{field}/max",
    response_model=APIResponse[List[AggRow]],
    operation_id="public_usuario_max_field",
    summary=MAX_SUMMARY,
    responses=MAX_RESPONSES
)
async def usuario_max_field(
    field: str = Path(..., description="Nombre del campo para encontrar el valor máximo"),
    name: Optional[str] = Query(None, description="Filtrar por name. Nombre del usuario"),
    in_name: Optional[List[str]] = Query(None, description="Filtrar por múltiples valores de name"),
    email: Optional[str] = Query(None, description="Filtrar por email. Campo email de la tabla usuario"),
    in_email: Optional[List[str]] = Query(None, description="Filtrar por múltiples valores de email"),
    min_last_post_date: Optional[datetime] = Query(None, description="Valor mínimo para last_post_date (incluido)"),
    max_last_post_date: Optional[datetime] = Query(None, description="Valor máximo para last_post_date (incluido)"),
    token: AccessToken = Depends(requires_permissions("read", "usuario")),
) -> APIResponse[List[AggRow]]:
    """
    ## Resumen
    Encuentra el valor máximo de un campo específico que coincida con los filtros.

    ## Parámetros
    - **field** (path): Nombre del campo para encontrar el máximo.

    ## Filtros Opcionales
    - **name**: Filtrar por name
    - **in_name**: Filtrar por múltiples valores de name (OR lógico)
    - **email**: Filtrar por email
    - **in_email**: Filtrar por múltiples valores de email (OR lógico)
    - **min_last_post_date**: Filtrar por valor mínimo de last_post_date (incluído)
    - **max_last_post_date**: Filtrar por valor máximo de last_post_date (incluído)

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
        result = await UsuarioAsyncDAO.max(
            agg_fields=[field],
            name=name,
            in_name=in_name,
            email=email,
            in_email=in_email,
            min_last_post_date=min_last_post_date,
            max_last_post_date=max_last_post_date,
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
                message=f"Error al calcular el máximo de '{field}'"
            )

        return APIResponse.success(
            data=result.rows,
            message=f"Máximo de '{field}' calculado exitosamente",
            meta=result.metadata
        )
