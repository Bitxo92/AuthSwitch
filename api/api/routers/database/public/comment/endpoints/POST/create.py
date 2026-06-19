from fastapi import Depends
from ......auth import requires_permissions, AccessToken
from ...._shared import username_context, get_model_by_name

from ...database import CommentAsyncDAO, CommentRead, CommentCreate
from api.resources import APIResponse
from .docs import CREATE_RESPONSES, CREATE_SUMMARY
from ... import comment_router

@comment_router.post("",
    response_model=APIResponse[CommentRead],
    status_code=201,
    operation_id="public_comment_create",
    summary=CREATE_SUMMARY,
    responses=CREATE_RESPONSES
)
async def comment_create(
    comment: CommentCreate,
    token: AccessToken = Depends(requires_permissions("create", "comment")),
) -> APIResponse[CommentRead]:
    """
    Crea un nuevo Comment.
    """
    with username_context(token.preferred_username):
        result = await CommentAsyncDAO.create(
            comment,
        )

        return APIResponse.success(
            data=result,
            message="Comment creado exitosamente"
        )
