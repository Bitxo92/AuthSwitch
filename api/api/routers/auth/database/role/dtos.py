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

from .model import Role
from .._shared import (
    PrettyModel,
    get_username,
    should_include_relation,
    get_nested_includes
)

if TYPE_CHECKING:
    from pandas import DataFrame, Series  # type: ignore[import-untyped]



class RoleRead(PrettyModel):
    """DTO de lectura para Role."""
    name: str = Field(
        description="Nombre del rol",
    )
    realm_name: str = Field(
        description="Realm al que pertenece el rol",
    )
    description: Optional[str] = Field(
        description="Descripción del rol",
    )
    attributes: Optional[Dict[str, Any]] = Field(
        description="Atributos adicionales del rol (JSON)",
    )
    parent_role_name: Optional[str] = Field(
        description="ID del rol padre para subroles (roles anidados)",
    )

    realm: Optional[RealmRead] = Field(default=None)
    role_permissions: Optional[List[RolePermissionRead]] = Field(default=None)
    user_roles: Optional[List[UserRoleRead]] = Field(default=None)

    tree_level: Optional[int] = Field(default=None, description="Nivel en el árbol jerárquico (0 = nodo raíz de la consulta)")
    descendants: Optional[List[RoleRead]] = Field(default=None, description="Subárbol de descendientes (poblado en tree_mode='descendants' o 'full_tree')")
    ancestors: Optional[List[RoleRead]] = Field(default=None, description="Cadena de ancestros (poblado en tree_mode='ancestors' o 'full_tree')")


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
        instance: Role,
        includes: Optional[List[str]] = None,
        max_depth: int = 5,
        distance_score: Optional[float] = None
    ) -> RoleRead:
        dto_data = {
            'name': instance.name,
            'realm_name': instance.realm_name,
            'description': instance.description,
            'attributes': instance.attributes,
            'parent_role_name': instance.parent_role_name,
        }

        if includes is not None and max_depth > 0:
            if should_include_relation('realm', includes):
                nested_includes = get_nested_includes('realm', includes)
                if hasattr(instance, 'realm') and instance.realm is not None:
                    dto_data['realm'] = RealmRead.from_instance(
                        instance.realm, nested_includes, max_depth - 1
                    )
            if should_include_relation('role_permissions', includes):
                nested_includes = get_nested_includes('role_permissions', includes)
                if hasattr(instance, 'role_permissions') and instance.role_permissions is not None:
                    dto_data['role_permissions'] = [
                        RolePermissionRead.from_instance(reg, nested_includes, max_depth - 1) 
                        for reg in instance.role_permissions
                    ]
            if should_include_relation('user_roles', includes):
                nested_includes = get_nested_includes('user_roles', includes)
                if hasattr(instance, 'user_roles') and instance.user_roles is not None:
                    dto_data['user_roles'] = [
                        UserRoleRead.from_instance(reg, nested_includes, max_depth - 1) 
                        for reg in instance.user_roles
                    ]
        return cls(**dto_data)

    @classmethod
    def from_created_instance(cls, instance: Role, included: set[str], excluded: str=None) -> RoleRead:
        dto_data = {
            'name': instance.name,
            'realm_name': instance.realm_name,
            'description': instance.description,
            'attributes': instance.attributes,
            'parent_role_name': instance.parent_role_name,
        }
        if 'realm' in included and 'realm' != excluded:
            dto_data['realm'] = RealmRead.from_created_instance(
                instance.realm, included, 'roles'
            )
        if 'role_permissions' in included and 'role_permissions' != excluded:
            dto_data['role_permissions'] = [
                RolePermissionRead.from_created_instance(reg, included, 'role') 
                for reg in instance.role_permissions
            ]
        if 'user_roles' in included and 'user_roles' != excluded:
            dto_data['user_roles'] = [
                UserRoleRead.from_created_instance(reg, included, 'role') 
                for reg in instance.user_roles
            ]
        return cls(**dto_data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> RoleRead:
        return cls(**data)
    
    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()




class RoleCreate(PrettyModel):
    """DTO de escritura para Role."""
    name: str
    realm_name: Optional[str] = None
    description: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None
    parent_role_name: Optional[str] = None

    realm: Optional[RealmCreate] = None
    role_permissions: Optional[List[RolePermissionCreate]] = None
    user_roles: Optional[List[UserRoleCreate]] = None

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
    
    def to_instance(self) -> Role:
        model = Role(
            name=self.name,
            realm_name=self.realm_name,
            description=self.description,
            attributes=self.attributes,
            parent_role_name=self.parent_role_name,
        )
        if self.realm is not None:
            realm = self.realm.to_instance()
            model.realm = realm
        if self.role_permissions is not None:
            role_permissions = [reg.to_instance() for reg in self.role_permissions]
            model.role_permissions = role_permissions
        if self.user_roles is not None:
            user_roles = [reg.to_instance() for reg in self.user_roles]
            model.user_roles = user_roles
        return model
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> RoleCreate:
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)




