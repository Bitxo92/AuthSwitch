from typing import List
from api.resources import APIResponse
from .docs import PERMISSION_TYPE_RESPONSES
from ... import enumerations_router


@enumerations_router.get("/permission-type",
    tags=["Enumeraciones"],
    response_model=APIResponse[List[str]],
    responses=PERMISSION_TYPE_RESPONSES
)
async def get_permission_type_enumeration() -> APIResponse[List[str]]:
    """
    Obtiene los valores de la enumeración permission_type.
    """
    return APIResponse.success(
        data=["api", "app"],
        message="Enumeración permission_type obtenida exitosamente"
    )