# Este archivo ha sido generado automáticamente por tai-sql
# No modifiques este archivo directamente


from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from .._base import Base, encrypt_value, decrypt_value
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Dict, Any

from sqlalchemy import ForeignKeyConstraint, JSON
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import event


if TYPE_CHECKING:
    from ..realm.model import Realm
    from ..user_role.model import UserRole



class User(Base):
    """SQLAlchemy model for ``auth.user``."""

    __tablename__ = "user"

    def __init__(self, **kwargs):
        if 'password' in kwargs:
            password_value = kwargs.pop('password')
            self.password = password_value
        kwargs.pop('full_name', None)
        super().__init__(**kwargs)
        self._recompute_full_name()

    username: Mapped[str] = mapped_column(primary_key=True)
    realm_name: Mapped[str] = mapped_column(primary_key=True)
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    _password: Mapped[str] = mapped_column(name="password")
    email: Mapped[Optional[str]]
    is_active: Mapped[bool] = mapped_column(default=True)
    session_id: Mapped[Optional[str]]
    password_expiration: Mapped[Optional[datetime]]
    attributes: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    _full_name: Mapped[str] = mapped_column(name="full_name")


    @hybrid_property
    def password(self) -> str:
        if self._password is None:
            return None
        return decrypt_value(self._password)

    @password.setter
    def password(self, value: str):
        if value is None:
            self._password = None
        else:
            self._password = encrypt_value(str(value))


    @hybrid_property
    def full_name(self) -> str:
        return self._full_name

    @full_name.setter
    def full_name(self, value: str):
        self._full_name = value

    @full_name.expression
    def full_name(cls):
        return cls._full_name

    def _recompute_full_name(self):
        """Recompute calculated column ``full_name``."""
        self._full_name = f"{self.first_name or ''} {self.last_name or ''}".strip() if self.first_name or self.last_name else None

    realm: Mapped[Realm] = relationship(back_populates="users", foreign_keys="[User.realm_name]")
    user_roles: Mapped[List[UserRole]] = relationship(back_populates="user", foreign_keys="[UserRole.user_name, UserRole.realm_name]", passive_deletes="all")

    __table_args__ = (
        ForeignKeyConstraint(
            ['realm_name'],
            ['auth.realm.name'],
            ondelete='CASCADE',
            onupdate='CASCADE',
        ),
        {'schema': 'auth'},
    )



@event.listens_for(User, 'before_insert')
@event.listens_for(User, 'before_update')
def _recompute_user_calculated(mapper, connection, target: User):
    """Recompute all calculated columns before insert/update."""
    target._recompute_full_name()
