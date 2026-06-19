# Este archivo ha sido generado automáticamente por tai-sql
# No modifiques este archivo directamente

from __future__ import annotations
from typing import (
    List,
    Optional,
    Dict,
    Any,
    TYPE_CHECKING,
)
from sqlalchemy.orm.query import Query
from pydantic import (
    Field,
    ConfigDict,
)

from .model import Realm
from .._shared import (
    PrettyModel,
    get_username,
    should_include_relation,
    get_nested_includes
)

if TYPE_CHECKING:
    from pandas import DataFrame, Series  # type: ignore[import-untyped]



class RealmRead(PrettyModel):
    """DTO de lectura para Realm."""
    name: str = Field(
        description="Nombre único del realm",
    )
    description: Optional[str] = Field(
        description="Descripción del realm",
    )

    users: Optional[List[UserRead]] = Field(default=None)
    roles: Optional[List[RoleRead]] = Field(default=None)
    permissions: Optional[List[PermissionRead]] = Field(default=None)



    model_config = ConfigDict(
        # Performance optimizations
        arbitrary_types_allowed=False,  # Más rápido al validar tipos estrictos
        use_enum_values=True,
        validate_assignment=True,  # Valida en cada asignación
        frozen=False,  # Si True, hace el objeto inmutable
        str_strip_whitespace=False,  # No procesa strings automáticamente
        validate_default=False,  # No valida valores por defecto
        extra="forbid",  # Más rápido que "allow" o "ignore"
        # Configuraciones adicionales de v2
        populate_by_name=True,  # Permite usar alias y nombres originales
        use_attribute_docstrings=True,  # Usa docstrings como descripciones
        validate_call=True,  # Valida llamadas a métodos
    )
    
    @classmethod
    def from_instance(
        cls,
        instance: Realm,
        includes: Optional[List[str]] = None,
        max_depth: int = 5,
        distance_score: Optional[float] = None
    ) -> RealmRead:
        dto_data = {
            'name': instance.name,
            'description': instance.description,
        }

        if includes is not None and max_depth > 0:
            if should_include_relation('users', includes):
                nested_includes = get_nested_includes('users', includes)
                if hasattr(instance, 'users') and instance.users is not None:
                    dto_data['users'] = [
                        UserRead.from_instance(reg, nested_includes, max_depth - 1) 
                        for reg in instance.users
                    ]
            if should_include_relation('roles', includes):
                nested_includes = get_nested_includes('roles', includes)
                if hasattr(instance, 'roles') and instance.roles is not None:
                    dto_data['roles'] = [
                        RoleRead.from_instance(reg, nested_includes, max_depth - 1) 
                        for reg in instance.roles
                    ]
            if should_include_relation('permissions', includes):
                nested_includes = get_nested_includes('permissions', includes)
                if hasattr(instance, 'permissions') and instance.permissions is not None:
                    dto_data['permissions'] = [
                        PermissionRead.from_instance(reg, nested_includes, max_depth - 1) 
                        for reg in instance.permissions
                    ]
        return cls(**dto_data)

    @classmethod
    def from_created_instance(cls, instance: Realm, included: set[str], excluded: str=None) -> RealmRead:
        dto_data = {
            'name': instance.name,
            'description': instance.description,
        }
        if 'users' in included and 'users' != excluded:
            dto_data['users'] = [
                UserRead.from_created_instance(reg, included, 'realm') 
                for reg in instance.users
            ]
        if 'roles' in included and 'roles' != excluded:
            dto_data['roles'] = [
                RoleRead.from_created_instance(reg, included, 'realm') 
                for reg in instance.roles
            ]
        if 'permissions' in included and 'permissions' != excluded:
            dto_data['permissions'] = [
                PermissionRead.from_created_instance(reg, included, 'realm') 
                for reg in instance.permissions
            ]
        return cls(**dto_data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> RealmRead:
        return cls(**data)
    
    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()




class RealmCreate(PrettyModel):
    """DTO de escritura para Realm."""
    name: str
    description: Optional[str] = None

    users: Optional[List[UserCreate]] = None
    roles: Optional[List[RoleCreate]] = None
    permissions: Optional[List[PermissionCreate]] = None

    model_config = ConfigDict(
        # Performance optimizations
        arbitrary_types_allowed=False,  # Más rápido al validar tipos estrictos
        use_enum_values=True,
        validate_assignment=True,  # Valida en cada asignación
        frozen=False,  # Si True, hace el objeto inmutable
        str_strip_whitespace=False,  # No procesa strings automáticamente
        validate_default=False,  # No valida valores por defecto
        extra="forbid",  # Más rápido que "allow" o "ignore"
        # Configuraciones adicionales de v2
        populate_by_name=True,  # Permite usar alias y nombres originales
        use_attribute_docstrings=True,  # Usa docstrings como descripciones
        validate_call=True,  # Valida llamadas a métodos
    )
    
    def to_instance(self) -> Realm:
        model = Realm(
            name=self.name,
            description=self.description,
        )
        if self.users is not None:
            users = [reg.to_instance() for reg in self.users]
            model.users = users
        if self.roles is not None:
            roles = [reg.to_instance() for reg in self.roles]
            model.roles = roles
        if self.permissions is not None:
            permissions = [reg.to_instance() for reg in self.permissions]
            model.permissions = permissions
        return model
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> RealmCreate:
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)




