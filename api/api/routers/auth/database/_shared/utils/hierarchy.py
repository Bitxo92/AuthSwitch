# Este archivo ha sido generado automáticamente por tai-sql
# No modifiques este archivo directamente

"""
Hierarchy utilities — CTE-based recursive queries for self-referencing tables.

Provides `HierarchyResolver`, a reusable engine that builds PostgreSQL
WITH RECURSIVE queries and assembles nested tree structures from flat results.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from sqlalchemy import literal, select
from sqlalchemy.orm import Session, aliased
from sqlalchemy.ext.asyncio import AsyncSession
from .funcs import get_loading_options

from tai_alphi import Alphi

logger = Alphi.get_logger_by_name("tai-sql")


# ─────────────────────────────────────────────────────────────────────────────
# Types
# ─────────────────────────────────────────────────────────────────────────────

T = TypeVar("T")  # SQLAlchemy model type
D = TypeVar("D")  # DTO type


class TreeMode(str, Enum):
    """Modos de consulta jerárquica."""
    FLAT = "flat"
    DESCENDANTS = "descendants"
    ANCESTORS = "ancestors"
    FULL_TREE = "full_tree"


@dataclass(frozen=True)
class HierarchyConfig:
    """
    Configuración inmutable de la jerarquía para un modelo.

    Attributes:
        model_class: La clase SQLAlchemy del modelo.
        pk_column: Nombre de la columna PK (ej: 'id_equipo').
        parent_column: Nombre de la columna que referencia al padre (ej: 'equipo_superior').
    """
    model_class: Any
    pk_column: str
    parent_column: str

    @property
    def pk_attr(self):
        """Atributo SQLAlchemy de la PK."""
        return getattr(self.model_class, self.pk_column)

    @property
    def parent_attr(self):
        """Atributo SQLAlchemy de la columna padre."""
        return getattr(self.model_class, self.parent_column)


@dataclass
class TreeNode(Generic[D]):
    """
    Nodo del árbol con DTO y metadatos de profundidad.

    Attributes:
        dto: El DTO de lectura del registro.
        pk: Valor de la PK del nodo.
        parent_ref: Valor de la referencia al padre (None si es raíz).
        level: Profundidad en el árbol (0 = nodo raíz de la consulta).
    """
    dto: D
    pk: Any
    parent_ref: Any
    level: int = 0


# ─────────────────────────────────────────────────────────────────────────────
# HierarchyResolver
# ─────────────────────────────────────────────────────────────────────────────

class HierarchyResolver(Generic[T, D]):
    """
    Motor de consultas jerárquicas basado en CTEs recursivos.

    Uso desde el DAO generado:

        resolver = HierarchyResolver(
            config=HierarchyConfig(Equipo, 'id_equipo', 'equipo_superior'),
            dto_factory=lambda instance, includes, max_depth: EquipoRead.from_instance(instance, includes, max_depth),
        )

        results = resolver.resolve(
            session=session,
            root_ids=['E87-00927'],
            mode=TreeMode.DESCENDANTS,
            max_depth=None,
            includes=['componentes'],
            dto_max_depth=5,
        )

    El resolver:
    1. Construye un CTE recursivo (descendants, ancestors, o ambos).
    2. Ejecuta la query y obtiene filas planas con _tree_level.
    3. Ensambla la estructura anidada (descendants/ancestors en cada DTO).
    """

    __slots__ = ('config', 'dto_factory')

    def __init__(
        self,
        config: HierarchyConfig,
        dto_factory: Callable[..., D],
    ):
        self.config = config
        self.dto_factory = dto_factory

    # ── Public API ───────────────────────────────────────────────────────

    def resolve(
        self,
        session: Session,
        root_ids: List[Any],
        mode: TreeMode,
        max_depth: Optional[int] = None,
        includes: Optional[List[str]] = None,
        dto_max_depth: int = 5,
    ) -> List[D]:
        """
        Ejecuta la consulta jerárquica y retorna DTOs con árbol anidado.

        Args:
            session: Sesión SQLAlchemy activa.
            root_ids: PKs de los nodos raíz.
            mode: Modo de consulta (descendants, ancestors, full_tree).
            max_depth: Profundidad máxima de recursión (None = ilimitada).
            includes: Relaciones a incluir en from_instance.
            dto_max_depth: max_depth para from_instance.

        Returns:
            Lista de DTOs raíz con descendants/ancestors poblados.
        """
        if not root_ids:
            return []

        desc_rows: List[Tuple[Any, int]] = []
        anc_rows: List[Tuple[Any, int]] = []

        if mode in (TreeMode.DESCENDANTS, TreeMode.FULL_TREE):
            desc_rows = self._fetch_descendants(session, root_ids, max_depth, includes)

        if mode in (TreeMode.ANCESTORS, TreeMode.FULL_TREE):
            anc_rows = self._fetch_ancestors(session, root_ids, max_depth, includes)

        # Build nested structures
        root_id_set = set(root_ids)

        if mode == TreeMode.DESCENDANTS:
            return self._build_descendant_tree(desc_rows, root_id_set, includes, dto_max_depth)
        elif mode == TreeMode.ANCESTORS:
            return self._build_ancestor_chain(anc_rows, root_id_set, includes, dto_max_depth)
        else:
            # full_tree: merge both directions
            desc_dtos = self._build_descendant_tree(desc_rows, root_id_set, includes, dto_max_depth)
            anc_dtos = self._build_ancestor_chain(anc_rows, root_id_set, includes, dto_max_depth)

            # Attach ancestors to each root
            anc_by_pk = {
                getattr(dto, self.config.pk_column): dto
                for dto in anc_dtos
            }
            for dto in desc_dtos:
                root_pk = getattr(dto, self.config.pk_column)
                if root_pk in anc_by_pk:
                    dto.ancestors = anc_by_pk[root_pk].ancestors

            return desc_dtos

    async def resolve_async(
        self,
        session: AsyncSession,
        root_ids: List[Any],
        mode: TreeMode,
        max_depth: Optional[int] = None,
        includes: Optional[List[str]] = None,
        dto_max_depth: int = 5,
    ) -> List[D]:
        """Versión async de resolve."""
        if not root_ids:
            return []

        # Compute loading options up-front so CTE rows arrive with relationships
        # already populated — avoids greenlet context errors in async path.
        _loading_opts = get_loading_options(self.config.model_class, includes) if includes else []

        desc_rows: List[Tuple[Any, int]] = []
        anc_rows: List[Tuple[Any, int]] = []

        if mode in (TreeMode.DESCENDANTS, TreeMode.FULL_TREE):
            desc_rows = await self._fetch_descendants_async(session, root_ids, max_depth, includes)

        if mode in (TreeMode.ANCESTORS, TreeMode.FULL_TREE):
            anc_rows = await self._fetch_ancestors_async(session, root_ids, max_depth, includes)

        root_id_set = set(root_ids)

        if mode == TreeMode.DESCENDANTS:
            return self._build_descendant_tree(desc_rows, root_id_set, includes, dto_max_depth)
        elif mode == TreeMode.ANCESTORS:
            return self._build_ancestor_chain(anc_rows, root_id_set, includes, dto_max_depth)
        else:
            desc_dtos = self._build_descendant_tree(desc_rows, root_id_set, includes, dto_max_depth)
            anc_dtos = self._build_ancestor_chain(anc_rows, root_id_set, includes, dto_max_depth)

            anc_by_pk = {
                getattr(dto, self.config.pk_column): dto
                for dto in anc_dtos
            }
            for dto in desc_dtos:
                root_pk = getattr(dto, self.config.pk_column)
                if root_pk in anc_by_pk:
                    dto.ancestors = anc_by_pk[root_pk].ancestors

            return desc_dtos

    # ── CTE Construction ─────────────────────────────────────────────────

    def _build_descendants_cte(
        self,
        root_ids: List[Any],
        max_depth: Optional[int],
        includes: Optional[List[str]] = None,
    ):
        """
        Construye el CTE recursivo para descendientes.

        SQL equivalente:
            WITH RECURSIVE _descendants AS (
                SELECT *, 0 AS _tree_level FROM equipo WHERE id_equipo IN (:roots)
                UNION ALL
                SELECT e.*, d._tree_level + 1
                FROM equipo e JOIN _descendants d ON e.equipo_superior = d.id_equipo
                WHERE d._tree_level < :max_depth  -- si se especifica
            )
            SELECT * FROM _descendants
        """
        cfg = self.config
        Model = cfg.model_class

        base = (
            select(Model, literal(0).label("_tree_level"))
            .where(cfg.pk_attr.in_(root_ids))
        )

        cte = base.cte(name="_descendants", recursive=True)

        recursive = (
            select(Model, (cte.c._tree_level + 1).label("_tree_level"))
            .where(cfg.parent_attr == getattr(cte.c, cfg.pk_column))
        )

        if max_depth is not None:
            recursive = recursive.where(cte.c._tree_level < max_depth)

        cte = cte.union_all(recursive)

        query = (
            select(Model, cte.c._tree_level)
            .join(cte, cfg.pk_attr == getattr(cte.c, cfg.pk_column))
        )

        if includes:
            loading_options = get_loading_options(Model, includes)
            if loading_options:
                query = query.options(*loading_options)

        return query

    def _build_ancestors_cte(
        self,
        root_ids: List[Any],
        max_depth: Optional[int],
        includes: Optional[List[str]] = None,
    ):
        """
        Construye el CTE recursivo para ancestros.

        SQL equivalente:
            WITH RECURSIVE _ancestors AS (
                SELECT *, 0 AS _tree_level FROM equipo WHERE id_equipo IN (:roots)
                UNION ALL
                SELECT e.*, a._tree_level + 1
                FROM equipo e JOIN _ancestors a ON e.id_equipo = a.equipo_superior
                WHERE a._tree_level < :max_depth  -- si se especifica
            )
            SELECT * FROM _ancestors
        """
        cfg = self.config
        Model = cfg.model_class

        base = (
            select(Model, literal(0).label("_tree_level"))
            .where(cfg.pk_attr.in_(root_ids))
        )

        cte = base.cte(name="_ancestors", recursive=True)

        recursive = (
            select(Model, (cte.c._tree_level + 1).label("_tree_level"))
            .where(cfg.pk_attr == getattr(cte.c, cfg.parent_column))
        )

        if max_depth is not None:
            recursive = recursive.where(cte.c._tree_level < max_depth)

        cte = cte.union_all(recursive)

        query = (
            select(Model, cte.c._tree_level)
            .join(cte, cfg.pk_attr == getattr(cte.c, cfg.pk_column))
        )

        if includes:
            loading_options = get_loading_options(Model, includes)
            if loading_options:
                query = query.options(*loading_options)

        return query

    # ── Query Execution ──────────────────────────────────────────────────

    def _fetch_descendants(
        self,
        session: Session,
        root_ids: List[Any],
        max_depth: Optional[int],
        includes: Optional[List[str]] = None,
    ) -> List[Tuple[Any, int]]:
        query = self._build_descendants_cte(root_ids, max_depth, includes)
        result = session.execute(query)
        return result.all()

    def _fetch_ancestors(
        self,
        session: Session,
        root_ids: List[Any],
        max_depth: Optional[int],
        includes: Optional[List[str]] = None,
    ) -> List[Tuple[Any, int]]:
        query = self._build_ancestors_cte(root_ids, max_depth, includes)
        result = session.execute(query)
        return result.all()

    async def _fetch_descendants_async(
        self,
        session: AsyncSession,
        root_ids: List[Any],
        max_depth: Optional[int],
        includes: Optional[List[str]] = None,
    ) -> List[Tuple[Any, int]]:
        query = self._build_descendants_cte(root_ids, max_depth, includes)
        result = await session.execute(query)
        return result.all()

    async def _fetch_ancestors_async(
        self,
        session: AsyncSession,
        root_ids: List[Any],
        max_depth: Optional[int],
        includes: Optional[List[str]] = None,
    ) -> List[Tuple[Any, int]]:
        query = self._build_ancestors_cte(root_ids, max_depth, includes)
        result = await session.execute(query)
        return result.all()

    # ── Tree Assembly ────────────────────────────────────────────────────

    def _build_descendant_tree(
        self,
        rows: List[Tuple[Any, int]],
        root_ids: Set[Any],
        includes: Optional[List[str]],
        dto_max_depth: int,
    ) -> List[D]:
        """
        Ensambla árbol de descendientes desde filas planas del CTE.

        Cada fila es (instance, _tree_level). Los nodos se indexan por PK
        y se enlazan hijos→padre usando parent_column.
        """
        if not rows:
            return []

        cfg = self.config
        nodes: Dict[Any, TreeNode[D]] = {}

        for row in rows:
            instance, level = row[0], row[1]
            pk = getattr(instance, cfg.pk_column)

            # When all PKs are passed as root_ids the CTE produces duplicate rows
            # (once from the base case at level 0, once as a descendant at level N).
            # Keep only the deepest occurrence - it reflects the node's actual
            # position in the tree.
            if pk in nodes and level <= nodes[pk].level:
                continue

            parent_ref = getattr(instance, cfg.parent_column)

            dto = self.dto_factory(instance, includes, dto_max_depth)
            dto.tree_level = level
            dto.descendants = []

            nodes[pk] = TreeNode(dto=dto, pk=pk, parent_ref=parent_ref, level=level)

        # Link children to parents.
        # A node is a root only when its parent is absent from the result set -
        # do NOT use root_ids here, because every fetched PK is in root_ids when
        # find_many passes all records (which would incorrectly promote every
        # node to a top-level root).
        roots: List[D] = []
        for node in nodes.values():
            if node.parent_ref is None or node.parent_ref not in nodes:
                roots.append(node.dto)
            else:
                parent_node = nodes[node.parent_ref]
                if parent_node.dto.descendants is None:
                    parent_node.dto.descendants = []
                parent_node.dto.descendants.append(node.dto)

        return roots

    def _build_ancestor_chain(
        self,
        rows: List[Tuple[Any, int]],
        root_ids: Set[Any],
        includes: Optional[List[str]],
        dto_max_depth: int,
    ) -> List[D]:
        """
        Ensambla cadena de ancestros desde filas planas del CTE.

        Cada nodo apunta a su padre a través de ancestors=[parent_dto].
        La cadena es recursiva: nodo.ancestors[0].ancestors[0]... hasta la raíz.
        """
        if not rows:
            return []

        cfg = self.config
        nodes: Dict[Any, TreeNode[D]] = {}

        for row in rows:
            instance, level = row[0], row[1]
            pk = getattr(instance, cfg.pk_column)
            parent_ref = getattr(instance, cfg.parent_column)

            dto = self.dto_factory(instance, includes, dto_max_depth)
            dto.tree_level = level
            dto.ancestors = []

            nodes[pk] = TreeNode(dto=dto, pk=pk, parent_ref=parent_ref, level=level)

        # Link each node to its parent as ancestor
        roots: List[D] = []
        for node in nodes.values():
            if node.pk in root_ids:
                roots.append(node.dto)
            if node.parent_ref is not None and node.parent_ref in nodes:
                node.dto.ancestors = [nodes[node.parent_ref].dto]

        return roots