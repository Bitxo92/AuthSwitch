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

from .model import Comment
from .._shared import (
    PrettyModel,
    get_username,
    should_include_relation,
    get_nested_includes
)

if TYPE_CHECKING:
    from pandas import DataFrame, Series  # type: ignore[import-untyped]



class CommentRead(PrettyModel):
    """DTO de lectura para Comment."""
    id: int = Field(
        description="Campo id de la tabla comment",
    )
    content: str = Field(
        description="Contenido del comentario",
    )
    post_id: int = Field(
        description="Campo post_id de la tabla comment",
    )

    post: Optional[PostRead] = Field(default=None)



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
        instance: Comment,
        includes: Optional[List[str]] = None,
        max_depth: int = 5,
        distance_score: Optional[float] = None
    ) -> CommentRead:
        dto_data = {
            'id': instance.id,
            'content': instance.content,
            'post_id': instance.post_id,
        }

        if includes is not None and max_depth > 0:
            if should_include_relation('post', includes):
                nested_includes = get_nested_includes('post', includes)
                if hasattr(instance, 'post') and instance.post is not None:
                    dto_data['post'] = PostRead.from_instance(
                        instance.post, nested_includes, max_depth - 1
                    )
        return cls(**dto_data)

    @classmethod
    def from_created_instance(cls, instance: Comment, included: set[str], excluded: str=None) -> CommentRead:
        dto_data = {
            'id': instance.id,
            'content': instance.content,
            'post_id': instance.post_id,
        }
        if 'post' in included and 'post' != excluded:
            dto_data['post'] = PostRead.from_created_instance(
                instance.post, included, 'comments'
            )
        return cls(**dto_data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> CommentRead:
        return cls(**data)
    
    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()




class CommentCreate(PrettyModel):
    """DTO de escritura para Comment."""
    content: str
    post_id: Optional[int] = None

    post: Optional[PostCreate] = None

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
    
    def to_instance(self) -> Comment:
        model = Comment(
            content=self.content,
            post_id=self.post_id,
        )
        if self.post is not None:
            post = self.post.to_instance()
            model.post = post
        return model
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> CommentCreate:
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)




class CommentFilter(PrettyModel):
    """DTO de filtrado para Comment."""
    content: Optional[str] = None
    in_content: Optional[List[str]] = None
    post_id: Optional[int] = None
    in_post_id: Optional[List[int]] = None
    min_post_id: Optional[int] = None
    max_post_id: Optional[int] = None


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
        if self.content is not None:
            if isinstance(self.content, str) and '%' in self.content:
                query = query.where(Comment.content.ilike(self.content))
            else:
                query = query.where(Comment.content == self.content)
        if self.in_content is not None and len(self.in_content) > 0:
            query = query.where(Comment.content.in_(self.in_content))
        if self.post_id is not None:
            query = query.where(Comment.post_id == self.post_id)
        if self.in_post_id is not None and len(self.in_post_id) > 0:
            query = query.where(Comment.post_id.in_(self.in_post_id))
        if self.min_post_id is not None:
            query = query.where(Comment.post_id >= self.min_post_id)
        if self.max_post_id is not None:
            query = query.where(Comment.post_id <= self.max_post_id)

        return query





class CommentUpdateNested(PrettyModel):
    """DTO para actualización anidada de Comment."""
    id: int
    values: CommentUpdateValues

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



class CommentUpdateValues(PrettyModel):
    """DTO de actualización para Comment."""
    content: str = None
    post_id: int = None

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
        })



class CommentUpdate(PrettyModel):
    """DTO de actualización completo para Comment."""
    filter: CommentFilter
    values: CommentUpdateValues

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



from ..post.dtos import (
    PostRead,
    PostCreate,
    PostUpdateNested,
)



class CommentDataFrameValidator:
    """Validador de DataFrame para el modelo Comment."""

    def validate_dataframe_schema(self, df: DataFrame, ignore_extra_columns: bool, fill_missing_nullable: bool) -> None:
        model_columns = {
            'id': {
                'type': 'int',
                'nullable': False,
                'primary_key': True,
                'autoincrement': True
            },
            'content': {
                'type': 'str',
                'nullable': False,
                'primary_key': False,
                'autoincrement': False
            },
            'post_id': {
                'type': 'bigint',
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
            'content': {
                'sqlalchemy_type': 'str',
                'compatible_pandas_types': [
                    'object', 'string', 'category'
                ]
            },
            'post_id': {
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
            'content': {
                'nullable': False,
                'autoincrement': False
            },
            'post_id': {
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