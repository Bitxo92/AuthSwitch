# Este archivo ha sido generado automáticamente por tai-sql
# No modifiques este archivo directamente


from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from .._base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sqlalchemy import BigInteger, ForeignKeyConstraint


if TYPE_CHECKING:
    from ..role.model import Role
    from ..permission.model import Permission



class RolePermission(Base):
    """SQLAlchemy model for ``auth.role_permission``."""

    __tablename__ = "role_permission"


    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    role_name: Mapped[str]
    permission_name: Mapped[str]
    realm_name: Mapped[str]



    role: Mapped[Role] = relationship(back_populates="role_permissions", foreign_keys="[RolePermission.role_name, RolePermission.realm_name]")
    permission: Mapped[Permission] = relationship(back_populates="role_permissions", foreign_keys="[RolePermission.permission_name, RolePermission.realm_name]")

    __table_args__ = (
        ForeignKeyConstraint(
            ['role_name', 'realm_name'],
            ['auth.role.name', 'auth.role.realm_name'],
            ondelete='CASCADE',
            onupdate='CASCADE',
        ),
        ForeignKeyConstraint(
            ['permission_name', 'realm_name'],
            ['auth.permission.name', 'auth.permission.realm_name'],
            ondelete='CASCADE',
            onupdate='CASCADE',
        ),
        {'schema': 'auth'},
    )


