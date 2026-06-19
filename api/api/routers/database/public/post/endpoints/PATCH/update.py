from fastapi import Path, Body, Depends
from ......auth import requires_permissions, AccessToken
from ...._shared import username_context, get_model_by_name

from ...database import PostAsyncDAO, PostUpdateValues
from api.resources import APIResponse, RecordNotFoundException, ValidationException
from .docs import UPDATE_RESPONSES, UPDATE_SUMMARY, UPDATE_DESCRIPTION
from ... import post_router

@post_router.patch("/{id:int}",
    response_model=APIResponse[int],
    operation_id="public_post_update",
    summary=UPDATE_SUMMARY,
    description=UPDATE_DESCRIPTION,
    responses=UPDATE_RESPONSES
)
async def post_update(
    id: int = Path(..., description="Campo id de la tabla post"),
    values: PostUpdateValues = Body(...),
    token: AccessToken = Depends(requires_permissions("update", "post")),
) -> APIResponse[int]:
    """
    Actualiza un Post específico.
    """

    with username_context(token.preferred_username):
        existing = await PostAsyncDAO.find(
            id=id,
        )

        if existing is None:
            raise RecordNotFoundException("Post")

        result = await PostAsyncDAO.update(
            id=id,
            updated_values=values,
        )

        if result == 0:
            raise RecordNotFoundException("Post")

        return APIResponse.success(
            data=result,
            message="Post actualizado exitosamente"
        )
