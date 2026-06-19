from fastapi import Depends
from ......auth import requires_permissions, AccessToken
from ...._shared import username_context, get_model_by_name

from ...database import PostAsyncDAO, PostRead, PostCreate
from api.resources import APIResponse
from .docs import CREATE_RESPONSES, CREATE_SUMMARY
from ... import post_router

@post_router.post("",
    response_model=APIResponse[PostRead],
    status_code=201,
    operation_id="public_post_create",
    summary=CREATE_SUMMARY,
    responses=CREATE_RESPONSES
)
async def post_create(
    post: PostCreate,
    token: AccessToken = Depends(requires_permissions("create", "post")),
) -> APIResponse[PostRead]:
    """
    Crea un nuevo Post.
    """
    with username_context(token.preferred_username):
        result = await PostAsyncDAO.create(
            post,
        )

        return APIResponse.success(
            data=result,
            message="Post creado exitosamente"
        )
