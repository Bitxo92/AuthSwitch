# Este archivo ha sido generado automáticamente por tai-sql
# No modifiques este archivo directamente

from __future__ import annotations
from typing import (
    List,
    Optional,
    Dict,
    Union,
    Literal,
    Any,
    TYPE_CHECKING,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    select,
    update,
    delete,
    func,
    text,
    literal_column,
    or_,
    and_,
)
from .model import UserStats
from .dtos import *
from ..._shared import (
    async_error_handler,
    get_loading_options,
    get_included_relations,
    get_username,
    RLSQueryApplicator,
    ExpressionParser,
    RLS,
    _log_tx,
    _log_commit,
    OPERATION_TYPE_VALIDATORS,
    OPERATION_FUNCTIONS,
    GROUP_BY_FORBIDDEN_TYPES,
    GROUP_BY_DATETIME_TYPES,
    AggregationResult,
    AggRow,
    AggRequest,
    AggField,
    GroupByField
)
from ..._session import async_session_manager
from tai_alphi import Alphi

if TYPE_CHECKING:
    from pandas import DataFrame  # type: ignore[import-untyped]

# Logger
logger = Alphi.get_logger_by_name("tai-api")


class UserStatsAsyncDAO:
    """
    DAO síncrono de acceso a datos para el modelo ``UserStats``.

    Encapsula la lógica de persistencia del esquema ``public``,
    exponiendo una API tipada y completa sobre SQLAlchemy síncrono.
    Soporta sesión automática (commit/rollback gestionados internamente)
    y sesión compartida para agrupar operaciones en una misma transacción.

    Gestión de sesiones:
        - ``session=None``      → sesión automática: se abre, se hace commit
          y se cierra en cada llamada. Errores hacen rollback automáticamente.
        - ``session=<Session>`` → sesión compartida: la operación participa en
          la transacción del llamador (ej. dentro de un bloque
          ``with session_manager.transaction() as session``).

    Características:
        - Carga eager declarativa de relaciones mediante ``includes``
        - Row Level Security integrado mediante ``rls``
        - Hooks de trigger antes/después de cada escritura (create/update/delete)
        - Motor de agregaciones multi-operación con GROUP BY opcional
        - Integración nativa con pandas DataFrames

    Attributes:
        session_manager (SyncSessionManager):
            Fuente de todas las sesiones síncronas de este DAO.

    Métodos de lectura:
        find(*pk_fields, includes, rls, session) → Optional[UserStatsRead]:
            Busca un registro por su clave primaria. Acepta ``includes`` para
            carga eager de relaciones anidadas (ej. ``["autor", "autor.perfil"]``)
            y ``rls`` para filtros de seguridad por fila. Retorna ``None`` si
            el registro no existe.

        find_many(limit, offset, order_by, order, *filters, includes, rls, session)
                → List[UserStatsRead]:
            Lista registros con filtros opcionales, paginación (``limit``,
            ``offset``) y ordenamiento multi-columna (``order_by``, ``order``).
            Admite ``includes`` para relaciones y ``rls`` para seguridad.

        count(*filters, session) → int:
            Cuenta registros que satisfacen los filtros. Útil para obtener
            totales sin cargar los datos completos.

        exists(*filters, session) → bool:
            Devuelve ``True`` si existe al menos un registro coincidente.
            Internamente delega en ``count``.

    Métodos de agregación:
        sum(agg_fields, *filters, session) → AggregationResult:
            Suma campos numéricos filtrados. ``result.data`` contiene
            ``{"sum_<campo>": float | None}`` por cada campo solicitado.

        mean(agg_fields, *filters, session) → AggregationResult:
            Media aritmética de campos numéricos filtrados.
            ``result.data`` → ``{"mean_<campo>": float | None}``.

        max(agg_fields, *filters, session) → AggregationResult:
            Valor máximo de campos numéricos o de fecha (ISO 8601).
            ``result.data`` → ``{"max_<campo>": float | str | None}``.

        min(agg_fields, *filters, session) → AggregationResult:
            Valor mínimo de campos numéricos o de fecha (ISO 8601).
            ``result.data`` → ``{"min_<campo>": float | str | None}``.

        agg(request, *filters, verbose, session) → AggregationResult:
            Motor de agregaciones multi-operación. Acepta un ``AggRequest``
            con múltiples operaciones (sum, mean, max, min, count),
            expresiones aritméticas mediante ``AggField``, GROUP BY con
            truncado temporal (``GroupByField + DatetimeTrunc``),
            ordenamiento por resultado y límite de grupos.
            ``result.rows: List[AggRow]`` — cada AggRow expone ``group``
            (valores de agrupación) y ``data`` (valores agregados).

    Métodos de DataFrame:
        as_dataframe(limit, offset, *filters) → pandas.DataFrame:
            Equivalente a ``find_many`` devolviendo un ``DataFrame`` de pandas.
            Los tipos de columnas se optimizan automáticamente: enteros a
            ``Int64``, decimales a ``float64``, booleanos a ``boolean``,
            fechas a ``datetime64[ns]`` y cadenas a ``string``.
            Requiere ``pandas`` instalado.

    Ejemplos de uso:
        ```python
        from tai_sql.orm import AggRequest, AggField, GroupByField, DatetimeTrunc, AggOrderBy

        dao = UserStatsAsyncDAO

        # ── Lectura ───────────────────────────────────────────────────────────
        registro  = dao.find()
        pagina    = dao.find_many(limit=20, offset=0, order_by=["created_at"], order="DESC")
        total     = dao.count()
        hay_datos = dao.exists()

        # Con carga de relaciones
        registros = dao.find_many(limit=10, includes=["relacion_a", "relacion_a.anidada_b"])

        # ── Agregaciones ──────────────────────────────────────────────────────
        r = dao.sum(agg_fields=["importe"])
        print(r.data)  # {"sum_importe": 1234.56}

        # Multipropósito con GROUP BY mensual y orden descendente
        r = dao.agg(
            AggRequest(
                aggregations={
                    "sum":   [AggField(expr="ingresos - costes", alias="beneficio")],
                    "count": ["id"],
                    "mean":  ["precio"],
                },
                group_by=[GroupByField(field="created_at", trunc=DatetimeTrunc.month)],
                order_by=[AggOrderBy(operation="sum", field="beneficio", direction="desc")],
                limit=12,
            ),
        )
        for fila in r.rows:
            print(fila.group, fila.data)

        # ── DataFrame ─────────────────────────────────────────────────────────
        df = dao.as_dataframe(limit=5000)
        df.to_csv("user_stats.csv", index=False)

        ```
    """




    @classmethod
    @async_error_handler
    async def find_many(
        cls,
        limit: Optional[int] = None, 
        offset: Optional[int] = None,
        order_by: Optional[List[str]] = None,
        order: Literal["ASC", "DESC"] = "ASC",
        user_id: Optional[int] = None,
        in_user_id: Optional[List[int]] = None,
        min_user_id: Optional[int] = None,
        max_user_id: Optional[int] = None,
        user_name: Optional[str] = None,
        in_user_name: Optional[List[str]] = None,
        post_count: Optional[int] = None,
        in_post_count: Optional[List[int]] = None,
        min_post_count: Optional[int] = None,
        max_post_count: Optional[int] = None,
        includes: Optional[List[str]] = None,
        rls: Optional[Union[List[RLS], RLS]] = None,
        session: Optional[AsyncSession] = None
    ) -> List[UserStatsRead]:
        """
        Busca múltiples registros, filtrados, con carga optimizada de relaciones.
        
        Args:
        - limit: Límite de registros a retornar
        - offset: Número de registros a saltar
        - order_by: Lista de nombres de columnas para ordenar los resultados
        - order: ASC/DESC (por defecto ASC). Solo se aplica si se especifica order_by.
        - user_id: Filtrar por user_id
        - in_user_id: Filtrar por múltiples valores de user_id (OR lógico)
        - min_user_id: Filtrar por valor mínimo de user_id (incluído)
        - max_user_id: Filtrar por valor máximo de user_id (incluído)
        - user_name: Filtrar por user_name
        - in_user_name: Filtrar por múltiples valores de user_name (OR lógico)
        - post_count: Filtrar por post_count
        - in_post_count: Filtrar por múltiples valores de post_count (OR lógico)
        - min_post_count: Filtrar por valor mínimo de post_count (incluído)
        - max_post_count: Filtrar por valor máximo de post_count (incluído)
        
        
        - includes: Lista de relaciones a incluir (formato: 'relation' o 'relation.nested')
        - session: Sesión existente (opcional)
            
        Returns:
            Lista de instancias del modelo

        Examples:
            Búsqueda simple con relaciones

            dao.find_many(limit=10, includes=['author'])
            
            Relaciones anidadas

            dao.find_many(
                ..., 
                includes=['author', 'author.profile', 'comments']
            )
            
            Ordenamiento ascendente por columnas

            dao.find_many(order_by=['created_at', 'name'], order='ASC')
            
            Ordenamiento descendente por columnas

            dao.find_many(order_by=['created_at', 'name'], order='DESC')
            
            Paginación

            # Obtener los primeros 10 registros
            dao.find_many(limit=10)
            
            # Obtener los últimos 5 registros ordenados por fecha
            dao.find_many(limit=5, order_by=['created_at'], order='DESC')
            
            # Paginación con offset
            dao.find_many(limit=10, offset=20)
        """
        _log_tx(session, f"[public] 🔍 Buscando múltiples UserStats:")
        if limit is not None:
            _log_tx(session, f"[public]     limit={limit}")
        if offset is not None:
            _log_tx(session, f"[public]     offset={offset}")
        if order_by:
            _log_tx(session, f"[public]     order_by={order_by}")
            _log_tx(session, f"[public]     order={order}")
        if includes:
            _log_tx(session, f"[public]     includes={includes}")

        # Construir query base
        query = select(UserStats)
        
        # Aplicar filtros de búsqueda
        _filter = UserStatsFilter(
            user_id=user_id,
            in_user_id=in_user_id,
            min_user_id=min_user_id,
            max_user_id=max_user_id,
            user_name=user_name,
            in_user_name=in_user_name,
            post_count=post_count,
            in_post_count=in_post_count,
            min_post_count=min_post_count,
            max_post_count=max_post_count,
        )
        query = _filter.apply_to_query(query)
        filters = _filter.to_dict()





        # Log de parámetros aplicados
        if filters:
            _log_tx(session, f"[public]     filters={filters}")

        # Aplicar regla RLS (si existe)
        if rls is not None:
            query = RLSQueryApplicator.apply_rls(query, UserStats, rls)
        
        # Aplicar opciones de carga optimizada
        if includes:
            loading_options = get_loading_options(UserStats, includes)
            if loading_options:
                query = query.options(*loading_options)

        
        # Aplicar ordenamiento
        if order_by:
            for column_name in order_by:
                if hasattr(UserStats, column_name):
                    column = getattr(UserStats, column_name)
                    if order.upper() == "DESC":
                        query = query.order_by(column.desc())
                    elif order.upper() == "ASC":
                        query = query.order_by(column.asc())
                else:
                    logger.warning(f"[public] ⚠️ Columna '{column_name}' no existe en modelo UserStats, ignorando en order_by")

        # Aplicar límite (solo valores positivos)
        if limit is not None and limit > 0:
            query = query.limit(limit)

        # Aplicar paginación
        if offset is not None:
            query = query.offset(offset)

        # Ejecutar query
        async def execute_query(session: AsyncSession) -> List[UserStatsRead]:
            results = await session.execute(query)
            instances = results.scalars().all()
            
            _log_commit(session, f"[public] ✅ Encontrados {len(instances)} registros UserStats")

            return [
                UserStatsRead.from_instance(
                    instance, 
                ) 
                for instance in instances
            ]
        
        if session is not None:
            return await execute_query(session)
        else:
            async with async_session_manager.get_session() as session:
                return await execute_query(session)

    @classmethod
    async def count(
        cls,
        user_id: Optional[int] = None,
        in_user_id: Optional[List[int]] = None,
        min_user_id: Optional[int] = None,
        max_user_id: Optional[int] = None,
        user_name: Optional[str] = None,
        in_user_name: Optional[List[str]] = None,
        post_count: Optional[int] = None,
        in_post_count: Optional[List[int]] = None,
        min_post_count: Optional[int] = None,
        max_post_count: Optional[int] = None,
        rls: Optional[Union[List[RLS], RLS]] = None,
        session: Optional[AsyncSession] = None
    ) -> int:
        """
        Cuenta registros que coincidan con los filtros.
        
        Args:
        - user_id: Filtrar por user_id
            - in_user_id: Filtrar por múltiples valores de user_id (OR lógico)
            - min_user_id: Filtrar por valor mínimo de user_id (incluído)
            - max_user_id: Filtrar por valor máximo de user_id (incluído)
            - user_name: Filtrar por user_name
            - in_user_name: Filtrar por múltiples valores de user_name (OR lógico)
            - post_count: Filtrar por post_count
            - in_post_count: Filtrar por múltiples valores de post_count (OR lógico)
            - min_post_count: Filtrar por valor mínimo de post_count (incluído)
            - max_post_count: Filtrar por valor máximo de post_count (incluído)
        - rls: Reglas de seguridad a aplicar (opcional)
        - session: Sesión existente (opcional)
            
        Returns:
            Número de registros que coinciden con los filtros
        """
        _log_tx(session, f"[public] 🔢 Contando registros UserStats con filtros aplicados")
        
        query = select(func.count()).select_from(UserStats)
        
        _filter = UserStatsFilter(
            user_id=user_id,
            in_user_id=in_user_id,
            min_user_id=min_user_id,
            max_user_id=max_user_id,
            user_name=user_name,
            in_user_name=in_user_name,
            post_count=post_count,
            in_post_count=in_post_count,
            min_post_count=min_post_count,
            max_post_count=max_post_count,
        )
        query = _filter.apply_to_query(query)
        filters = _filter.to_dict()
        
        # Log de parámetros aplicados
        if filters:
            _log_tx(session, f"[public]     filters={filters}")

        # Aplicar regla RLS (si existe)
        if rls is not None:
            query = RLSQueryApplicator.apply_rls(query, UserStats, rls)

        if session is not None:
            result = await session.execute(query)
        else:
            async with async_session_manager.get_session() as session:
                result = await session.execute(query)

        count_result = result.scalar() or 0
        _log_commit(session, f"[public] ✅ Conteo UserStats completado: {count_result} registros")
        return count_result

    @classmethod
    @async_error_handler
    async def exists(
        cls,
        user_id: Optional[int] = None,
        in_user_id: Optional[List[int]] = None,
        min_user_id: Optional[int] = None,
        max_user_id: Optional[int] = None,
        user_name: Optional[str] = None,
        in_user_name: Optional[List[str]] = None,
        post_count: Optional[int] = None,
        in_post_count: Optional[List[int]] = None,
        min_post_count: Optional[int] = None,
        max_post_count: Optional[int] = None,
        rls: Optional[Union[List[RLS], RLS]] = None,
        session: Optional[AsyncSession] = None
    ) -> bool:
        """
        Verifica si existe al menos un registro que coincida con los filtros.
        
        Args:
            - user_id: Filtrar por user_id
            - in_user_id: Filtrar por múltiples valores de user_id (OR lógico)
            - min_user_id: Filtrar por valor mínimo de user_id (incluído)
            - max_user_id: Filtrar por valor máximo de user_id (incluído)
            - user_name: Filtrar por user_name
            - in_user_name: Filtrar por múltiples valores de user_name (OR lógico)
            - post_count: Filtrar por post_count
            - in_post_count: Filtrar por múltiples valores de post_count (OR lógico)
            - min_post_count: Filtrar por valor mínimo de post_count (incluído)
            - max_post_count: Filtrar por valor máximo de post_count (incluído)
            - rls: Reglas de seguridad a aplicar (opcional)
            - session: Sesión existente (opcional)
            
        Returns:
            True si existe al menos un registro, False en caso contrario
        """
        _log_tx(session, f"[public] ❓ Verificando existencia de registros UserStats")
        records = await cls.count(
            user_id=user_id,
            in_user_id=in_user_id,
            min_user_id=min_user_id,
            max_user_id=max_user_id,
            user_name=user_name,
            in_user_name=in_user_name,
            post_count=post_count,
            in_post_count=in_post_count,
            min_post_count=min_post_count,
            max_post_count=max_post_count,
            rls=rls,
            session=session
        )
        exists_result = records > 0
        _log_commit(session, f"[public] ✅ Verificación UserStats completada: {'existe' if exists_result else 'no existe'}")
        return exists_result
    
    @classmethod
    async def as_dataframe(
        cls,
        limit: Optional[int] = None, 
        offset: Optional[int] = None,
        user_id: Optional[int] = None,
        min_user_id: Optional[int] = None,
        max_user_id: Optional[int] = None,
        user_name: Optional[str] = None,
        post_count: Optional[int] = None,
        min_post_count: Optional[int] = None,
        max_post_count: Optional[int] = None,
    ) -> DataFrame:
        """
        Busca múltiples registros estableciendo filtros y devuelve el resultado como pandas DataFrame.
        
        Args:
            limit: Límite de registros a retornar (positivo para primeros n, negativo para últimos n - requiere order_by)
            offset: Número de registros a saltar
            user_id: Filtrar por user_id
            min_user_id: Filtrar por valor mínimo de user_id (incluído)
            max_user_id: Filtrar por valor máximo de user_id (incluído)
            user_name: Filtrar por user_name
            post_count: Filtrar por post_count
            min_post_count: Filtrar por valor mínimo de post_count (incluído)
            max_post_count: Filtrar por valor máximo de post_count (incluído)
            
        Returns:
            pandas.DataFrame con los registros encontrados
            
        Raises:
            ImportError: Si pandas no está instalado
            
        Example:
            ```python
            
            # Obtener todos los registros como DataFrame
            df = db_api.userstats.as_dataframe()
            
            # Con filtros y límites
            df = db_api.userstats.as_dataframe(
                limit=100,
                user_id="valor_filtro"
            )
            
            # Análisis de datos
            print(df.describe())
            print(df.head())
            
            # Exportar a CSV
            df.to_csv('userstats_data.csv', index=False)
            ```
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError(
                "pandas no está instalado. Para usar find_as_dataframe(), instala pandas:\n"
                "pip install pandas\n"
                "o si usas poetry:\n"
                "poetry add pandas"
            )
        
        # Obtener los registros usando find_many
        records = cls.find_many(
            limit=limit,
            offset=offset,
            user_id=user_id,
            min_user_id=min_user_id,
            max_user_id=max_user_id,
            user_name=user_name,
            post_count=post_count,
            min_post_count=min_post_count,
            max_post_count=max_post_count,
        )

        # Si no hay registros, devolver DataFrame vacío con las columnas del modelo
        if not records:
            return pd.DataFrame(columns=[
                'user_id',
                'user_name',
                'post_count'
            ])

        data = [record.to_dict() for record in records]
        
        # Crear DataFrame
        df = pd.DataFrame(data)
        
        # Optimizar tipos de datos si es posible
        return cls._optimize_dataframe_dtypes(df)

    @classmethod
    async def _optimize_dataframe_dtypes(cls, df: DataFrame) -> DataFrame:
        """
        Optimiza los tipos de datos del DataFrame basándose en las columnas del modelo.
        
        Args:
            df: DataFrame a optimizar
            
        Returns:
            DataFrame con tipos de datos optimizados
        """
        try:
            import pandas as pd
        except ImportError:
            # Si pandas no está disponible, devolver el DataFrame tal como está
            return df
        
        if df.empty:
            return df
        
        # Mapeo de tipos SQLAlchemy a tipos pandas optimizados
        type_mapping = {
            'user_id': 'int64',
            'user_name': 'string',
            'post_count': 'int64'
        }
        
        # Aplicar conversiones de tipo de forma segura
        for column, target_type in type_mapping.items():
            if column in df.columns:
                try:
                    if target_type == 'int64':
                        # Manejar valores nulos en columnas enteras
                        df[column] = pd.to_numeric(df[column], errors='coerce').astype('Int64')
                    elif target_type == 'float64':
                        df[column] = pd.to_numeric(df[column], errors='coerce')
                    elif target_type == 'boolean':
                        df[column] = df[column].astype('boolean')
                    elif target_type == 'datetime64[ns]':
                        df[column] = pd.to_datetime(df[column], errors='coerce')
                    elif target_type == 'string':
                        df[column] = df[column].astype('string')
                    # 'object' se deja como está
                except Exception:
                    # Si falla la conversión, mantener el tipo original
                    continue
        
        return df



    @classmethod
    @async_error_handler
    async def sum(
        cls,
        agg_fields: List[str],
        user_id: Optional[int] = None,
        in_user_id: Optional[List[int]] = None,
        min_user_id: Optional[int] = None,
        max_user_id: Optional[int] = None,
        user_name: Optional[str] = None,
        in_user_name: Optional[List[str]] = None,
        post_count: Optional[int] = None,
        in_post_count: Optional[List[int]] = None,
        min_post_count: Optional[int] = None,
        max_post_count: Optional[int] = None,
        rls: Optional[Union[List[RLS], RLS]] = None,
        session: Optional[AsyncSession] = None
    ) -> AggregationResult:
        """
        Suma los valores de campos específicos que coincidan con los filtros.
        
        Args:
            - agg_fields: Lista de nombres de campos a sumar
            - user_id: Filtrar por user_id
            - in_user_id: Filtrar por múltiples valores de user_id (OR lógico)
            - min_user_id: Filtrar por valor mínimo de user_id (incluído)
            - max_user_id: Filtrar por valor máximo de user_id (incluído)
            - user_name: Filtrar por user_name
            - in_user_name: Filtrar por múltiples valores de user_name (OR lógico)
            - post_count: Filtrar por post_count
            - in_post_count: Filtrar por múltiples valores de post_count (OR lógico)
            - min_post_count: Filtrar por valor mínimo de post_count (incluído)
            - max_post_count: Filtrar por valor máximo de post_count (incluído)
            - rls: Reglas de seguridad a aplicar (opcional)
            - session: Sesión existente (opcional)
            
        Returns:
            AggregationResult con información detallada de la operación:
            - success: True si al menos un campo fue procesado
            - rows: Lista con una fila AggRow con las sumas {"sum_<field>": value}
            - processed_fields: Lista de campos procesados exitosamente
            - warnings: Lista de advertencias (campos no numéricos)
            - errors: Lista de errores (campos inexistentes)
            - metadata: Información adicional sobre la operación
        """
        _log_tx(session, f"[public] 🧮 Sumando campos {agg_fields} de registros UserStats con filtros aplicados")
        
        warnings = []
        errors = []
        valid_fields = []
        
        if not agg_fields:
            logger.warning(f"[public] ⚠️ No se proporcionaron campos para sumar")
            return AggregationResult(
                success=False,
                rows=[],
                processed_fields=[],
                warnings=[],
                errors=["No se proporcionaron campos para sumar"],
                metadata={"total_requested_fields": 0}
            )
        
        # Validar que los campos existen en el modelo y son de tipo válido
        for field in agg_fields:
            if hasattr(UserStats, field):
                column = getattr(UserStats, field)
                column_type = str(column.type).upper()
                # Usar validadores genéricos
                if any(valid_type in column_type for valid_type in OPERATION_TYPE_VALIDATORS['sum']):
                    valid_fields.append(field)
                else:
                    warning_msg = f"Campo '{field}' de tipo '{column_type}' no es válido para suma"
                    warnings.append(warning_msg)
                    logger.warning(f"[public] ⚠️ {warning_msg}")
            else:
                error_msg = f"Campo '{field}' no existe en modelo UserStats"
                errors.append(error_msg)
                logger.warning(f"[public] ⚠️ {error_msg}")
        
        if not valid_fields:
            logger.warning(f"[public] ⚠️ No hay campos válidos para sumar")
            return AggregationResult(
                success=False,
                rows=[],
                processed_fields=[],
                warnings=warnings,
                errors=errors,
                metadata={
                    "total_requested_fields": len(agg_fields),
                    "valid_fields_count": 0
                }
            )
        
        # Construir las expresiones de suma
        sum_expressions = []
        for field in valid_fields:
            column = getattr(UserStats, field)
            sum_expressions.append(func.sum(column).label(f"sum_{field}"))
        
        query = select(*sum_expressions)
        
        _filter = UserStatsFilter(
            user_id=user_id,
            in_user_id=in_user_id,
            min_user_id=min_user_id,
            max_user_id=max_user_id,
            user_name=user_name,
            in_user_name=in_user_name,
            post_count=post_count,
            in_post_count=in_post_count,
            min_post_count=min_post_count,
            max_post_count=max_post_count,
        )
        query = _filter.apply_to_query(query)
        filters = _filter.to_dict()
        
        # Log de parámetros aplicados
        if filters:
            _log_tx(session, f"[public]     filters={filters}")
        
        # Aplicar regla RLS (si existe)
        if rls is not None:
            query = RLSQueryApplicator.apply_rls(query, UserStats, rls)

        if session is not None:
            result = await session.execute(query)
        else:
            async with async_session_manager.get_session() as session:
                result = await session.execute(query)

        # Obtener el resultado y construir el diccionario
        row = result.first()
        sum_result = {}
        
        if row:
            for field in valid_fields:
                sum_key = f"sum_{field}"
                sum_value = getattr(row, sum_key)
                sum_result[sum_key] = float(sum_value) if sum_value is not None else None
        else:
            # Si no hay resultados, devolver None para todos los campos
            for field in valid_fields:
                sum_result[f"sum_{field}"] = None
        
        _log_commit(session, f"[public] ✅ Suma UserStats completada: {sum_result}")
        
        return AggregationResult(
            success=True,
            rows=[AggRow(group={}, data=sum_result)],
            processed_fields=valid_fields,
            warnings=warnings,
            errors=errors,
            metadata={
                "total_requested_fields": len(agg_fields),
                "valid_fields_count": len(valid_fields),
                "operation": "sum"
            }
        )
    
    @classmethod
    @async_error_handler
    async def mean(
        cls,
        agg_fields: List[str],
        user_id: Optional[int] = None,
        in_user_id: Optional[List[int]] = None,
        min_user_id: Optional[int] = None,
        max_user_id: Optional[int] = None,
        user_name: Optional[str] = None,
        in_user_name: Optional[List[str]] = None,
        post_count: Optional[int] = None,
        in_post_count: Optional[List[int]] = None,
        min_post_count: Optional[int] = None,
        max_post_count: Optional[int] = None,
        rls: Optional[Union[List[RLS], RLS]] = None,
        session: Optional[AsyncSession] = None
    ) -> AggregationResult:
        """
        Calcula la media de los valores de campos específicos que coincidan con los filtros.
        
        Args:
            - agg_fields: Lista de nombres de campos para calcular la media
            - user_id: Filtrar por user_id
            - in_user_id: Filtrar por múltiples valores de user_id (OR lógico)
            - min_user_id: Filtrar por valor mínimo de user_id (incluído)
            - max_user_id: Filtrar por valor máximo de user_id (incluído)
            - user_name: Filtrar por user_name
            - in_user_name: Filtrar por múltiples valores de user_name (OR lógico)
            - post_count: Filtrar por post_count
            - in_post_count: Filtrar por múltiples valores de post_count (OR lógico)
            - min_post_count: Filtrar por valor mínimo de post_count (incluído)
            - max_post_count: Filtrar por valor máximo de post_count (incluído)
            - rls: Reglas de seguridad a aplicar (opcional)
            - session: Sesión existente (opcional)
            
        Returns:
            AggregationResult con información detallada de la operación:
            - success: True si al menos un campo fue procesado
            - rows: Lista con una fila AggRow con las medias {"mean_<field>": value}
            - processed_fields: Lista de campos procesados exitosamente
            - warnings: Lista de advertencias (campos no numéricos)
            - errors: Lista de errores (campos inexistentes)
            - metadata: Información adicional sobre la operación
        """
        _log_tx(session, f"[public] 📊 Calculando media de campos {agg_fields} de registros UserStats con filtros aplicados")
        
        warnings = []
        errors = []
        valid_fields = []
        
        if not agg_fields:
            logger.warning(f"[public] ⚠️ No se proporcionaron campos para calcular la media")
            return AggregationResult(
                success=False,
                rows=[],
                processed_fields=[],
                warnings=[],
                errors=["No se proporcionaron campos para calcular la media"],
                metadata={"total_requested_fields": 0}
            )
        
        # Validar que los campos existen en el modelo y son de tipo válido
        for field in agg_fields:
            if hasattr(UserStats, field):
                column = getattr(UserStats, field)
                column_type = str(column.type).upper()
                # Usar validadores genéricos
                if any(valid_type in column_type for valid_type in OPERATION_TYPE_VALIDATORS['mean']):
                    valid_fields.append(field)
                else:
                    warning_msg = f"Campo '{field}' de tipo '{column_type}' no es válido para media"
                    warnings.append(warning_msg)
                    logger.warning(f"[public] ⚠️ {warning_msg}")
            else:
                error_msg = f"Campo '{field}' no existe en modelo UserStats"
                errors.append(error_msg)
                logger.warning(f"[public] ⚠️ {error_msg}")
        
        if not valid_fields:
            logger.warning(f"[public] ⚠️ No hay campos válidos para calcular la media")
            return AggregationResult(
                success=False,
                rows=[],
                processed_fields=[],
                warnings=warnings,
                errors=errors,
                metadata={
                    "total_requested_fields": len(agg_fields),
                    "valid_fields_count": 0
                }
            )
        
        # Construir las expresiones de media
        mean_expressions = []
        for field in valid_fields:
            column = getattr(UserStats, field)
            mean_expressions.append(func.avg(column).label(f"mean_{field}"))
        
        query = select(*mean_expressions)
        
        _filter = UserStatsFilter(
            user_id=user_id,
            in_user_id=in_user_id,
            min_user_id=min_user_id,
            max_user_id=max_user_id,
            user_name=user_name,
            in_user_name=in_user_name,
            post_count=post_count,
            in_post_count=in_post_count,
            min_post_count=min_post_count,
            max_post_count=max_post_count,
        )
        query = _filter.apply_to_query(query)
        filters = _filter.to_dict()
        
        # Log de parámetros aplicados
        if filters:
            _log_tx(session, f"[public]     filters={filters}")

        # Aplicar regla RLS (si existe)
        if rls is not None:
            query = RLSQueryApplicator.apply_rls(query, UserStats, rls)

        if session is not None:
            result = await session.execute(query)
        else:
            async with async_session_manager.get_session() as session:
                result = await session.execute(query)

        # Obtener el resultado y construir el diccionario
        row = result.first()
        mean_result = {}
        
        if row:
            for field in valid_fields:
                mean_key = f"mean_{field}"
                mean_value = getattr(row, mean_key)
                mean_result[mean_key] = float(mean_value) if mean_value is not None else None
        else:
            # Si no hay resultados, devolver None para todos los campos
            for field in valid_fields:
                mean_result[f"mean_{field}"] = None
        
        _log_commit(session, f"[public] ✅ Media UserStats completada: {mean_result}")
        
        return AggregationResult(
            success=True,
            rows=[AggRow(group={}, data=mean_result)],
            processed_fields=valid_fields,
            warnings=warnings,
            errors=errors,
            metadata={
                "total_requested_fields": len(agg_fields),
                "valid_fields_count": len(valid_fields),
                "operation": "mean"
            }
        )
    
    @classmethod
    @async_error_handler
    async def max(
        cls,
        agg_fields: List[str],
        user_id: Optional[int] = None,
        in_user_id: Optional[List[int]] = None,
        min_user_id: Optional[int] = None,
        max_user_id: Optional[int] = None,
        user_name: Optional[str] = None,
        in_user_name: Optional[List[str]] = None,
        post_count: Optional[int] = None,
        in_post_count: Optional[List[int]] = None,
        min_post_count: Optional[int] = None,
        max_post_count: Optional[int] = None,
        rls: Optional[Union[List[RLS], RLS]] = None,
        session: Optional[AsyncSession] = None
    ) -> AggregationResult:
        """
        Encuentra el valor máximo de campos específicos que coincidan con los filtros.
        
        Args:
            - agg_fields: Lista de nombres de campos para encontrar el máximo
            - user_id: Filtrar por user_id
            - in_user_id: Filtrar por múltiples valores de user_id (OR lógico)
            - min_user_id: Filtrar por valor mínimo de user_id (incluído)
            - max_user_id: Filtrar por valor máximo de user_id (incluído)
            - user_name: Filtrar por user_name
            - in_user_name: Filtrar por múltiples valores de user_name (OR lógico)
            - post_count: Filtrar por post_count
            - in_post_count: Filtrar por múltiples valores de post_count (OR lógico)
            - min_post_count: Filtrar por valor mínimo de post_count (incluído)
            - max_post_count: Filtrar por valor máximo de post_count (incluído)
            - session: Sesión existente (opcional)
            
        Returns:
            AggregationResult con información detallada de la operación:
            - success: True si al menos un campo fue procesado
            - rows: Lista con una fila AggRow con los máximos {"max_<field>": value}
            - processed_fields: Lista de campos procesados exitosamente
            - warnings: Lista de advertencias (campos no válidos)
            - errors: Lista de errores (campos inexistentes)
            - metadata: Información adicional sobre la operación
        """
        _log_tx(session, f"[public] 🔺 Calculando máximo de campos {agg_fields} de registros UserStats con filtros aplicados")
        
        warnings = []
        errors = []
        valid_fields = []
        field_types = {}  # Trackear el tipo de cada campo para parsear el resultado
        
        if not agg_fields:
            logger.warning(f"[public] ⚠️ No se proporcionaron campos para calcular el máximo")
            return AggregationResult(
                success=False,
                rows=[],
                processed_fields=[],
                warnings=[],
                errors=["No se proporcionaron campos para calcular el máximo"],
                metadata={"total_requested_fields": 0}
            )
        
        # Validar que los campos existen en el modelo y son de tipo válido
        for field in agg_fields:
            if hasattr(UserStats, field):
                column = getattr(UserStats, field)
                column_type = str(column.type).upper()
                # Usar validadores genéricos
                if any(valid_type in column_type for valid_type in OPERATION_TYPE_VALIDATORS['max']):
                    # Determinar el tipo del campo
                    if any(num_type in column_type for num_type in ['INTEGER', 'FLOAT', 'NUMERIC', 'DECIMAL', 'DOUBLE', 'REAL', 'BIGINT', 'SMALLINT', 'TINYINT']):
                        field_types[field] = 'numeric'
                    elif any(date_type in column_type for date_type in ['DATETIME', 'TIMESTAMP', 'DATE', 'TIME']):
                        field_types[field] = 'datetime'
                    valid_fields.append(field)
                else:
                    warning_msg = f"Campo '{field}' de tipo '{column_type}' no es válido para máximo"
                    warnings.append(warning_msg)
                    logger.warning(f"[public] ⚠️ {warning_msg}")
            else:
                error_msg = f"Campo '{field}' no existe en modelo UserStats"
                errors.append(error_msg)
                logger.warning(f"[public] ⚠️ {error_msg}")
        
        if not valid_fields:
            logger.warning(f"[public] ⚠️ No hay campos válidos para calcular el máximo")
            return AggregationResult(
                success=False,
                rows=[],
                processed_fields=[],
                warnings=warnings,
                errors=errors,
                metadata={
                    "total_requested_fields": len(agg_fields),
                    "valid_fields_count": 0
                }
            )
        
        # Construir las expresiones de máximo
        max_expressions = []
        for field in valid_fields:
            column = getattr(UserStats, field)
            max_expressions.append(func.max(column).label(f"max_{field}"))
        
        query = select(*max_expressions)
        
        _filter = UserStatsFilter(
            user_id=user_id,
            in_user_id=in_user_id,
            min_user_id=min_user_id,
            max_user_id=max_user_id,
            user_name=user_name,
            in_user_name=in_user_name,
            post_count=post_count,
            in_post_count=in_post_count,
            min_post_count=min_post_count,
            max_post_count=max_post_count,
        )
        query = _filter.apply_to_query(query)
        filters = _filter.to_dict()
        
        # Log de parámetros aplicados
        if filters:
            _log_tx(session, f"[public]     filters={filters}")
        
        # Aplicar regla RLS (si existe)
        if rls is not None:
            query = RLSQueryApplicator.apply_rls(query, UserStats, rls)

        if session is not None:
            result = await session.execute(query)
        else:
            async with async_session_manager.get_session() as session:
                result = await session.execute(query)

        # Obtener el resultado y construir el diccionario
        row = result.first()
        max_result = {}
        
        if row:
            for field in valid_fields:
                max_key = f"max_{field}"
                max_value = getattr(row, max_key)
                if max_value is not None:
                    # Parsear según el tipo de campo
                    if field_types[field] == 'numeric':
                        max_result[max_key] = float(max_value)
                    elif field_types[field] == 'datetime':
                        max_result[max_key] = max_value.isoformat() if hasattr(max_value, 'isoformat') else str(max_value)
                else:
                    max_result[max_key] = None
        else:
            # Si no hay resultados, devolver None para todos los campos
            for field in valid_fields:
                max_result[f"max_{field}"] = None
        
        _log_commit(session, f"[public] ✅ Máximo UserStats completado: {max_result}")
        
        return AggregationResult(
            success=True,
            rows=[AggRow(group={}, data=max_result)],
            processed_fields=valid_fields,
            warnings=warnings,
            errors=errors,
            metadata={
                "total_requested_fields": len(agg_fields),
                "valid_fields_count": len(valid_fields),
                "field_types": field_types,
                "operation": "max"
            }
        )
    
    @classmethod
    @async_error_handler
    async def min(
        cls,
        agg_fields: List[str],
        user_id: Optional[int] = None,
        in_user_id: Optional[List[int]] = None,
        min_user_id: Optional[int] = None,
        max_user_id: Optional[int] = None,
        user_name: Optional[str] = None,
        in_user_name: Optional[List[str]] = None,
        post_count: Optional[int] = None,
        in_post_count: Optional[List[int]] = None,
        min_post_count: Optional[int] = None,
        max_post_count: Optional[int] = None,
        rls: Optional[Union[List[RLS], RLS]] = None,
        session: Optional[AsyncSession] = None
    ) -> AggregationResult:
        """
        Encuentra el valor mínimo de campos específicos que coincidan con los filtros.
        
        Args:
            - agg_fields: Lista de nombres de campos para encontrar el mínimo
            - user_id: Filtrar por user_id
            - in_user_id: Filtrar por múltiples valores de user_id (OR lógico)
            - min_user_id: Filtrar por valor mínimo de user_id (incluído)
            - max_user_id: Filtrar por valor máximo de user_id (incluído)
            - user_name: Filtrar por user_name
            - in_user_name: Filtrar por múltiples valores de user_name (OR lógico)
            - post_count: Filtrar por post_count
            - in_post_count: Filtrar por múltiples valores de post_count (OR lógico)
            - min_post_count: Filtrar por valor mínimo de post_count (incluído)
            - max_post_count: Filtrar por valor máximo de post_count (incluído)
            - rls: Reglas de seguridad a aplicar (opcional)
            - session: Sesión existente (opcional)
            
        Returns:
            AggregationResult con información detallada de la operación:
            - success: True si al menos un campo fue procesado
            - rows: Lista con una fila AggRow con los mínimos {"min_<field>": value}
            - processed_fields: Lista de campos procesados exitosamente
            - warnings: Lista de advertencias (campos no válidos)
            - errors: Lista de errores (campos inexistentes)
            - metadata: Información adicional sobre la operación
        """
        _log_tx(session, f"[public] 🔻 Calculando mínimo de campos {agg_fields} de registros UserStats con filtros aplicados")
        
        warnings = []
        errors = []
        valid_fields = []
        field_types = {}  # Trackear el tipo de cada campo para parsear el resultado
        
        if not agg_fields:
            logger.warning(f"[public] ⚠️ No se proporcionaron campos para calcular el mínimo")
            return AggregationResult(
                success=False,
                rows=[],
                processed_fields=[],
                warnings=[],
                errors=["No se proporcionaron campos para calcular el mínimo"],
                metadata={"total_requested_fields": 0}
            )
        
        # Validar que los campos existen en el modelo y son de tipo válido
        for field in agg_fields:
            if hasattr(UserStats, field):
                column = getattr(UserStats, field)
                column_type = str(column.type).upper()
                # Usar validadores genéricos
                if any(valid_type in column_type for valid_type in OPERATION_TYPE_VALIDATORS['min']):
                    # Determinar el tipo del campo
                    if any(num_type in column_type for num_type in ['INTEGER', 'FLOAT', 'NUMERIC', 'DECIMAL', 'DOUBLE', 'REAL', 'BIGINT', 'SMALLINT', 'TINYINT']):
                        field_types[field] = 'numeric'
                    elif any(date_type in column_type for date_type in ['DATETIME', 'TIMESTAMP', 'DATE', 'TIME']):
                        field_types[field] = 'datetime'
                    valid_fields.append(field)
                else:
                    warning_msg = f"Campo '{field}' de tipo '{column_type}' no es válido para mínimo"
                    warnings.append(warning_msg)
                    logger.warning(f"[public] ⚠️ {warning_msg}")
            else:
                error_msg = f"Campo '{field}' no existe en modelo UserStats"
                errors.append(error_msg)
                logger.warning(f"[public] ⚠️ {error_msg}")
        
        if not valid_fields:
            logger.warning(f"[public] ⚠️ No hay campos válidos para calcular el mínimo")
            return AggregationResult(
                success=False,
                rows=[],
                processed_fields=[],
                warnings=warnings,
                errors=errors,
                metadata={
                    "total_requested_fields": len(agg_fields),
                    "valid_fields_count": 0
                }
            )
        
        # Construir las expresiones de mínimo
        min_expressions = []
        for field in valid_fields:
            column = getattr(UserStats, field)
            min_expressions.append(func.min(column).label(f"min_{field}"))
        
        query = select(*min_expressions)
        
        _filter = UserStatsFilter(
            user_id=user_id,
            in_user_id=in_user_id,
            min_user_id=min_user_id,
            max_user_id=max_user_id,
            user_name=user_name,
            in_user_name=in_user_name,
            post_count=post_count,
            in_post_count=in_post_count,
            min_post_count=min_post_count,
            max_post_count=max_post_count,
        )
        query = _filter.apply_to_query(query)
        filters = _filter.to_dict()
        
        # Log de parámetros aplicados
        if filters:
            _log_tx(session, f"[public]     filters={filters}")

        # Aplicar regla RLS (si existe)
        if rls is not None:
            query = RLSQueryApplicator.apply_rls(query, UserStats, rls)

        if session is not None:
            result = await session.execute(query)
        else:
            async with async_session_manager.get_session() as session:
                result = await session.execute(query)

        # Obtener el resultado y construir el diccionario
        row = result.first()
        min_result = {}
        
        if row:
            for field in valid_fields:
                min_key = f"min_{field}"
                min_value = getattr(row, min_key)
                if min_value is not None:
                    # Parsear según el tipo de campo
                    if field_types[field] == 'numeric':
                        min_result[min_key] = float(min_value)
                    elif field_types[field] == 'datetime':
                        min_result[min_key] = min_value.isoformat() if hasattr(min_value, 'isoformat') else str(min_value)
                else:
                    min_result[min_key] = None
        else:
            # Si no hay resultados, devolver None para todos los campos
            for field in valid_fields:
                min_result[f"min_{field}"] = None
        
        _log_commit(session, f"[public] ✅ Mínimo UserStats completado: {min_result}")
        
        return AggregationResult(
            success=True,
            rows=[AggRow(group={}, data=min_result)],
            processed_fields=valid_fields,
            warnings=warnings,
            errors=errors,
            metadata={
                "total_requested_fields": len(agg_fields),
                "valid_fields_count": len(valid_fields),
                "field_types": field_types,
                "operation": "min"
            }
        )
    
    @classmethod
    @async_error_handler
    async def agg(
        cls,
        request: AggRequest,
        user_id: Optional[int] = None,
        in_user_id: Optional[List[int]] = None,
        min_user_id: Optional[int] = None,
        max_user_id: Optional[int] = None,
        user_name: Optional[str] = None,
        in_user_name: Optional[List[str]] = None,
        post_count: Optional[int] = None,
        in_post_count: Optional[List[int]] = None,
        min_post_count: Optional[int] = None,
        max_post_count: Optional[int] = None,
        verbose: bool = False,
        rls: Optional[Union[List[RLS], RLS]] = None,
        session: Optional[AsyncSession] = None
    ) -> AggregationResult:
        """
        Realiza múltiples operaciones de agregación en una sola consulta, con GROUP BY opcional.

        Args:
            - request: AggRequest con las operaciones a calcular y los campos de agrupación.
                       Ejemplo sin GROUP BY:
                           AggRequest(aggregations={"sum": ["price"], "count": ["id"]})
                       Ejemplo con GROUP BY:
                           AggRequest(
                               aggregations={"sum": [AggField(expr="revenue-cost", alias="profit")]},
                               group_by=["status", GroupByField(field="created_at", trunc=DatetimeTrunc.month)]
                           )
            - user_id: Filtrar por user_id
            - in_user_id: Filtrar por múltiples valores de user_id (OR lógico)
            - min_user_id: Filtrar por valor mínimo de user_id (incluído)
            - max_user_id: Filtrar por valor máximo de user_id (incluído)
            - user_name: Filtrar por user_name
            - in_user_name: Filtrar por múltiples valores de user_name (OR lógico)
            - post_count: Filtrar por post_count
            - in_post_count: Filtrar por múltiples valores de post_count (OR lógico)
            - min_post_count: Filtrar por valor mínimo de post_count (incluído)
            - max_post_count: Filtrar por valor máximo de post_count (incluído)
            - verbose: Si True, emite logs detallados de cada campo, expresión y fila procesada.
            - rls: Reglas de seguridad a aplicar (opcional)
            - session: Sesión existente (opcional).

        Returns:
            AggregationResult:
            - Sin GROUP BY: rows contiene una sola fila con group={}.
            - Con GROUP BY: rows contiene una fila por combinación de valores de agrupación.

        Examples:
            ```python
            # Agregación global
            result = dao.agg(
                AggRequest(aggregations={"sum": ["price"], "count": ["id"]}),
                status="active"
            )
            result.rows[0].data  # {"sum_price": 1000.0, "count_id": 50}

            # Con GROUP BY por campo discreto
            result = dao.agg(AggRequest(
                aggregations={"sum": ["revenue"], "count": ["id"]},
                group_by=["status"]
            ))
            for row in result.rows:
                print(row.group, row.data)

            # Con GROUP BY por datetime truncado al mes
            result = dao.agg(AggRequest(
                aggregations={"sum": [AggField(expr="revenue-cost", alias="profit")]},
                group_by=[GroupByField(field="created_at", trunc=DatetimeTrunc.month)]
            ))
            ```
        """
        _log_tx(session, f"[public] 🎯 Realizando agregaciones en UserStats: {list(request.aggregations.keys())}")
        if verbose:
            _log_tx(session, f"[public]   aggregations={dict(request.aggregations)}, group_by={request.group_by}")

        warnings = []
        errors = []
        all_valid_fields = []
        operations_metadata = {}

        if not request.aggregations:
            logger.warning(f"[public] ⚠️ No se proporcionaron operaciones de agregación")
            return AggregationResult(
                success=False,
                rows=[],
                group_by=[],
                processed_fields=[],
                errors=["No se proporcionaron operaciones de agregación"],
                metadata={"total_operations": 0}
            )

        # ── 1. Construir expresiones de agregación ────────────────────────────
        agg_expressions = []

        for operation, fields in request.aggregations.items():
            if operation not in OPERATION_TYPE_VALIDATORS:
                error_msg = f"Operación '{operation}' no soportada. Válidas: {list(OPERATION_TYPE_VALIDATORS.keys())}"
                errors.append(error_msg)
                logger.warning(f"[public] ⚠️ {error_msg}")
                continue

            if not fields:
                warnings.append(f"No se proporcionaron campos para la operación '{operation}'")
                continue

            valid_fields_for_operation = []
            field_types_for_operation  = {}
            field_label_mapping        = {}

            for field in fields:
                try:
                    # Normalizar a (expression, alias)
                    if isinstance(field, AggField):
                        expression = field.expr
                        alias      = field.alias
                    else:
                        expression = str(field)
                        alias      = None

                    is_expression = any(op in expression for op in ['+', '-', '*', '/', '%', '(', ')'])

                    if is_expression:
                        try:
                            column_expr = ExpressionParser.parse(expression, UserStats)
                            if alias:
                                field_key  = alias
                                label_name = f"{operation}_{alias}"
                            else:
                                clean_expr = ExpressionParser.get_field_name(expression)
                                field_key  = clean_expr
                                label_name = f"{operation}_{clean_expr}"

                            valid_fields_for_operation.append(field_key)
                            all_valid_fields.append(field_key)
                            field_label_mapping[field_key] = label_name
                            sql_func = OPERATION_FUNCTIONS[operation]
                            agg_expressions.append(sql_func(column_expr).label(label_name))
                            if operation in ['max', 'min']:
                                field_types_for_operation[field_key] = 'numeric'
                            if verbose:
                                _log_tx(session, f"[public]   ✓ [{operation}] expr='{expression}' → label='{label_name}'")
                        except ValueError as e:
                            error_msg = f"Error al parsear expresión '{expression}': {str(e)}"
                            errors.append(error_msg)
                            logger.warning(f"[public] ⚠️ {error_msg}")
                    else:
                        if hasattr(UserStats, expression):
                            column      = getattr(UserStats, expression)
                            column_type = str(column.type).upper()

                            if any(valid_type in column_type for valid_type in OPERATION_TYPE_VALIDATORS[operation]):
                                if alias:
                                    field_key  = alias
                                    label_name = f"{operation}_{alias}"
                                else:
                                    field_key  = expression
                                    label_name = f"{operation}_{expression}"

                                valid_fields_for_operation.append(field_key)
                                all_valid_fields.append(field_key)
                                field_label_mapping[field_key] = label_name

                                if operation in ['max', 'min']:
                                    if any(t in column_type for t in ['INTEGER', 'FLOAT', 'NUMERIC', 'DECIMAL', 'DOUBLE', 'REAL', 'BIGINT', 'SMALLINT', 'TINYINT']):
                                        field_types_for_operation[field_key] = 'numeric'
                                    elif any(t in column_type for t in ['DATETIME', 'TIMESTAMP', 'DATE', 'TIME']):
                                        field_types_for_operation[field_key] = 'datetime'

                                sql_func = OPERATION_FUNCTIONS[operation]
                                agg_expressions.append(sql_func(column).label(label_name))
                                if verbose:
                                    _log_tx(session, f"[public]   ✓ [{operation}] campo='{expression}' tipo={column_type} → label='{label_name}'")
                            else:
                                warnings.append(f"Campo '{expression}' de tipo '{column_type}' no es válido para operación '{operation}'")
                                if verbose:
                                    _log_tx(session, f"[public]   ✗ [{operation}] campo='{expression}' tipo={column_type} incompatible con la operación")
                        else:
                            errors.append(f"Campo '{expression}' no existe en modelo UserStats")

                except Exception as e:
                    errors.append(f"Error inesperado procesando campo '{field}': {str(e)}")

            if valid_fields_for_operation:
                operations_metadata[operation] = {
                    "requested_fields": [f.expr if isinstance(f, AggField) else str(f) for f in fields],
                    "valid_fields":      valid_fields_for_operation,
                    "field_label_mapping": field_label_mapping,
                    "valid_count":       len(valid_fields_for_operation),
                    "invalid_count":     len(fields) - len(valid_fields_for_operation),
                }
                if operation in ['max', 'min'] and field_types_for_operation:
                    operations_metadata[operation]["field_types"] = field_types_for_operation

        if not agg_expressions:
            logger.warning(f"[public] ⚠️ No hay operaciones de agregación válidas")
            return AggregationResult(
                success=False,
                rows=[],
                group_by=[],
                processed_fields=[],
                warnings=warnings,
                errors=errors,
                metadata={"total_operations": len(request.aggregations), "valid_operations": 0, "total_expressions": 0, "operations_summary": operations_metadata}
            )

        # ── 2. Validar y construir expresiones de GROUP BY ────────────────────
        group_select_exprs = []   # van al SELECT con label
        group_raw_exprs    = []   # van al GROUP BY sin label
        group_keys         = []   # claves en AggRow.group
        group_field_names  = []   # nombres de campo originales para AggregationResult.group_by

        if request.group_by:
            for gb_item in request.group_by:
                gb_field = gb_item if isinstance(gb_item, GroupByField) else GroupByField(field=gb_item)
                field_name = gb_field.field

                if not hasattr(UserStats, field_name):
                    errors.append(f"Campo de group_by '{field_name}' no existe en modelo UserStats")
                    continue

                column      = getattr(UserStats, field_name)
                column_type = str(column.type).upper()

                if any(t in column_type for t in GROUP_BY_FORBIDDEN_TYPES):
                    errors.append(f"Campo '{field_name}' es de tipo '{column_type}': los tipos continuos no están permitidos en group_by")
                    continue

                is_datetime = any(t in column_type for t in GROUP_BY_DATETIME_TYPES)

                if is_datetime:
                    if gb_field.trunc is None:
                        errors.append(f"Campo '{field_name}' es de tipo DATETIME/TIMESTAMP: 'trunc' es obligatorio en GroupByField")
                        continue
                    trunc_value  = gb_field.trunc.value
                    group_key    = f"{field_name}_{trunc_value}"
                    # Intervalos personalizados usan date_bin; estándar usan date_trunc
                    _CUSTOM_TRUNC_INTERVALS = {
                        "15min": "15 minutes",
                        "30min": "30 minutes",
                        "3h":    "3 hours",
                        "6h":    "6 hours",
                        "12h":   "12 hours",
                    }
                    if trunc_value in _CUSTOM_TRUNC_INTERVALS:
                        interval_str = _CUSTOM_TRUNC_INTERVALS[trunc_value]
                        raw_expr = func.date_bin(
                            text(f"interval '{interval_str}'"),
                            column,
                            text("timestamp '2001-01-01'")
                        )
                    else:
                        raw_expr = func.date_trunc(trunc_value, column)
                    select_expr  = raw_expr.label(group_key)
                else:
                    if gb_field.trunc is not None:
                        warnings.append(f"Campo '{field_name}' no es DATETIME/TIMESTAMP: se ignora trunc='{gb_field.trunc.value}'")
                    group_key    = field_name
                    raw_expr     = column
                    select_expr  = column.label(group_key)

                group_select_exprs.append(select_expr)
                group_raw_exprs.append(raw_expr)
                group_keys.append(group_key)
                group_field_names.append(field_name)
                if verbose:
                    if is_datetime:
                        _log_tx(session, f"[public]   GROUP BY '{field_name}' (datetime, trunc='{trunc_value}') → key='{group_key}'")
                    else:
                        _log_tx(session, f"[public]   GROUP BY '{field_name}' (tipo={column_type}) → key='{group_key}'")

            # Si se solicitó group_by pero todos fallaron, abortar
            if not group_select_exprs:
                logger.warning(f"[public] ⚠️ Todos los campos de group_by son inválidos")
                return AggregationResult(
                    success=False,
                    rows=[],
                    group_by=[],
                    processed_fields=[],
                    warnings=warnings,
                    errors=errors,
                    metadata={"total_operations": len(request.aggregations), "valid_operations": len(operations_metadata), "total_expressions": len(agg_expressions), "operations_summary": operations_metadata}
                )

        # ── 3. Construir y ejecutar query ─────────────────────────────────────
        query = select(*agg_expressions, *group_select_exprs)

        # Filters
        _filter = UserStatsFilter(
            user_id=user_id,
            in_user_id=in_user_id,
            min_user_id=min_user_id,
            max_user_id=max_user_id,
            user_name=user_name,
            in_user_name=in_user_name,
            post_count=post_count,
            in_post_count=in_post_count,
            min_post_count=min_post_count,
            max_post_count=max_post_count,
        )
        query = _filter.apply_to_query(query)
        filters = _filter.to_dict()

        if filters:
            _log_tx(session, f"[public]     filters={filters}")
        
        # Aplicar regla RLS (si existe)
        if rls is not None:
            query = RLSQueryApplicator.apply_rls(query, UserStats, rls)

        if group_raw_exprs:
            query = query.group_by(*group_raw_exprs)

        # ── ORDER BY / LIMIT ──────────────────────────────────────────────────
        if request.order_by:
            order_clauses = []
            for order_item in request.order_by:
                op_meta = operations_metadata.get(order_item.operation)
                if op_meta is None:
                    warnings.append(f"order_by: operación '{order_item.operation}' no está en las agregaciones solicitadas")
                    continue
                label_name = op_meta.get("field_label_mapping", {}).get(order_item.field)
                if label_name is None:
                    warnings.append(f"order_by: campo '{order_item.field}' no encontrado en operación '{order_item.operation}'")
                    continue
                col = literal_column(label_name)
                order_clauses.append(col.desc() if order_item.direction == "desc" else col.asc())
                if verbose:
                    _log_tx(session, f"[public]   ORDER BY '{label_name}' {order_item.direction.upper()}")
            if order_clauses:
                query = query.order_by(*order_clauses)

        if request.limit is not None:
            query = query.limit(request.limit)
            if verbose:
                _log_tx(session, f"[public]   LIMIT {request.limit}")

        if session is not None:
            result = await session.execute(query)
        else:
            async with async_session_manager.get_session() as session:
                result = await session.execute(query)

        # ── 4. Construir AggRow por cada fila del resultado ───────────────────
        db_rows  = result.all()
        agg_rows = []

        def _extract_row_data(row) -> Dict[str, Any]:
            row_data = {}
            for operation, op_meta in operations_metadata.items():
                lmap = op_meta.get("field_label_mapping", {})
                for field in op_meta["valid_fields"]:
                    label_name   = lmap.get(field, f"{operation}_{field}")
                    result_value = getattr(row, label_name, None)
                    result_key   = f"{operation}_{field}"
                    if result_value is not None:
                        if operation == 'count':
                            row_data[result_key] = int(result_value)
                        elif operation in ['max', 'min'] and 'field_types' in op_meta:
                            if op_meta['field_types'].get(field) == 'datetime':
                                row_data[result_key] = result_value.isoformat() if hasattr(result_value, 'isoformat') else str(result_value)
                            else:
                                row_data[result_key] = float(result_value)
                        elif operation in ['sum', 'mean']:
                            row_data[result_key] = float(result_value)
                        else:
                            row_data[result_key] = result_value
                    else:
                        row_data[result_key] = 0 if operation == 'count' else None
            return row_data

        if db_rows:
            for row in db_rows:
                group_data = {key: getattr(row, key, None) for key in group_keys}
                agg_row = AggRow(group=group_data, data=_extract_row_data(row))
                agg_rows.append(agg_row)
                if verbose:
                    _log_tx(session, f"[public]   → AggRow group={agg_row.group} data={agg_row.data}")
        else:
            # Sin resultados: una fila vacía para queries sin group_by, ninguna para grouped
            if not group_raw_exprs:
                empty_data = {f"{op}_{f}": (0 if op == 'count' else None) for op, m in operations_metadata.items() for f in m["valid_fields"]}
                agg_rows.append(AggRow(group={}, data=empty_data))

        _log_commit(session, f"[public] ✅ Agregaciones UserStats completadas: {len(agg_expressions)} expresiones, {len(agg_rows)} filas")

        return AggregationResult(
            success=True,
            rows=agg_rows,
            group_by=group_field_names,
            processed_fields=all_valid_fields,
            warnings=warnings,
            errors=errors,
            metadata={
                "total_operations":  len(request.aggregations),
                "valid_operations":  len(operations_metadata),
                "total_expressions": len(agg_expressions),
                "operations_summary": operations_metadata,
            }
        )
