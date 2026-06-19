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
from datetime import datetime
from sqlalchemy.orm.query import Query
from pydantic import (
    Field,
    ConfigDict,
)

from .model import User
from .._shared import (
    PrettyModel,
    get_username,
    should_include_relation,
    get_nested_includes
)

if TYPE_CHECKING:
    from pandas import DataFrame, Series  # type: ignore[import-untyped]



class UserRead(PrettyModel):
    """DTO de lectura para User."""
    username: str = Field(
        description="Nombre de usuario único",
    )
    realm_name: str = Field(
        description="Realm al que pertenece el usuario",
    )
    first_name: Optional[str] = Field(
        description="Nombre del usuario",
    )
    last_name: Optional[str] = Field(
        description="Apellido del usuario",
    )
    password: str = Field(
        description="Contraseña encriptada",
    )
    email: Optional[str] = Field(
        description="Correo electrónico",
    )
    is_active: bool = Field(
        description="Usuario activo",
    )
    session_id: Optional[str] = Field(
        description="ID de sesión actual (para control de concurrencia)",
    )
    password_expiration: Optional[datetime] = Field(
        description="Fecha de expiración de la contraseña",
    )
    attributes: Optional[Dict[str, Any]] = Field(
        description="Atributos adicionales del usuario (JSON)",
    )
    full_name: str = Field(
        description="Columna calculada full_name",
    )

    realm: Optional[RealmRead] = Field(default=None)
    user_roles: Optional[List[UserRoleRead]] = Field(default=None)



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
        instance: User,
        includes: Optional[List[str]] = None,
        max_depth: int = 5,
        distance_score: Optional[float] = None
    ) -> UserRead:
        dto_data = {
            'username': instance.username,
            'realm_name': instance.realm_name,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'password': instance.password,
            'email': instance.email,
            'is_active': instance.is_active,
            'session_id': instance.session_id,
            'password_expiration': instance.password_expiration,
            'attributes': instance.attributes,
            'full_name': instance.full_name,
        }

        if includes is not None and max_depth > 0:
            if should_include_relation('realm', includes):
                nested_includes = get_nested_includes('realm', includes)
                if hasattr(instance, 'realm') and instance.realm is not None:
                    dto_data['realm'] = RealmRead.from_instance(
                        instance.realm, nested_includes, max_depth - 1
                    )
            if should_include_relation('user_roles', includes):
                nested_includes = get_nested_includes('user_roles', includes)
                if hasattr(instance, 'user_roles') and instance.user_roles is not None:
                    dto_data['user_roles'] = [
                        UserRoleRead.from_instance(reg, nested_includes, max_depth - 1) 
                        for reg in instance.user_roles
                    ]
        return cls(**dto_data)

    @classmethod
    def from_created_instance(cls, instance: User, included: set[str], excluded: str=None) -> UserRead:
        dto_data = {
            'username': instance.username,
            'realm_name': instance.realm_name,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'password': instance.password,
            'email': instance.email,
            'is_active': instance.is_active,
            'session_id': instance.session_id,
            'password_expiration': instance.password_expiration,
            'attributes': instance.attributes,
            'full_name': instance.full_name,
        }
        if 'realm' in included and 'realm' != excluded:
            dto_data['realm'] = RealmRead.from_created_instance(
                instance.realm, included, 'users'
            )
        if 'user_roles' in included and 'user_roles' != excluded:
            dto_data['user_roles'] = [
                UserRoleRead.from_created_instance(reg, included, 'user') 
                for reg in instance.user_roles
            ]
        return cls(**dto_data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> UserRead:
        return cls(**data)
    
    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()




class UserCreate(PrettyModel):
    """DTO de escritura para User."""
    username: str
    password: str
    realm_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    is_active: bool = True
    session_id: Optional[str] = None
    password_expiration: Optional[datetime] = None
    attributes: Optional[Dict[str, Any]] = None

    realm: Optional[RealmCreate] = None
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
    
    def to_instance(self) -> User:
        model = User(
            username=self.username,
            realm_name=self.realm_name,
            first_name=self.first_name,
            last_name=self.last_name,
            password=self.password,
            email=self.email,
            is_active=self.is_active,
            session_id=self.session_id,
            password_expiration=self.password_expiration,
            attributes=self.attributes,
        )
        if self.realm is not None:
            realm = self.realm.to_instance()
            model.realm = realm
        if self.user_roles is not None:
            user_roles = [reg.to_instance() for reg in self.user_roles]
            model.user_roles = user_roles
        return model
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> UserCreate:
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)




