from fastapi import Depends
from ......auth import requires_permissions, AccessToken
from ...._shared import username_context, get_model_by_name

from ...database import UsuarioAsyncDAO, UsuarioRead, UsuarioCreate
from api.resources import APIResponse
from .docs import CREATE_RESPONSES, CREATE_SUMMARY
from ... import usuario_router

@usuario_router.post("",
    response_model=APIResponse[UsuarioRead],
    status_code=201,
    operation_id="public_usuario_create",
    summary=CREATE_SUMMARY,
    responses=CREATE_RESPONSES
)
async def usuario_create(
    usuario: UsuarioCreate,
    token: AccessToken = Depends(requires_permissions("create", "usuario")),
) -> APIResponse[UsuarioRead]:
    """
    Crea un nuevo Usuario.
    """
    with username_context(token.preferred_username):
        result = await UsuarioAsyncDAO.create(
            usuario,
        )

        return APIResponse.success(
            data=result,
            message="Usuario creado exitosamente"
        )
