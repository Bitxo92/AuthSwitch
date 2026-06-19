from fastapi import Depends
from ......auth import requires_permissions, AccessToken
from ...._shared import username_context, get_model_by_name

from ...database import PostAsyncDAO, PostUpdate
from api.resources import APIResponse
from .docs import UPDATE_MANY_RESPONSES, UPDATE_MANY_SUMMARY
from ... import post_router

@post_router.patch("",
    response_model=APIResponse[int],
    operation_id="public_post_update_many",
    summary=UPDATE_MANY_SUMMARY,
    responses=UPDATE_MANY_RESPONSES
)
async def post_update_many(
    payload: PostUpdate,
    token: AccessToken = Depends(requires_permissions("update", "post")),
) -> APIResponse[int]:
    """
    Actualiza múltiples Posts.
    """
    with username_context(token.preferred_username):
        result = await PostAsyncDAO.update_many(
            payload,
        )

        message = f"{result} Posts actualizados exitosamente" if result > 0 else "No se encontraron registros que coincidan con los criterios"

        return APIResponse.success(
            data=result,
            message=message
        )
