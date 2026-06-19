from fastapi import Depends
from ......auth import requires_permissions, AccessToken
from ...._shared import username_context, get_model_by_name

from ...database import UsuarioAsyncDAO, UsuarioUpdate
from api.resources import APIResponse
from .docs import UPDATE_MANY_RESPONSES, UPDATE_MANY_SUMMARY
from ... import usuario_router

@usuario_router.patch("",
    response_model=APIResponse[int],
    operation_id="public_usuario_update_many",
    summary=UPDATE_MANY_SUMMARY,
    responses=UPDATE_MANY_RESPONSES
)
async def usuario_update_many(
    payload: UsuarioUpdate,
    token: AccessToken = Depends(requires_permissions("update", "usuario")),
) -> APIResponse[int]:
    """
    Actualiza múltiples Usuarios.
    """
    with username_context(token.preferred_username):
        result = await UsuarioAsyncDAO.update_many(
            payload,
        )

        message = f"{result} Usuarios actualizados exitosamente" if result > 0 else "No se encontraron registros que coincidan con los criterios"

        return APIResponse.success(
            data=result,
            message=message
        )
