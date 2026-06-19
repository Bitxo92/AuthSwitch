from fastapi import Query, Path, Depends
from typing import Optional, List
from ......auth import requires_permissions, AccessToken
from ...._shared import username_context, get_model_by_name

from ...database import PostAsyncDAO, PostRead, RLS
from api.resources import APIResponse, RecordNotFoundException, ValidationException
from .docs import FIND_RESPONSES, FIND_SUMMARY, FIND_DESCRIPTION
from ... import post_router

@post_router.get("/{id:int}",
    response_model=APIResponse[PostRead],
    response_description="Registro único de post obtenido exitosamente",
    operation_id="public_post_find",
    summary=FIND_SUMMARY,
    description=FIND_DESCRIPTION,
    responses=FIND_RESPONSES
)
async def post_find(
    id: int = Path(..., description="Campo id de la tabla post"),
    includes: List[str] = Query(None, description="Lista de relaciones a incluir en la respuesta para obtener datos relacionados. Especifica los nombres de las relaciones que deseas expandir"),
    token: AccessToken = Depends(requires_permissions("read", "post")),
) -> APIResponse[PostRead]:
    rls = [
        RLS(
            target_model=model,
            target_column=col_name,
            values=conditions
        ) for schema_name, table_dict in (token.rls or {}).items()
        for table_name, col_dict in (table_dict or {}).items()
        for col_name, conditions in (col_dict or {}).items()
        if (
            (model := get_model_by_name(f"{schema_name}.{table_name}")) is not None 
        )
    ]

    with username_context(token.preferred_username):
        result = await PostAsyncDAO.find(
            id=id,
            includes=includes,
            rls=rls
        )

        if result is None:
            raise RecordNotFoundException("Post")

        return APIResponse.success(
            data=result,
            message="Post obtenido exitosamente"
        )
