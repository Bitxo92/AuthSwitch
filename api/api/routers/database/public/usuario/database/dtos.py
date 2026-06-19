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

from .model import Usuario
from ..._shared import (
    PrettyModel,
    get_username,
    should_include_relation,
    get_nested_includes
)

if TYPE_CHECKING:
    from pandas import DataFrame, Series  # type: ignore[import-untyped]



class UsuarioRead(PrettyModel):
    """DTO de lectura para Usuario."""
    id: int = Field(
        description="Campo id de la tabla usuario",
    )
    name: str = Field(
        description="Nombre del usuario",
    )
    pwd: str = Field(
        description="Campo pwd de la tabla usuario",
    )
    email: Optional[str] = Field(
        description="Campo email de la tabla usuario",
    )
    last_post_date: Optional[datetime] = Field(
        description="Campo last_post_date de la tabla usuario",
    )

    posts: Optional[List[PostRead]] = Field(default=None)



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
        instance: Usuario,
        includes: Optional[List[str]] = None,
        max_depth: int = 5,
        distance_score: Optional[float] = None
    ) -> UsuarioRead:
        dto_data = {
            'id': instance.id,
            'name': instance.name,
            'pwd': instance.pwd,
            'email': instance.email,
            'last_post_date': instance.last_post_date,
        }

        if includes is not None and max_depth > 0:
            if should_include_relation('posts', includes):
                nested_includes = get_nested_includes('posts', includes)
                if hasattr(instance, 'posts') and instance.posts is not None:
                    dto_data['posts'] = [
                        PostRead.from_instance(reg, nested_includes, max_depth - 1) 
                        for reg in instance.posts
                    ]
        return cls(**dto_data)

    @classmethod
    def from_created_instance(cls, instance: Usuario, included: set[str], excluded: str=None) -> UsuarioRead:
        dto_data = {
            'id': instance.id,
            'name': instance.name,
            'pwd': instance.pwd,
            'email': instance.email,
            'last_post_date': instance.last_post_date,
        }
        if 'posts' in included and 'posts' != excluded:
            dto_data['posts'] = [
                PostRead.from_created_instance(reg, included, 'author') 
                for reg in instance.posts
            ]
        return cls(**dto_data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> UsuarioRead:
        return cls(**data)
    
    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()




class UsuarioCreate(PrettyModel):
    """DTO de escritura para Usuario."""
    name: str
    pwd: str
    email: Optional[str] = None
    last_post_date: Optional[datetime] = None

    posts: Optional[List[PostCreate]] = None

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
    
    def to_instance(self) -> Usuario:
        model = Usuario(
            name=self.name,
            pwd=self.pwd,
            email=self.email,
            last_post_date=self.last_post_date,
        )
        if self.posts is not None:
            posts = [reg.to_instance() for reg in self.posts]
            model.posts = posts
        return model
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> UsuarioCreate:
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)




class UsuarioFilter(PrettyModel):
    """DTO de filtrado para Usuario."""
    name: Optional[str] = None
    in_name: Optional[List[str]] = None
    email: Optional[str] = None
    in_email: Optional[List[str]] = None
    min_last_post_date: Optional[datetime] = None
    max_last_post_date: Optional[datetime] = None


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
                query = query.where(Usuario.name.ilike(self.name))
            else:
                query = query.where(Usuario.name == self.name)
        if self.in_name is not None and len(self.in_name) > 0:
            query = query.where(Usuario.name.in_(self.in_name))
        if self.email is not None:
            if isinstance(self.email, str) and '%' in self.email:
                query = query.where(Usuario.email.ilike(self.email))
            else:
                query = query.where(Usuario.email == self.email)
        if self.in_email is not None and len(self.in_email) > 0:
            query = query.where(Usuario.email.in_(self.in_email))
        if self.min_last_post_date is not None:
            query = query.where(Usuario.last_post_date >= self.min_last_post_date)
        if self.max_last_post_date is not None:
            query = query.where(Usuario.last_post_date <= self.max_last_post_date)

        return query



class UsuarioPostsNestedUpdate(PrettyModel):
    """DTO para nested writes de 'posts' al actualizar Usuario."""
    create: Optional[List[PostCreate]] = None
    update: Optional[List[PostUpdateNested]] = None
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



class UsuarioUpdateNested(PrettyModel):
    """DTO para actualización anidada de Usuario."""
    id: int
    values: UsuarioUpdateValues

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



class UsuarioUpdateValues(PrettyModel):
    """DTO de actualización para Usuario."""
    name: str = None
    pwd: str = None
    email: Optional[str] = None
    last_post_date: Optional[datetime] = None
    posts: Optional[UsuarioPostsNestedUpdate] = None

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
            'posts',
        })



class UsuarioUpdate(PrettyModel):
    """DTO de actualización completo para Usuario."""
    filter: UsuarioFilter
    values: UsuarioUpdateValues

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



from ...post.database.dtos import (
    PostRead,
    PostCreate,
    PostUpdateNested,
)



class UsuarioDataFrameValidator:
    """Validador de DataFrame para el modelo Usuario."""

    def validate_dataframe_schema(self, df: DataFrame, ignore_extra_columns: bool, fill_missing_nullable: bool) -> None:
        model_columns = {
            'id': {
                'type': 'int',
                'nullable': False,
                'primary_key': True,
                'autoincrement': True
            },
            'name': {
                'type': 'str',
                'nullable': False,
                'primary_key': False,
                'autoincrement': False
            },
            'pwd': {
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
            'last_post_date': {
                'type': 'datetime',
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
            'id': {
                'sqlalchemy_type': 'int',
                'compatible_pandas_types': [
                    'int64', 'Int64', 'int32', 'Int32', 'int16', 'Int16', 'int8', 'Int8', 'object'
                ]
            },
            'name': {
                'sqlalchemy_type': 'str',
                'compatible_pandas_types': [
                    'object', 'string', 'category'
                ]
            },
            'pwd': {
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
            'last_post_date': {
                'sqlalchemy_type': 'datetime',
                'compatible_pandas_types': [
                    'datetime64[ns]', 'object'
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
            'id': {
                'nullable': False,
                'autoincrement': True
            },
            'name': {
                'nullable': False,
                'autoincrement': False
            },
            'pwd': {
                'nullable': False,
                'autoincrement': False
            },
            'email': {
                'nullable': True,
                'autoincrement': False
            },
            'last_post_date': {
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