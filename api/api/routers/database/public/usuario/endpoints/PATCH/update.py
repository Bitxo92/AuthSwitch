from fastapi import Path, Body, Depends
from ......auth import requires_permissions, AccessToken
from ...._shared import username_context, get_model_by_name

from ...database import UsuarioAsyncDAO, UsuarioUpdateValues
from api.resources import APIResponse, RecordNotFoundException, ValidationException
from .docs import UPDATE_RESPONSES, UPDATE_SUMMARY, UPDATE_DESCRIPTION
from ... import usuario_router

@usuario_router.patch("/{id:int}",
    response_model=APIResponse[int],
    operation_id="public_usuario_update",
    summary=UPDATE_SUMMARY,
    description=UPDATE_DESCRIPTION,
    responses=UPDATE_RESPONSES
)
async def usuario_update(
    id: int = Path(..., description="Campo id de la tabla usuario"),
    values: UsuarioUpdateValues = Body(...),
    token: AccessToken = Depends(requires_permissions("update", "usuario")),
) -> APIResponse[int]:
    """
    Actualiza un Usuario específico.
    """
    if id <= 0:
        raise ValidationException("id debe ser mayor a 0", "id")

    with username_context(token.preferred_username):
        existing = await UsuarioAsyncDAO.find(
            id=id,
        )

        if existing is None:
            raise RecordNotFoundException("Usuario")

        result = await UsuarioAsyncDAO.update(
            id=id,
            updated_values=values,
        )

        if result == 0:
            raise RecordNotFoundException("Usuario")

        return APIResponse.success(
            data=result,
            message="Usuario actualizado exitosamente"
        )
