from fastapi import Query, Depends
from typing import Optional, List

from ......auth import requires_permissions, AccessToken
from ...._shared import username_context, get_model_by_name

from ...database import UserStatsAsyncDAO
from api.resources import APIResponse
from .docs import EXISTS_RESPONSES, EXISTS_SUMMARY
from ... import user_stats_router

@user_stats_router.get("/exists",
    response_model=APIResponse[bool],
    operation_id="public_user_stats_exists",
    summary=EXISTS_SUMMARY,
    responses=EXISTS_RESPONSES
)
async def user_stats_exists(
    user_id: Optional[int] = Query(None, description="Filtrar por user_id. Campo user_id de la tabla user_stats"),
    in_user_id: Optional[List[int]] = Query(None, description="Filtrar por múltiples valores de user_id"),
    min_user_id: Optional[int] = Query(None, description="Valor mínimo para user_id (incluido)"),
    max_user_id: Optional[int] = Query(None, description="Valor máximo para user_id (incluido)"),
    user_name: Optional[str] = Query(None, description="Filtrar por user_name. Campo user_name de la tabla user_stats"),
    in_user_name: Optional[List[str]] = Query(None, description="Filtrar por múltiples valores de user_name"),
    post_count: Optional[int] = Query(None, description="Filtrar por post_count. Campo post_count de la tabla user_stats"),
    in_post_count: Optional[List[int]] = Query(None, description="Filtrar por múltiples valores de post_count"),
    min_post_count: Optional[int] = Query(None, description="Valor mínimo para post_count (incluido)"),
    max_post_count: Optional[int] = Query(None, description="Valor máximo para post_count (incluido)"),
    token: AccessToken = Depends(requires_permissions("read", "user_stats")),
) -> APIResponse[bool]:
    """
    Verifica si existe al menos un user_stats que coincida con los filtros.
    """
    with username_context(token.preferred_username):
        result = await UserStatsAsyncDAO.exists(
            user_id=user_id,
            in_user_id=in_user_id,
            min_user_id=min_user_id,
            max_user_id=max_user_id,
            user_name=user_name,
            in_user_name=in_user_name,
            post_count=post_count,
            in_post_count=in_post_count,
            min_post_count=min_post_count,
            max_post_count=max_post_count,
        )

        return APIResponse.success(
            data=result,
            message="Verificación realizada exitosamente"
        )