class UserFilter(PrettyModel):
    """DTO de filtrado para User."""
    username: Optional[str] = None
    in_username: Optional[List[str]] = None
    realm_name: Optional[str] = None
    in_realm_name: Optional[List[str]] = None
    first_name: Optional[str] = None
    in_first_name: Optional[List[str]] = None
    last_name: Optional[str] = None
    in_last_name: Optional[List[str]] = None
    email: Optional[str] = None
    in_email: Optional[List[str]] = None
    is_active: Optional[bool] = None
    session_id: Optional[str] = None
    in_session_id: Optional[List[str]] = None
    min_password_expiration: Optional[datetime] = None
    max_password_expiration: Optional[datetime] = None
    full_name: Optional[str] = None
    in_full_name: Optional[List[str]] = None


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
        if self.username is not None:
            if isinstance(self.username, str) and '%' in self.username:
                query = query.where(User.username.ilike(self.username))
            else:
                query = query.where(User.username == self.username)
        if self.in_username is not None and len(self.in_username) > 0:
            query = query.where(User.username.in_(self.in_username))
        if self.realm_name is not None:
            if isinstance(self.realm_name, str) and '%' in self.realm_name:
                query = query.where(User.realm_name.ilike(self.realm_name))
            else:
                query = query.where(User.realm_name == self.realm_name)
        if self.in_realm_name is not None and len(self.in_realm_name) > 0:
            query = query.where(User.realm_name.in_(self.in_realm_name))
        if self.first_name is not None:
            if isinstance(self.first_name, str) and '%' in self.first_name:
                query = query.where(User.first_name.ilike(self.first_name))
            else:
                query = query.where(User.first_name == self.first_name)
        if self.in_first_name is not None and len(self.in_first_name) > 0:
            query = query.where(User.first_name.in_(self.in_first_name))
        if self.last_name is not None:
            if isinstance(self.last_name, str) and '%' in self.last_name:
                query = query.where(User.last_name.ilike(self.last_name))
            else:
                query = query.where(User.last_name == self.last_name)
        if self.in_last_name is not None and len(self.in_last_name) > 0:
            query = query.where(User.last_name.in_(self.in_last_name))
        if self.email is not None:
            if isinstance(self.email, str) and '%' in self.email:
                query = query.where(User.email.ilike(self.email))
            else:
                query = query.where(User.email == self.email)
        if self.in_email is not None and len(self.in_email) > 0:
            query = query.where(User.email.in_(self.in_email))
        if self.is_active is not None:
            query = query.where(User.is_active == self.is_active)
        if self.session_id is not None:
            if isinstance(self.session_id, str) and '%' in self.session_id:
                query = query.where(User.session_id.ilike(self.session_id))
            else:
                query = query.where(User.session_id == self.session_id)
        if self.in_session_id is not None and len(self.in_session_id) > 0:
            query = query.where(User.session_id.in_(self.in_session_id))
        if self.min_password_expiration is not None:
            query = query.where(User.password_expiration >= self.min_password_expiration)
        if self.max_password_expiration is not None:
            query = query.where(User.password_expiration <= self.max_password_expiration)
        if self.full_name is not None:
            if isinstance(self.full_name, str) and '%' in self.full_name:
                query = query.where(User.full_name.ilike(self.full_name))
            else:
                query = query.where(User.full_name == self.full_name)
        if self.in_full_name is not None and len(self.in_full_name) > 0:
            query = query.where(User.full_name.in_(self.in_full_name))

        return query



class UserUser_rolesNestedUpdate(PrettyModel):
    """DTO para nested writes de 'user_roles' al actualizar User."""
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



