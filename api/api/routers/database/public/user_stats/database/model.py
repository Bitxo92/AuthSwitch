# Este archivo ha sido generado automáticamente por tai-sql
# No modifiques este archivo directamente


from __future__ import annotations
from typing import Optional, List
from ..._base import Base
from sqlalchemy.orm import Mapped, mapped_column






class UserStats(Base):
    """SQLAlchemy model for ``public.user_stats``."""

    __tablename__ = "user_stats"
    is_view = True


    user_id: Mapped[int]
    user_name: Mapped[str]
    post_count: Mapped[int]




    __table_args__ = {'schema': 'public'}

    __mapper_args__ = {'primary_key': [
        'user_id',
        'user_name',
        'post_count',
    ]}

