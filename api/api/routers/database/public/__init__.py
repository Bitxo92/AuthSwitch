from fastapi import APIRouter
from .usuario import usuario_router
from .post import post_router
from .comment import comment_router
from .user_stats import user_stats_router
from ._enums import enumerations_router

public_router = APIRouter(prefix="/public")

public_router.include_router(usuario_router)
public_router.include_router(post_router)
public_router.include_router(comment_router)
public_router.include_router(user_stats_router)
public_router.include_router(enumerations_router)
