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



class Permission(Base):
    """SQLAlchemy model for ``auth.permission``."""

    __tablename__ = "permission"


    name: Mapped[str] = mapped_column(primary_key=True)
    realm_name: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[Optional[str]]
    type: Mapped[str]
    attributes: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)



    realm: Mapped[Realm] = relationship(back_populates="permissions", foreign_keys="[Permission.realm_name]")
    role_permissions: Mapped[List[RolePermission]] = relationship(back_populates="permission", foreign_keys="[RolePermission.permission_name, RolePermission.realm_name]", passive_deletes="all")

    __table_args__ = (
        ForeignKeyConstraint(
            ['realm_name'],
            ['auth.realm.name'],
            ondelete='CASCADE',
            onupdate='CASCADE',
        ),
        {'schema': 'auth'},
    )


