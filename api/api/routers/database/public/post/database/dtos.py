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

from .model import Post
from ..._shared import (
    PrettyModel,
    get_username,
    should_include_relation,
    get_nested_includes
)

if TYPE_CHECKING:
    from pandas import DataFrame, Series  # type: ignore[import-untyped]



class PostRead(PrettyModel):
    """DTO de lectura para Post."""
    id: int = Field(
        description="Campo id de la tabla post",
    )
    title: str = Field(
        description="Campo title de la tabla post",
    )
    content: str = Field(
        description="Contenido del post",
    )
    content_type: str = Field(
        description="Campo content_type de la tabla post",
    )
    timestamp: datetime = Field(
        description="Fecha y hora del post",
    )
    author_id: int = Field(
        description="Campo author_id de la tabla post",
    )

    comments: Optional[List[CommentRead]] = Field(default=None)
    author: Optional[UsuarioRead] = Field(default=None)



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
        instance: Post,
        includes: Optional[List[str]] = None,
        max_depth: int = 5,
        distance_score: Optional[float] = None
    ) -> PostRead:
        dto_data = {
            'id': instance.id,
            'title': instance.title,
            'content': instance.content,
            'content_type': instance.content_type,
            'timestamp': instance.timestamp,
            'author_id': instance.author_id,
        }

        if includes is not None and max_depth > 0:
            if should_include_relation('comments', includes):
                nested_includes = get_nested_includes('comments', includes)
                if hasattr(instance, 'comments') and instance.comments is not None:
                    dto_data['comments'] = [
                        CommentRead.from_instance(reg, nested_includes, max_depth - 1) 
                        for reg in instance.comments
                    ]
            if should_include_relation('author', includes):
                nested_includes = get_nested_includes('author', includes)
                if hasattr(instance, 'author') and instance.author is not None:
                    dto_data['author'] = UsuarioRead.from_instance(
                        instance.author, nested_includes, max_depth - 1
                    )
        return cls(**dto_data)

    @classmethod
    def from_created_instance(cls, instance: Post, included: set[str], excluded: str=None) -> PostRead:
        dto_data = {
            'id': instance.id,
            'title': instance.title,
            'content': instance.content,
            'content_type': instance.content_type,
            'timestamp': instance.timestamp,
            'author_id': instance.author_id,
        }
        if 'comments' in included and 'comments' != excluded:
            dto_data['comments'] = [
                CommentRead.from_created_instance(reg, included, 'post') 
                for reg in instance.comments
            ]
        if 'author' in included and 'author' != excluded:
            dto_data['author'] = UsuarioRead.from_created_instance(
                instance.author, included, 'posts'
            )
        return cls(**dto_data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PostRead:
        return cls(**data)
    
    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()




class PostCreate(PrettyModel):
    """DTO de escritura para Post."""
    content: str
    title: str = "Post Title"
    content_type: str = "text"
    timestamp: datetime = Field(default_factory=datetime.now)
    author_id: Optional[int] = None

    comments: Optional[List[CommentCreate]] = None
    author: Optional[UsuarioCreate] = None

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
    
    def to_instance(self) -> Post:
        model = Post(
            title=self.title,
            content=self.content,
            content_type=self.content_type,
            timestamp=self.timestamp,
            author_id=self.author_id,
        )
        if self.comments is not None:
            comments = [reg.to_instance() for reg in self.comments]
            model.comments = comments
        if self.author is not None:
            author = self.author.to_instance()
            model.author = author
        return model
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PostCreate:
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)




