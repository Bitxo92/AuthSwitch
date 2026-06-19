from fastapi import APIRouter

user_stats_router = APIRouter(
    prefix="/user-stats",
    tags=["UserStats"]
)

from .endpoints.GET import find_many
from .endpoints.GET import count
from .endpoints.GET import exists
from .endpoints.GET import sum
from .endpoints.GET import mean
from .endpoints.GET import max
from .endpoints.GET import min
from .endpoints.POST import agg
