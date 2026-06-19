# Este archivo ha sido generado automáticamente por tai-sql
# No modifiques este archivo directamente


from __future__ import annotations
from typing import Optional, List
from .._base import Base
from sqlalchemy.orm import Mapped, mapped_column






class RowLevelSecurity(Base):
    """SQLAlchemy model for ``auth.row_level_security``."""

    __tablename__ = "row_level_security"


    realm_name: Mapped[str] = mapped_column(primary_key=True)
    schema_name: Mapped[str] = mapped_column(primary_key=True)
    table_name: Mapped[str] = mapped_column(primary_key=True)
    column_name: Mapped[str] = mapped_column(primary_key=True)




    __table_args__ = {'schema': 'auth'}


