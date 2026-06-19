from fastapi import Query, Depends
from typing import Optional, List

from ......auth import requires_permissions, AccessToken
from ...._shared import username_context, get_model_by_name

from ...database import CommentAsyncDAO
from api.resources import APIResponse
from .docs import DELETE_MANY_RESPONSES, DELETE_MANY_SUMMARY
from ... import comment_router

@comment_router.delete("",
    response_model=APIResponse[int],
    response_description="Número de registros de comment eliminados",
    operation_id="public_comment_delete_many",
    summary=DELETE_MANY_SUMMARY,
    responses=DELETE_MANY_RESPONSES
)
async def comment_delete_many(
    content: Optional[str] = Query(None, description="Filtrar por content. Contenido del comentario"),
    in_content: Optional[List[str]] = Query(None, description="Filtrar por múltiples valores de content"),
    post_id: Optional[int] = Query(None, description="Filtrar por post_id"),
    in_post_id: Optional[List[int]] = Query(None, description="Filtrar por múltiples valores de post_id"),
    token: AccessToken = Depends(requires_permissions("delete", "comment")),
) -> APIResponse[int]:
    """
    Elimina múltiples Comments que coincidan con los filtros.
    """
    with username_context(token.preferred_username):
        result = await CommentAsyncDAO.delete_many(
            content=content,
            in_content=in_content,
            post_id=post_id,
            in_post_id=in_post_id,
        )

        message = f"{result} Comments eliminados exitosamente" if result > 0 else "No se encontraron registros que coincidan con los criterios"

        return APIResponse.success(
            data=result,
            message=message
        )
