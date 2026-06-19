# Este archivo ha sido generado automáticamente por tai-sql
# No modifiques este archivo directamente


from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from .._base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from sqlalchemy import BigInteger, ForeignKeyConstraint


if TYPE_CHECKING:
    from ..comment.model import Comment
    from ..usuario.model import Usuario



class Post(Base):
    """SQLAlchemy model for ``public.post``."""

    __tablename__ = "post"


    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(default="Post Title")
    content: Mapped[str]
    content_type: Mapped[str] = mapped_column(default="text")
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now)
    author_id: Mapped[int]



    comments: Mapped[List[Comment]] = relationship(back_populates="post", foreign_keys="[Comment.post_id]", passive_deletes="all")
    author: Mapped[Usuario] = relationship(back_populates="posts", foreign_keys="[Post.author_id]")

    __table_args__ = (
        ForeignKeyConstraint(
            ['author_id'],
            ['public.usuario.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
        ),
        {'schema': 'public'},
    )


