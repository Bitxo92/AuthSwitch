from fastapi import Path, Body, Depends
from ......auth import requires_permissions, AccessToken
from ...._shared import username_context, get_model_by_name

from ...database import CommentAsyncDAO, CommentUpdateValues
from api.resources import APIResponse, RecordNotFoundException, ValidationException
from .docs import UPDATE_RESPONSES, UPDATE_SUMMARY, UPDATE_DESCRIPTION
from ... import comment_router

@comment_router.patch("/{id:int}",
    response_model=APIResponse[int],
    operation_id="public_comment_update",
    summary=UPDATE_SUMMARY,
    description=UPDATE_DESCRIPTION,
    responses=UPDATE_RESPONSES
)
async def comment_update(
    id: int = Path(..., description="Campo id de la tabla comment"),
    values: CommentUpdateValues = Body(...),
    token: AccessToken = Depends(requires_permissions("update", "comment")),
) -> APIResponse[int]:
    """
    Actualiza un Comment específico.
    """
    if id <= 0:
        raise ValidationException("id debe ser mayor a 0", "id")

    with username_context(token.preferred_username):
        existing = await CommentAsyncDAO.find(
            id=id,
        )

        if existing is None:
            raise RecordNotFoundException("Comment")

        result = await CommentAsyncDAO.update(
            id=id,
            updated_values=values,
        )

        if result == 0:
            raise RecordNotFoundException("Comment")

        return APIResponse.success(
            data=result,
            message="Comment actualizado exitosamente"
        )
