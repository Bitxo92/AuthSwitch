# Este archivo ha sido generado automáticamente por tai-sql
# No modifiques este archivo directamente


from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from ..._base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sqlalchemy import BigInteger, ForeignKeyConstraint


if TYPE_CHECKING:
    from ...post.database.model import Post



class Comment(Base):
    """SQLAlchemy model for ``public.comment``."""

    __tablename__ = "comment"


    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[str]
    post_id: Mapped[int] = mapped_column(BigInteger)



    post: Mapped[Post] = relationship(back_populates="comments", foreign_keys="[Comment.post_id]")

    __table_args__ = (
        ForeignKeyConstraint(
            ['post_id'],
            ['public.post.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
        ),
        {'schema': 'public'},
    )