class RealmFilter(PrettyModel):
    """DTO de filtrado para Realm."""
    name: Optional[str] = None
    in_name: Optional[List[str]] = None
    description: Optional[str] = None
    in_description: Optional[List[str]] = None


    model_config = ConfigDict(
        # Performance optimizations
        arbitrary_types_allowed=False,  # Más rápido al validar tipos estrictos
        use_enum_values=True,
        validate_assignment=True,  # Valida en cada asignación
        frozen=False,  # Si True, hace el objeto inmutable
        str_strip_whitespace=False,  # No procesa strings automáticamente
        validate_default=False,  # No valida valores por defecto
        extra="forbid",  # Más rápido que "allow" o "ignore"
        # Configuraciones adicionales de v2
        populate_by_name=True,  # Permite usar alias y nombres originales
        use_attribute_docstrings=True,  # Usa docstrings como descripciones
        validate_call=True,  # Valida llamadas a métodos
    )
    
    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_defaults=True)

    def apply_to_query(self, query: Query) -> Query:
        if self.name is not None:
            if isinstance(self.name, str) and '%' in self.name:
                query = query.where(Realm.name.ilike(self.name))
            else:
                query = query.where(Realm.name == self.name)
        if self.in_name is not None and len(self.in_name) > 0:
            query = query.where(Realm.name.in_(self.in_name))
        if self.description is not None:
            if isinstance(self.description, str) and '%' in self.description:
                query = query.where(Realm.description.ilike(self.description))
            else:
                query = query.where(Realm.description == self.description)
        if self.in_description is not None and len(self.in_description) > 0:
            query = query.where(Realm.description.in_(self.in_description))

        return query



class RealmUsersNestedUpdate(PrettyModel):
    """DTO para nested writes de 'users' al actualizar Realm."""
    create: Optional[List[UserCreate]] = None
    update: Optional[List[UserUpdateNested]] = None
    delete: Optional[List[Dict[str, Any]]] = None

    model_config = ConfigDict(
        # Performance optimizations
        arbitrary_types_allowed=False,  # Más rápido al validar tipos estrictos
        use_enum_values=True,
        validate_assignment=True,  # Valida en cada asignación
        frozen=False,  # Si True, hace el objeto inmutable
        str_strip_whitespace=False,  # No procesa strings automáticamente
        validate_default=False,  # No valida valores por defecto
        extra="forbid",  # Más rápido que "allow" o "ignore"
        # Configuraciones adicionales de v2
        populate_by_name=True,  # Permite usar alias y nombres originales
        use_attribute_docstrings=True,  # Usa docstrings como descripciones
        validate_call=True,  # Valida llamadas a métodos
    )

class RealmRolesNestedUpdate(PrettyModel):
    """DTO para nested writes de 'roles' al actualizar Realm."""
    create: Optional[List[RoleCreate]] = None
    update: Optional[List[RoleUpdateNested]] = None
    delete: Optional[List[Dict[str, Any]]] = None

    model_config = ConfigDict(
        # Performance optimizations
        arbitrary_types_allowed=False,  # Más rápido al validar tipos estrictos
        use_enum_values=True,
        validate_assignment=True,  # Valida en cada asignación
        frozen=False,  # Si True, hace el objeto inmutable
        str_strip_whitespace=False,  # No procesa strings automáticamente
        validate_default=False,  # No valida valores por defecto
        extra="forbid",  # Más rápido que "allow" o "ignore"
        # Configuraciones adicionales de v2
        populate_by_name=True,  # Permite usar alias y nombres originales
        use_attribute_docstrings=True,  # Usa docstrings como descripciones
        validate_call=True,  # Valida llamadas a métodos
    )

