from fastapi import Query, Depends
from typing import Optional, List
from datetime import datetime

from ......auth import requires_permissions, AccessToken
from ...._shared import username_context, get_model_by_name

from ...database import PostAsyncDAO
from api.resources import APIResponse
from .docs import EXISTS_RESPONSES, EXISTS_SUMMARY
from ... import post_router

@post_router.get("/exists",
    response_model=APIResponse[bool],
    operation_id="public_post_exists",
    summary=EXISTS_SUMMARY,
    responses=EXISTS_RESPONSES
)
async def post_exists(
    title: Optional[str] = Query(None, description="Filtrar por title. Campo title de la tabla post"),
    in_title: Optional[List[str]] = Query(None, description="Filtrar por múltiples valores de title"),
    content: Optional[str] = Query(None, description="Filtrar por content. Contenido del post"),
    in_content: Optional[List[str]] = Query(None, description="Filtrar por múltiples valores de content"),
    content_type: Optional[str] = Query(None, description="Filtrar por content_type. Campo content_type de la tabla post"),
    in_content_type: Optional[List[str]] = Query(None, description="Filtrar por múltiples valores de content_type"),
    min_timestamp: Optional[datetime] = Query(None, description="Valor mínimo para timestamp (incluido)"),
    max_timestamp: Optional[datetime] = Query(None, description="Valor máximo para timestamp (incluido)"),
    author_id: Optional[int] = Query(None, description="Filtrar por author_id"),
    in_author_id: Optional[List[int]] = Query(None, description="Filtrar por múltiples valores de author_id"),
    token: AccessToken = Depends(requires_permissions("read", "post")),
) -> APIResponse[bool]:
    """
    Verifica si existe al menos un post que coincida con los filtros.
    """
    with username_context(token.preferred_username):
        result = await PostAsyncDAO.exists(
            title=title,
            in_title=in_title,
            content=content,
            in_content=in_content,
            content_type=content_type,
            in_content_type=in_content_type,
            min_timestamp=min_timestamp,
            max_timestamp=max_timestamp,
            author_id=author_id,
            in_author_id=in_author_id,
        )

        return APIResponse.success(
            data=result,
            message="Verificación realizada exitosamente"
        )
