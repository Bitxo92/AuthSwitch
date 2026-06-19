from fastapi import Path, Depends
from ......auth import requires_permissions, AccessToken
from ...._shared import username_context, get_model_by_name

from ...database import UsuarioAsyncDAO
from api.resources import APIResponse, RecordNotFoundException, ValidationException
from .docs import DELETE_RESPONSES, DELETE_SUMMARY
from ... import usuario_router

@usuario_router.delete("/{id:int}",
    response_model=APIResponse[int],
    operation_id="public_usuario_delete",
    summary=DELETE_SUMMARY,
    responses=DELETE_RESPONSES
)
async def usuario_delete(
    id: int = Path(..., description="Campo id de la tabla usuario"),
    token: AccessToken = Depends(requires_permissions("delete", "usuario")),
) -> APIResponse[int]:
    """
    Elimina un Usuario por su primary key.
    """
    if id <= 0:
        raise ValidationException("id debe ser mayor a 0", "id")

    with username_context(token.preferred_username):
        existing = await UsuarioAsyncDAO.find(
            id=id,
        )

        if existing is None:
            raise RecordNotFoundException("Usuario")

        result = await UsuarioAsyncDAO.delete(
            id=id,
        )

        if result == 0:
            raise RecordNotFoundException("Usuario")

        return APIResponse.success(
            data=result,
            message="Usuario eliminado exitosamente"
        )
