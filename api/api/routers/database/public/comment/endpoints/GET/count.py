from fastapi import Query, Depends
from typing import Optional, List

from ......auth import requires_permissions, AccessToken
from ...._shared import username_context, get_model_by_name

from ...database import CommentAsyncDAO
from api.resources import APIResponse
from .docs import COUNT_RESPONSES, COUNT_SUMMARY
from ... import comment_router

@comment_router.get("/count",
    response_model=APIResponse[int],
    response_description="Número de registros de comment según los filtros aplicados",
    operation_id="public_comment_count",
    summary=COUNT_SUMMARY,
    responses=COUNT_RESPONSES
)
async def comment_count(
    content: Optional[str] = Query(None, description="Filtrar por content. Contenido del comentario"),
    in_content: Optional[List[str]] = Query(None, description="Filtrar por múltiples valores de content"),
    post_id: Optional[int] = Query(None, description="Filtrar por post_id"),
    in_post_id: Optional[List[int]] = Query(None, description="Filtrar por múltiples valores de post_id"),
    token: AccessToken = Depends(requires_permissions("read", "comment")),
) -> APIResponse[int]:
    """
    Cuenta el número de Comments que coinciden con los filtros.
    """
    with username_context(token.preferred_username):
        result = await CommentAsyncDAO.count(
            content=content,
            in_content=in_content,
            post_id=post_id,
            in_post_id=in_post_id,
        )

        return APIResponse.success(
            data=result,
            message="Conteo realizado exitosamente"
        )
