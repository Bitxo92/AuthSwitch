# Este archivo ha sido generado automáticamente por tai-sql
# No modifiques este archivo directamente


from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from ..._base import Base, encrypt_value, decrypt_value
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property


if TYPE_CHECKING:
    from ...post.database.model import Post



class Usuario(Base):
    """SQLAlchemy model for ``public.usuario``."""

    __tablename__ = "usuario"

    def __init__(self, **kwargs):
        if 'pwd' in kwargs:
            pwd_value = kwargs.pop('pwd')
            self.pwd = pwd_value
        super().__init__(**kwargs)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    _pwd: Mapped[str] = mapped_column(name="pwd")
    email: Mapped[Optional[str]]
    last_post_date: Mapped[Optional[datetime]]


    @hybrid_property
    def pwd(self) -> str:
        if self._pwd is None:
            return None
        return decrypt_value(self._pwd)

    @pwd.setter
    def pwd(self, value: str):
        if value is None:
            self._pwd = None
        else:
            self._pwd = encrypt_value(str(value))


    posts: Mapped[List[Post]] = relationship(back_populates="author", foreign_keys="[Post.author_id]", passive_deletes="all")

    __table_args__ = {'schema': 'public'}


