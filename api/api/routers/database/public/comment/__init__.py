from fastapi import APIRouter

comment_router = APIRouter(
    prefix="/comment",
    tags=["Comment"]
)

from .endpoints.GET import find_many
from .endpoints.GET import count
from .endpoints.GET import exists
from .endpoints.GET import sum
from .endpoints.GET import mean
from .endpoints.GET import max
from .endpoints.GET import min
from .endpoints.GET import find
from .endpoints.POST import agg
from .endpoints.POST import create
from .endpoints.PATCH import update
from .endpoints.PATCH import update_many
from .endpoints.DELETE import delete
from .endpoints.DELETE import delete_many