class RealmPermissionsNestedUpdate(PrettyModel):
    """DTO para nested writes de 'permissions' al actualizar Realm."""
    create: Optional[List[PermissionCreate]] = None
    update: Optional[List[PermissionUpdateNested]] = None
    delete: Optional[List[Dict[str, Any]]] = None

    model_config = ConfigDict(
        # Performance optimizations
        arbitrary_types_allowed=False,  # Más rápido al validar tipos estrictos
        use_enum_values=True,
        validate_assignment=True,  # Valida en cada asignación
        frozen=False,  # Si True, hace el objeto inmutable
        str_strip_whitespace=False,  # No procesa strings automáticamente
        validate_default=False,  # No valida valores por defecto
        extra="forbid",  # Más rápido que "allow" o "ignore"
        # Configuraciones adicionales de v2
        populate_by_name=True,  # Permite usar alias y nombres originales
        use_attribute_docstrings=True,  # Usa docstrings como descripciones
        validate_call=True,  # Valida llamadas a métodos
    )



class RealmUpdateNested(PrettyModel):
    """DTO para actualización anidada de Realm."""
    name: str
    values: RealmUpdateValues

    model_config = ConfigDict(
        # Performance optimizations
        arbitrary_types_allowed=False,  # Más rápido al validar tipos estrictos
        use_enum_values=True,
        validate_assignment=True,  # Valida en cada asignación
        frozen=False,  # Si True, hace el objeto inmutable
        str_strip_whitespace=False,  # No procesa strings automáticamente
        validate_default=False,  # No valida valores por defecto
        extra="forbid",  # Más rápido que "allow" o "ignore"
        # Configuraciones adicionales de v2
        populate_by_name=True,  # Permite usar alias y nombres originales
        use_attribute_docstrings=True,  # Usa docstrings como descripciones
        validate_call=True,  # Valida llamadas a métodos
    )



class RealmUpdateValues(PrettyModel):
    """DTO de actualización para Realm."""
    name: str = None
    description: Optional[str] = None
    users: Optional[RealmUsersNestedUpdate] = None
    roles: Optional[RealmRolesNestedUpdate] = None
    permissions: Optional[RealmPermissionsNestedUpdate] = None

    model_config = ConfigDict(
        # Performance optimizations
        arbitrary_types_allowed=False,  # Más rápido al validar tipos estrictos
        use_enum_values=True,
        validate_assignment=True,  # Valida en cada asignación
        frozen=False,  # Si True, hace el objeto inmutable
        str_strip_whitespace=False,  # No procesa strings automáticamente
        validate_default=False,  # No valida valores por defecto
        extra="forbid",  # Más rápido que "allow" o "ignore"
        # Configuraciones adicionales de v2
        populate_by_name=True,  # Permite usar alias y nombres originales
        use_attribute_docstrings=True,  # Usa docstrings como descripciones
        validate_call=True,  # Valida llamadas a métodos
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_unset=True, exclude={
            'users',
            'roles',
            'permissions',
        })



class RealmUpdate(PrettyModel):
    """DTO de actualización completo para Realm."""
    filter: RealmFilter
    values: RealmUpdateValues

    model_config = ConfigDict(
        # Performance optimizations
        arbitrary_types_allowed=False,  # Más rápido al validar tipos estrictos
        use_enum_values=True,
        validate_assignment=True,  # Valida en cada asignación
        frozen=False,  # Si True, hace el objeto inmutable
        str_strip_whitespace=False,  # No procesa strings automáticamente
        validate_default=False,  # No valida valores por defecto
        extra="forbid",  # Más rápido que "allow" o "ignore"
        # Configuraciones adicionales de v2
        populate_by_name=True,  # Permite usar alias y nombres originales
        use_attribute_docstrings=True,  # Usa docstrings como descripciones
        validate_call=True,  # Valida llamadas a métodos
    )



from ..user.dtos import (
    UserRead,
    UserCreate,
    UserUpdateNested,
)
from ..role.dtos import (
    RoleRead,
    RoleCreate,
    RoleUpdateNested,
)
from ..permission.dtos import (
    PermissionRead,
    PermissionCreate,
    PermissionUpdateNested,
)



