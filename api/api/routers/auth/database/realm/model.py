# Este archivo ha sido generado automáticamente por tai-sql
# No modifiques este archivo directamente


from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from .._base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship



if TYPE_CHECKING:
    from ..user.model import User
    from ..role.model import Role
    from ..permission.model import Permission



class Realm(Base):
    """SQLAlchemy model for ``auth.realm``."""

    __tablename__ = "realm"


    name: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[Optional[str]]



    users: Mapped[List[User]] = relationship(back_populates="realm", foreign_keys="[User.realm_name]", passive_deletes="all")
    roles: Mapped[List[Role]] = relationship(back_populates="realm", foreign_keys="[Role.realm_name]", passive_deletes="all")
    permissions: Mapped[List[Permission]] = relationship(back_populates="realm", foreign_keys="[Permission.realm_name]", passive_deletes="all")

    __table_args__ = {'schema': 'auth'}


