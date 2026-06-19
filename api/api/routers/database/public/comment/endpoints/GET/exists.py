from fastapi import Query, Depends
from typing import Optional, List

from ......auth import requires_permissions, AccessToken
from ...._shared import username_context, get_model_by_name

from ...database import CommentAsyncDAO
from api.resources import APIResponse
from .docs import EXISTS_RESPONSES, EXISTS_SUMMARY
from ... import comment_router

@comment_router.get("/exists",
    response_model=APIResponse[bool],
    operation_id="public_comment_exists",
    summary=EXISTS_SUMMARY,
    responses=EXISTS_RESPONSES
)
async def comment_exists(
    content: Optional[str] = Query(None, description="Filtrar por content. Contenido del comentario"),
    in_content: Optional[List[str]] = Query(None, description="Filtrar por múltiples valores de content"),
    post_id: Optional[int] = Query(None, description="Filtrar por post_id"),
    in_post_id: Optional[List[int]] = Query(None, description="Filtrar por múltiples valores de post_id"),
    token: AccessToken = Depends(requires_permissions("read", "comment")),
) -> APIResponse[bool]:
    """
    Verifica si existe al menos un comment que coincida con los filtros.
    """
    with username_context(token.preferred_username):
        result = await CommentAsyncDAO.exists(
            content=content,
            in_content=in_content,
            post_id=post_id,
            in_post_id=in_post_id,
        )

        return APIResponse.success(
            data=result,
            message="Verificación realizada exitosamente"
        )
