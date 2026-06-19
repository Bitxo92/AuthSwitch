from typing import List
from api.resources import APIResponse
from .docs import CONTENT_TYPE_RESPONSES
from ... import enumerations_router


@enumerations_router.get("/content-type",
    tags=["Enumeraciones"],
    response_model=APIResponse[List[str]],
    responses=CONTENT_TYPE_RESPONSES
)
async def get_content_type_enumeration() -> APIResponse[List[str]]:
    """
    Obtiene los valores de la enumeración content_type.
    """
    return APIResponse.success(
        data=["text", "image", "video"],
        message="Enumeración content_type obtenida exitosamente"
    )