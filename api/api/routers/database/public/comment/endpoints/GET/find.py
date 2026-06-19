from fastapi import Query, Path, Depends
from typing import Optional, List
from ......auth import requires_permissions, AccessToken
from ...._shared import username_context, get_model_by_name

from ...database import CommentAsyncDAO, CommentRead, RLS
from api.resources import APIResponse, RecordNotFoundException, ValidationException
from .docs import FIND_RESPONSES, FIND_SUMMARY, FIND_DESCRIPTION
from ... import comment_router

@comment_router.get("/{id:int}",
    response_model=APIResponse[CommentRead],
    response_description="Registro único de comment obtenido exitosamente",
    operation_id="public_comment_find",
    summary=FIND_SUMMARY,
    description=FIND_DESCRIPTION,
    responses=FIND_RESPONSES
)
async def comment_find(
    id: int = Path(..., description="Campo id de la tabla comment"),
    includes: List[str] = Query(None, description="Lista de relaciones a incluir en la respuesta para obtener datos relacionados. Especifica los nombres de las relaciones que deseas expandir"),
    token: AccessToken = Depends(requires_permissions("read", "comment")),
) -> APIResponse[CommentRead]:
    if id <= 0:
        raise ValidationException("id debe ser mayor a 0", "id")
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
        result = await CommentAsyncDAO.find(
            id=id,
            includes=includes,
            rls=rls
        )

        if result is None:
            raise RecordNotFoundException("Comment")

        return APIResponse.success(
            data=result,
            message="Comment obtenido exitosamente"
        )
