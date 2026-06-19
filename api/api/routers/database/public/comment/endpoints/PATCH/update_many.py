from fastapi import Depends
from ......auth import requires_permissions, AccessToken
from ...._shared import username_context, get_model_by_name

from ...database import CommentAsyncDAO, CommentUpdate
from api.resources import APIResponse
from .docs import UPDATE_MANY_RESPONSES, UPDATE_MANY_SUMMARY
from ... import comment_router

@comment_router.patch("",
    response_model=APIResponse[int],
    operation_id="public_comment_update_many",
    summary=UPDATE_MANY_SUMMARY,
    responses=UPDATE_MANY_RESPONSES
)
async def comment_update_many(
    payload: CommentUpdate,
    token: AccessToken = Depends(requires_permissions("update", "comment")),
) -> APIResponse[int]:
    """
    Actualiza múltiples Comments.
    """
    with username_context(token.preferred_username):
        result = await CommentAsyncDAO.update_many(
            payload,
        )

        message = f"{result} Comments actualizados exitosamente" if result > 0 else "No se encontraron registros que coincidan con los criterios"

        return APIResponse.success(
            data=result,
            message=message
        )
