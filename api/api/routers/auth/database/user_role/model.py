# Este archivo ha sido generado automáticamente por tai-sql
# No modifiques este archivo directamente


from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from .._base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sqlalchemy import BigInteger, ForeignKeyConstraint


if TYPE_CHECKING:
    from ..user.model import User
    from ..role.model import Role



class UserRole(Base):
    """SQLAlchemy model for ``auth.user_role``."""

    __tablename__ = "user_role"


    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_name: Mapped[str]
    role_name: Mapped[str]
    realm_name: Mapped[str]



    user: Mapped[User] = relationship(back_populates="user_roles", foreign_keys="[UserRole.user_name, UserRole.realm_name]")
    role: Mapped[Role] = relationship(back_populates="user_roles", foreign_keys="[UserRole.role_name, UserRole.realm_name]")

    __table_args__ = (
        ForeignKeyConstraint(
            ['user_name', 'realm_name'],
            ['auth.user.username', 'auth.user.realm_name'],
            ondelete='CASCADE',
            onupdate='CASCADE',
        ),
        ForeignKeyConstraint(
            ['role_name', 'realm_name'],
            ['auth.role.name', 'auth.role.realm_name'],
            ondelete='CASCADE',
            onupdate='CASCADE',
        ),
        {'schema': 'auth'},
    )


