from fastapi import APIRouter

enumerations_router = APIRouter(
    prefix="/enums",
    tags=["Enumeraciones"]
)

from .endpoints.GET import permission_type
from .endpoints.GET import content_type
