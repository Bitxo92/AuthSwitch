# Este archivo ha sido generado automáticamente por tai-sql
# No modifiques este archivo directamente


from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from .._base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Dict, Any

from sqlalchemy import ForeignKeyConstraint, JSON


if TYPE_CHECKING:
    from ..realm.model import Realm
    from ..role_permission.model import RolePermission
    from ..user_role.model import UserRole



class Role(Base):
    """SQLAlchemy model for ``auth.role``."""

    __tablename__ = "role"


    name: Mapped[str] = mapped_column(primary_key=True)
    realm_name: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[Optional[str]]
    attributes: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    parent_role_name: Mapped[Optional[str]]



    realm: Mapped[Realm] = relationship(back_populates="roles", foreign_keys="[Role.realm_name]")
    role_permissions: Mapped[List[RolePermission]] = relationship(back_populates="role", foreign_keys="[RolePermission.role_name, RolePermission.realm_name]", passive_deletes="all")
    user_roles: Mapped[List[UserRole]] = relationship(back_populates="role", foreign_keys="[UserRole.role_name, UserRole.realm_name]", passive_deletes="all")

    __table_args__ = (
        ForeignKeyConstraint(
            ['realm_name'],
            ['auth.realm.name'],
            ondelete='CASCADE',
            onupdate='CASCADE',
        ),
        {'schema': 'auth'},
    )


