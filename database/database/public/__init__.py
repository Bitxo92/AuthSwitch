# Este archivo ha sido generado automáticamente por tai-sql
# No modifiques este archivo directamente

from __future__ import annotations
from typing import Optional

from ._session import (
    SyncSessionManager,
    sync_session_manager,
    AsyncSessionManager,
    async_session_manager,
)
from .usuario.model import Usuario
from .usuario.dtos import *
from .usuario.dao_sync import UsuarioSyncDAO
from .usuario.dao_async import UsuarioAsyncDAO
from .post.model import Post
from .post.dtos import *
from .post.dao_sync import PostSyncDAO
from .post.dao_async import PostAsyncDAO
from .comment.model import Comment
from .comment.dtos import *
from .comment.dao_sync import CommentSyncDAO
from .comment.dao_async import CommentAsyncDAO
from .user_stats.model import UserStats
from .user_stats.dtos import *
from .user_stats.dao_sync import UserStatsSyncDAO
from .user_stats.dao_async import UserStatsAsyncDAO
from ._shared import (
    AggregationResult,
    AggRow,
    AggRequest,
    AggField,
    GroupByField,
    DatetimeTrunc,
    AggOrderBy,
    RLS,
    EnumModel,
    set_username,
    get_username,
    username_context,
)

_rebuild_ns = {k: v for k, v in globals().items()}
UsuarioRead.model_rebuild(_types_namespace=_rebuild_ns)
UsuarioCreate.model_rebuild(_types_namespace=_rebuild_ns)
UsuarioUpdateNested.model_rebuild(_types_namespace=_rebuild_ns)
UsuarioUpdateValues.model_rebuild(_types_namespace=_rebuild_ns)
UsuarioPostsNestedUpdate.model_rebuild(_types_namespace=_rebuild_ns)
PostRead.model_rebuild(_types_namespace=_rebuild_ns)
PostCreate.model_rebuild(_types_namespace=_rebuild_ns)
PostUpdateNested.model_rebuild(_types_namespace=_rebuild_ns)
PostUpdateValues.model_rebuild(_types_namespace=_rebuild_ns)
PostCommentsNestedUpdate.model_rebuild(_types_namespace=_rebuild_ns)
CommentRead.model_rebuild(_types_namespace=_rebuild_ns)
CommentCreate.model_rebuild(_types_namespace=_rebuild_ns)
CommentUpdateNested.model_rebuild(_types_namespace=_rebuild_ns)
CommentUpdateValues.model_rebuild(_types_namespace=_rebuild_ns)


class PublicSyncAPI:
    """
    API principal para operaciones de base de datos síncronas.
    
    Proporciona acceso centralizado a todos los DAOs síncronos.
    Los DAOs son stateless (classmethods), esta clase actúa como namespace.
    """

    _instance: Optional[PublicSyncAPI] = None

    def __new__(cls) -> PublicSyncAPI:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @property
    def session_manager(self) -> SyncSessionManager:
        return sync_session_manager
    
    @property
    def usuario(self):
        """Acceso a UsuarioSyncDAO (classmethods)"""
        return UsuarioSyncDAO

    @property
    def post(self):
        """Acceso a PostSyncDAO (classmethods)"""
        return PostSyncDAO

    @property
    def comment(self):
        """Acceso a CommentSyncDAO (classmethods)"""
        return CommentSyncDAO

    @property
    def user_stats(self):
        """Acceso a UserStatsSyncDAO (classmethods)"""
        return UserStatsSyncDAO

    @property
    def content_type(self):
        return EnumModel(name="content_type", values=['text', 'image', 'video'])


class PublicAsyncAPI:
    """
    API principal para operaciones de base de datos asíncronas.
    
    Proporciona acceso centralizado a todos los DAOs asíncronos.
    Los DAOs son stateless (classmethods), esta clase actúa como namespace.
    """

    _instance: Optional[PublicAsyncAPI] = None

    def __new__(cls) -> PublicAsyncAPI:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @property
    def session_manager(self) -> AsyncSessionManager:
        return async_session_manager
    
    @property
    def usuario(self):
        """Acceso a UsuarioAsyncDAO (classmethods)"""
        return UsuarioAsyncDAO

    @property
    def post(self):
        """Acceso a PostAsyncDAO (classmethods)"""
        return PostAsyncDAO

    @property
    def comment(self):
        """Acceso a CommentAsyncDAO (classmethods)"""
        return CommentAsyncDAO

    @property
    def user_stats(self):
        """Acceso a UserStatsAsyncDAO (classmethods)"""
        return UserStatsAsyncDAO

    @property
    def content_type(self):
        return EnumModel(name="content_type", values=['text', 'image', 'video'])


# Instancias globales
public_sync_api = PublicSyncAPI()
public_async_api = PublicAsyncAPI()


# Exportar
__all__ = [
    'PublicSyncAPI',
    'public_sync_api',
    'SyncSessionManager',
    'sync_session_manager',
    'PublicAsyncAPI',
    'public_async_api',
    'AsyncSessionManager',
    'async_session_manager',
    'set_username',
    'get_username',
    'username_context',
    'AggregationResult',
    'AggRow',
    'AggRequest',
    'AggField',
    'GroupByField',
    'DatetimeTrunc',
    'AggOrderBy',
    'RLS',
    'EnumModel',
    'Usuario',
    'UsuarioSyncDAO',
    'UsuarioAsyncDAO',
    'UsuarioRead',
    'UsuarioFilter',
    'UsuarioCreate',
    'UsuarioUpdate',
    'UsuarioUpdateValues',
    'UsuarioUpdateNested',
    'Post',
    'PostSyncDAO',
    'PostAsyncDAO',
    'PostRead',
    'PostFilter',
    'PostCreate',
    'PostUpdate',
    'PostUpdateValues',
    'PostUpdateNested',
    'Comment',
    'CommentSyncDAO',
    'CommentAsyncDAO',
    'CommentRead',
    'CommentFilter',
    'CommentCreate',
    'CommentUpdate',
    'CommentUpdateValues',
    'CommentUpdateNested',
    'UserStats',
    'UserStatsSyncDAO',
    'UserStatsAsyncDAO',
    'UserStatsRead',
    'UserStatsFilter',
]