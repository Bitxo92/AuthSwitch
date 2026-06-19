from fastapi import Path, Depends
from ......auth import requires_permissions, AccessToken
from ...._shared import username_context, get_model_by_name

from ...database import PostAsyncDAO
from api.resources import APIResponse, RecordNotFoundException, ValidationException
from .docs import DELETE_RESPONSES, DELETE_SUMMARY
from ... import post_router

@post_router.delete("/{id:int}",
    response_model=APIResponse[int],
    operation_id="public_post_delete",
    summary=DELETE_SUMMARY,
    responses=DELETE_RESPONSES
)
async def post_delete(
    id: int = Path(..., description="Campo id de la tabla post"),
    token: AccessToken = Depends(requires_permissions("delete", "post")),
) -> APIResponse[int]:
    """
    Elimina un Post por su primary key.
    """

    with username_context(token.preferred_username):
        existing = await PostAsyncDAO.find(
            id=id,
        )

        if existing is None:
            raise RecordNotFoundException("Post")

        result = await PostAsyncDAO.delete(
            id=id,
        )

        if result == 0:
            raise RecordNotFoundException("Post")

        return APIResponse.success(
            data=result,
            message="Post eliminado exitosamente"
        )