class PostFilter(PrettyModel):
    """DTO de filtrado para Post."""
    title: Optional[str] = None
    in_title: Optional[List[str]] = None
    content: Optional[str] = None
    in_content: Optional[List[str]] = None
    content_type: Optional[str] = None
    in_content_type: Optional[List[str]] = None
    min_timestamp: Optional[datetime] = None
    max_timestamp: Optional[datetime] = None
    author_id: Optional[int] = None
    in_author_id: Optional[List[int]] = None
    min_author_id: Optional[int] = None
    max_author_id: Optional[int] = None


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
        if self.title is not None:
            if isinstance(self.title, str) and '%' in self.title:
                query = query.where(Post.title.ilike(self.title))
            else:
                query = query.where(Post.title == self.title)
        if self.in_title is not None and len(self.in_title) > 0:
            query = query.where(Post.title.in_(self.in_title))
        if self.content is not None:
            if isinstance(self.content, str) and '%' in self.content:
                query = query.where(Post.content.ilike(self.content))
            else:
                query = query.where(Post.content == self.content)
        if self.in_content is not None and len(self.in_content) > 0:
            query = query.where(Post.content.in_(self.in_content))
        if self.content_type is not None:
            if isinstance(self.content_type, str) and '%' in self.content_type:
                query = query.where(Post.content_type.ilike(self.content_type))
            else:
                query = query.where(Post.content_type == self.content_type)
        if self.in_content_type is not None and len(self.in_content_type) > 0:
            query = query.where(Post.content_type.in_(self.in_content_type))
        if self.min_timestamp is not None:
            query = query.where(Post.timestamp >= self.min_timestamp)
        if self.max_timestamp is not None:
            query = query.where(Post.timestamp <= self.max_timestamp)
        if self.author_id is not None:
            query = query.where(Post.author_id == self.author_id)
        if self.in_author_id is not None and len(self.in_author_id) > 0:
            query = query.where(Post.author_id.in_(self.in_author_id))
        if self.min_author_id is not None:
            query = query.where(Post.author_id >= self.min_author_id)
        if self.max_author_id is not None:
            query = query.where(Post.author_id <= self.max_author_id)

        return query



class PostCommentsNestedUpdate(PrettyModel):
    """DTO para nested writes de 'comments' al actualizar Post."""
    create: Optional[List[CommentCreate]] = None
    update: Optional[List[CommentUpdateNested]] = None
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



class PostUpdateNested(PrettyModel):
    """DTO para actualización anidada de Post."""
    id: int
    values: PostUpdateValues

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



class PostUpdateValues(PrettyModel):
    """DTO de actualización para Post."""
    title: str = None
    content: str = None
    content_type: str = None
    timestamp: datetime = None
    author_id: int = None
    comments: Optional[PostCommentsNestedUpdate] = None

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
            'comments',
        })



class PostUpdate(PrettyModel):
    """DTO de actualización completo para Post."""
    filter: PostFilter
    values: PostUpdateValues

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



from ...comment.database.dtos import (
    CommentRead,
    CommentCreate,
    CommentUpdateNested,
)
from ...usuario.database.dtos import (
    UsuarioRead,
    UsuarioCreate,
    UsuarioUpdateNested,
)



class PostDataFrameValidator:
    """Validador de DataFrame para el modelo Post."""

    def validate_dataframe_schema(self, df: DataFrame, ignore_extra_columns: bool, fill_missing_nullable: bool) -> None:
        model_columns = {
            'id': {
                'type': 'bigint',
                'nullable': False,
                'primary_key': True,
                'autoincrement': True
            },
            'title': {
                'type': 'str',
                'nullable': False,
                'primary_key': False,
                'autoincrement': False
            },
            'content': {
                'type': 'str',
                'nullable': False,
                'primary_key': False,
                'autoincrement': False
            },
            'content_type': {
                'type': 'str',
                'nullable': False,
                'primary_key': False,
                'autoincrement': False
            },
            'timestamp': {
                'type': 'datetime',
                'nullable': False,
                'primary_key': False,
                'autoincrement': False
            },
            'author_id': {
                'type': 'int',
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
            'id': {
                'sqlalchemy_type': 'int',
                'compatible_pandas_types': [
                    'int64', 'Int64', 'int32', 'Int32', 'int16', 'Int16', 'int8', 'Int8', 'object'
                ]
            },
            'title': {
                'sqlalchemy_type': 'str',
                'compatible_pandas_types': [
                    'object', 'string', 'category'
                ]
            },
            'content': {
                'sqlalchemy_type': 'str',
                'compatible_pandas_types': [
                    'object', 'string', 'category'
                ]
            },
            'content_type': {
                'sqlalchemy_type': 'str',
                'compatible_pandas_types': [
                    'object', 'string', 'category'
                ]
            },
            'timestamp': {
                'sqlalchemy_type': 'datetime',
                'compatible_pandas_types': [
                    'datetime64[ns]', 'object'
                ]
            },
            'author_id': {
                'sqlalchemy_type': 'int',
                'compatible_pandas_types': [
                    'int64', 'Int64', 'int32', 'Int32', 'int16', 'Int16', 'int8', 'Int8', 'object'
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
            'title': {
                'nullable': False,
                'autoincrement': False
            },
            'content': {
                'nullable': False,
                'autoincrement': False
            },
            'content_type': {
                'nullable': False,
                'autoincrement': False
            },
            'timestamp': {
                'nullable': False,
                'autoincrement': False
            },
            'author_id': {
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