class UserUpdateNested(PrettyModel):
    """DTO para actualización anidada de User."""
    username: str
    realm_name: str
    values: UserUpdateValues

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



class UserUpdateValues(PrettyModel):
    """DTO de actualización para User."""
    username: str = None
    realm_name: str = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: str = None
    email: Optional[str] = None
    is_active: bool = None
    session_id: Optional[str] = None
    password_expiration: Optional[datetime] = None
    attributes: Optional[Dict[str, Any]] = None
    user_roles: Optional[UserUser_rolesNestedUpdate] = None

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
            'user_roles',
        })



class UserUpdate(PrettyModel):
    """DTO de actualización completo para User."""
    filter: UserFilter
    values: UserUpdateValues

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
from ..user_role.dtos import (
    UserRoleRead,
    UserRoleCreate,
    UserRoleUpdateNested,
)



class UserDataFrameValidator:
    """Validador de DataFrame para el modelo User."""

    def validate_dataframe_schema(self, df: DataFrame, ignore_extra_columns: bool, fill_missing_nullable: bool) -> None:
        model_columns = {
            'username': {
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
            'first_name': {
                'type': 'str',
                'nullable': True,
                'primary_key': False,
                'autoincrement': False
            },
            'last_name': {
                'type': 'str',
                'nullable': True,
                'primary_key': False,
                'autoincrement': False
            },
            'password': {
                'type': 'str',
                'nullable': False,
                'primary_key': False,
                'autoincrement': False
            },
            'email': {
                'type': 'str',
                'nullable': True,
                'primary_key': False,
                'autoincrement': False
            },
            'is_active': {
                'type': 'bool',
                'nullable': False,
                'primary_key': False,
                'autoincrement': False
            },
            'session_id': {
                'type': 'str',
                'nullable': True,
                'primary_key': False,
                'autoincrement': False
            },
            'password_expiration': {
                'type': 'datetime',
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
            'full_name': {
                'type': 'str',
                'nullable': False,
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
            'username': {
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
            'first_name': {
                'sqlalchemy_type': 'str',
                'compatible_pandas_types': [
                    'object', 'string', 'category'
                ]
            },
            'last_name': {
                'sqlalchemy_type': 'str',
                'compatible_pandas_types': [
                    'object', 'string', 'category'
                ]
            },
            'password': {
                'sqlalchemy_type': 'str',
                'compatible_pandas_types': [
                    'object', 'string', 'category'
                ]
            },
            'email': {
                'sqlalchemy_type': 'str',
                'compatible_pandas_types': [
                    'object', 'string', 'category'
                ]
            },
            'is_active': {
                'sqlalchemy_type': 'bool',
                'compatible_pandas_types': [
                    'bool', 'boolean', 'object'
                ]
            },
            'session_id': {
                'sqlalchemy_type': 'str',
                'compatible_pandas_types': [
                    'object', 'string', 'category'
                ]
            },
            'password_expiration': {
                'sqlalchemy_type': 'datetime',
                'compatible_pandas_types': [
                    'datetime64[ns]', 'object'
                ]
            },
            'attributes': {
                'sqlalchemy_type': 'dict',
                'compatible_pandas_types': [
                    'object'
                ]
            },
            'full_name': {
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
            'username': {
                'nullable': False,
                'autoincrement': False
            },
            'realm_name': {
                'nullable': False,
                'autoincrement': False
            },
            'first_name': {
                'nullable': True,
                'autoincrement': False
            },
            'last_name': {
                'nullable': True,
                'autoincrement': False
            },
            'password': {
                'nullable': False,
                'autoincrement': False
            },
            'email': {
                'nullable': True,
                'autoincrement': False
            },
            'is_active': {
                'nullable': False,
                'autoincrement': False
            },
            'session_id': {
                'nullable': True,
                'autoincrement': False
            },
            'password_expiration': {
                'nullable': True,
                'autoincrement': False
            },
            'attributes': {
                'nullable': True,
                'autoincrement': False
            },
            'full_name': {
                'nullable': False,
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