class RoleFilter(PrettyModel):
    """DTO de filtrado para Role."""
    name: Optional[str] = None
    in_name: Optional[List[str]] = None
    realm_name: Optional[str] = None
    in_realm_name: Optional[List[str]] = None
    description: Optional[str] = None
    in_description: Optional[List[str]] = None
    parent_role_name: Optional[str] = None
    in_parent_role_name: Optional[List[str]] = None


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
                query = query.where(Role.name.ilike(self.name))
            else:
                query = query.where(Role.name == self.name)
        if self.in_name is not None and len(self.in_name) > 0:
            query = query.where(Role.name.in_(self.in_name))
        if self.realm_name is not None:
            if isinstance(self.realm_name, str) and '%' in self.realm_name:
                query = query.where(Role.realm_name.ilike(self.realm_name))
            else:
                query = query.where(Role.realm_name == self.realm_name)
        if self.in_realm_name is not None and len(self.in_realm_name) > 0:
            query = query.where(Role.realm_name.in_(self.in_realm_name))
        if self.description is not None:
            if isinstance(self.description, str) and '%' in self.description:
                query = query.where(Role.description.ilike(self.description))
            else:
                query = query.where(Role.description == self.description)
        if self.in_description is not None and len(self.in_description) > 0:
            query = query.where(Role.description.in_(self.in_description))
        if self.parent_role_name is not None:
            if isinstance(self.parent_role_name, str) and '%' in self.parent_role_name:
                query = query.where(Role.parent_role_name.ilike(self.parent_role_name))
            else:
                query = query.where(Role.parent_role_name == self.parent_role_name)
        if self.in_parent_role_name is not None and len(self.in_parent_role_name) > 0:
            query = query.where(Role.parent_role_name.in_(self.in_parent_role_name))

        return query



class RoleRole_permissionsNestedUpdate(PrettyModel):
    """DTO para nested writes de 'role_permissions' al actualizar Role."""
    create: Optional[List[RolePermissionCreate]] = None
    update: Optional[List[RolePermissionUpdateNested]] = None
    delete: Optional[List[int]] = None

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

class RoleUser_rolesNestedUpdate(PrettyModel):
    """DTO para nested writes de 'user_roles' al actualizar Role."""
    create: Optional[List[UserRoleCreate]] = None
    update: Optional[List[UserRoleUpdateNested]] = None
    delete: Optional[List[int]] = None

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



class RoleUpdateNested(PrettyModel):
    """DTO para actualización anidada de Role."""
    name: str
    realm_name: str
    values: RoleUpdateValues

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



class RoleUpdateValues(PrettyModel):
    """DTO de actualización para Role."""
    name: str = None
    realm_name: str = None
    description: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None
    parent_role_name: Optional[str] = None
    role_permissions: Optional[RoleRole_permissionsNestedUpdate] = None
    user_roles: Optional[RoleUser_rolesNestedUpdate] = None

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
            'role_permissions',
            'user_roles',
        })



class RoleUpdate(PrettyModel):
    """DTO de actualización completo para Role."""
    filter: RoleFilter
    values: RoleUpdateValues

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



from ..realm.dtos import (
    RealmRead,
    RealmCreate,
    RealmUpdateNested,
)
from ..role_permission.dtos import (
    RolePermissionRead,
    RolePermissionCreate,
    RolePermissionUpdateNested,
)
from ..user_role.dtos import (
    UserRoleRead,
    UserRoleCreate,
    UserRoleUpdateNested,
)



class RoleDataFrameValidator:
    """Validador de DataFrame para el modelo Role."""

    def validate_dataframe_schema(self, df: DataFrame, ignore_extra_columns: bool, fill_missing_nullable: bool) -> None:
        model_columns = {
            'name': {
                'type': 'str',
                'nullable': False,
                'primary_key': True,
                'autoincrement': False
            },
            'realm_name': {
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
            },
            'attributes': {
                'type': 'dict',
                'nullable': True,
                'primary_key': False,
                'autoincrement': False
            },
            'parent_role_name': {
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
            'realm_name': {
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
            },
            'attributes': {
                'sqlalchemy_type': 'dict',
                'compatible_pandas_types': [
                    'object'
                ]
            },
            'parent_role_name': {
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
            'realm_name': {
                'nullable': False,
                'autoincrement': False
            },
            'description': {
                'nullable': True,
                'autoincrement': False
            },
            'attributes': {
                'nullable': True,
                'autoincrement': False
            },
            'parent_role_name': {
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