class RealmDataFrameValidator:
    """Validador de DataFrame para el modelo Realm."""

    def validate_dataframe_schema(self, df: DataFrame, ignore_extra_columns: bool, fill_missing_nullable: bool) -> None:
        model_columns = {
            'name': {
                'type': 'str',
                'nullable': False,
                'primary_key': True,
                'autoincrement': False
            },
            'description': {
                'type': 'str',
                'nullable': True,
                'primary_key': False,
                'autoincrement': False
            }
        }
        df_columns = set(df.columns)
        required_columns = set(model_columns.keys())
        extra_columns = df_columns - required_columns
        if extra_columns and not ignore_extra_columns:
            raise ValueError(f"DataFrame contiene columnas no definidas en el modelo: {list(extra_columns)}")
        missing_columns = required_columns - df_columns
        critical_missing = []
        for col in missing_columns:
            col_info = model_columns[col]
            if (not col_info['nullable'] and not col_info['autoincrement'] and 
                not (col_info['primary_key'] and col_info['autoincrement'])):
                critical_missing.append(col)
        if critical_missing:
            raise ValueError(f"DataFrame falta columnas requeridas (NOT NULL): {critical_missing}")
        nullable_missing = [col for col in missing_columns if col not in critical_missing]
        if nullable_missing and not fill_missing_nullable:
            import warnings
            warnings.warn(f"DataFrame falta columnas nullable: {nullable_missing}")
    
    def validate_dataframe_types(self, df: "DataFrame") -> None:
        type_compatibility = {
            'name': {
                'sqlalchemy_type': 'str',
                'compatible_pandas_types': [
                    'object', 'string', 'category'
                ]
            },
            'description': {
                'sqlalchemy_type': 'str',
                'compatible_pandas_types': [
                    'object', 'string', 'category'
                ]
            }
        }
        type_errors = []
        for column in df.columns:
            if column in type_compatibility:
                df_dtype = str(df[column].dtype)
                compatible_types = type_compatibility[column]['compatible_pandas_types']
                sqlalchemy_type = type_compatibility[column]['sqlalchemy_type']
                if df_dtype not in compatible_types:
                    if self.can_convert_type(df[column], sqlalchemy_type):
                        continue
                    type_errors.append(
                        f"Columna '{column}': tipo '{df_dtype}' no compatible con '{sqlalchemy_type}'."
                    )
        if type_errors:
            raise TypeError("Errores de tipo:\n" + "\n".join(f"  - {e}" for e in type_errors))
    
    def can_convert_type(self, series: "Series", target_sqlalchemy_type: str) -> bool:
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("pandas no está instalado.")
        try:
            sample = series.dropna().head(10)
            if sample.empty:
                return True
            if 'int' in target_sqlalchemy_type:
                pd.to_numeric(sample, errors='raise')
            elif 'float' in target_sqlalchemy_type or 'Numeric' in target_sqlalchemy_type:
                pd.to_numeric(sample, errors='raise')
            elif 'bool' in target_sqlalchemy_type:
                valid_bool_values = {True, False, 1, 0, '1', '0', 'true', 'false', 'True', 'False'}
                if not all(val in valid_bool_values for val in sample.unique()):
                    return False
            elif 'datetime' in target_sqlalchemy_type or 'date' in target_sqlalchemy_type:
                pd.to_datetime(sample, errors='raise')
            return True
        except:
            return False
    
    def prepare_dataframe_for_insertion(self, df: "DataFrame", ignore_extra_columns: bool, fill_missing_nullable: bool) -> "DataFrame":
        try:
            import pandas as pd
            import numpy as np
        except ImportError:
            return df
        cleaned_df = df.copy()
        model_columns = {
            'name': {
                'nullable': False,
                'autoincrement': False
            },
            'description': {
                'nullable': True,
                'autoincrement': False
            }
        }
        if ignore_extra_columns:
            extra_columns = set(cleaned_df.columns) - set(model_columns.keys())
            if extra_columns:
                cleaned_df = cleaned_df.drop(columns=list(extra_columns))
        if fill_missing_nullable:
            for col_name, col_info in model_columns.items():
                if (col_name not in cleaned_df.columns and col_info['nullable'] and not col_info['autoincrement']):
                    cleaned_df[col_name] = None
        autoincrement_columns = [
            col for col, info in model_columns.items() 
            if info['autoincrement'] and col in cleaned_df.columns
        ]
        if autoincrement_columns:
            cleaned_df = cleaned_df.drop(columns=autoincrement_columns)
        model_column_order = [col for col in model_columns.keys() if col in cleaned_df.columns]
        cleaned_df = cleaned_df[model_column_order]
        return cleaned_df
    
    def clean_records_data(self, records_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        try:
            import pandas as pd
        except ImportError:
            return records_data
        cleaned_records = []
        for record in records_data:
            cleaned_record = {}
            for key, value in record.items():
                if isinstance(value, list):
                    cleaned_record[key] = value
                elif pd.isna(value):
                    cleaned_record[key] = None
                elif hasattr(value, 'item'):
                    cleaned_record[key] = value.item()
                else:
                    cleaned_record[key] = value
            cleaned_records.append(cleaned_record)
        return cleaned_records