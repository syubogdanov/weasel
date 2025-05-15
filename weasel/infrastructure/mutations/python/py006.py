import ast

from dataclasses import dataclass
from typing import TYPE_CHECKING

from networkx.algorithms.matching import max_weight_matching
from networkx.classes import Graph

from weasel.domain.services.interfaces.mutation import MutationInterface


if TYPE_CHECKING:
    from weasel.domain.services.interfaces.estimator import EstimatorInterface


@dataclass
class PythonMutation(MutationInterface):
    """The *Python* mutation (`PY006`).

    Features
    --------
    * Eliminates syntatic reordering.

    Notes
    -----
    * Block comparison algorithm is used;
    * The Bubble-Down strategy is used.
    """

    _estimator: "EstimatorInterface"

    async def mutate(self, source: str, target: str) -> str:
        """Mutate `source` using `target` as the reference."""
        source_tree = ast.parse(source)
        target_tree = ast.parse(target)

        reorderer = PythonReorderer(_estimator=self._estimator)
        tree = await reorderer.reorder_tree(source_tree, target_tree)

        if not reorderer.is_triggered():
            return source

        tree = ast.fix_missing_locations(tree)
        return ast.unparse(tree)

    @classmethod
    def as_label(cls) -> str:
        """Return the mutation label."""
        return "PY006"


@dataclass
class PythonReorderer:
    """The AST reorderer.

    Notes
    -----
    * Consider this class as a private one.
    """

    _estimator: "EstimatorInterface"

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._triggered: bool = False

    def is_triggered(self) -> bool:
        """Check if any permutation was made."""
        return self._triggered

    async def reorder_tree(self, source: ast.Module, target: ast.Module) -> ast.Module:
        """Reorder `source` using `target` as the reference."""
        body = await self._reorder_list(source.body, target.body)
        return ast.Module(body=body, type_ignores=source.type_ignores)

    async def _reorder_list(self, source: list[ast.AST], target: list[ast.AST]) -> list[ast.AST]:
        """Reorder `source` using `target` as the reference."""
        if not (source_blocks := self._split_into_blocks(source)):
            return []

        if not (target_blocks := self._split_into_blocks(target)):
            return source

        matchings = await self._match_blocks(source_blocks, target_blocks)

        blocks: list[ast.AST | list[ast.AST]] = [[]] * len(source_blocks)

        min_index = min(matchings)
        for index in range(min_index):
            blocks[index] = source_blocks[index]

        max_index = max(matchings)
        for index in range(max_index + 1, len(source_blocks)):
            blocks[index] = source_blocks[index]

        bubble_count = 0
        for index in range(min_index, max_index + 1):
            if index not in matchings:
                blocks[min_index + bubble_count] = source_blocks[index]
                bubble_count += 1

        reordering = sorted(matchings, key=lambda old_index: matchings[old_index])

        for new_index, old_index in enumerate(reordering, start=min_index + bubble_count):
            target_index = matchings[old_index]

            source_block = source_blocks[old_index]
            target_block = target_blocks[target_index]

            if isinstance(source_block, ast.ClassDef) and isinstance(target_block, ast.ClassDef):
                source_block = await self._reorder_class(source_block, target_block)

            blocks[new_index] = source_block

            if new_index != old_index:
                self._triggered = True

        return self._merge_blocks(blocks)

    async def _reorder_class(self, source: ast.ClassDef, target: ast.ClassDef) -> ast.ClassDef:
        """Reorder `source` using `target` as the reference."""
        body = await self._reorder_list(source.body, target.body)
        return ast.ClassDef(
            name=source.name,
            bases=source.bases,
            keywords=source.keywords,
            body=body,
            decorator_list=source.decorator_list,
            type_params=source.type_params,
        )

    async def _compare_two_blocks(
        self, source: ast.AST | list[ast.AST], target: ast.AST | list[ast.AST]
    ) -> float:
        """Compare `source` and `target` blocks."""
        if isinstance(source, ast.ClassDef) and isinstance(target, ast.ClassDef):
            source = await self._reorder_class(source, target)
        return await self._estimator.estimate(ast.unparse(source), ast.unparse(target))

    async def _match_blocks(
        self, source: list[ast.AST | list[ast.AST]], target: list[ast.AST | list[ast.AST]]
    ) -> dict[int, int]:
        """Match `source` and `target` blocks."""
        graph = Graph()

        for index1, block1 in enumerate(source):
            for index2, block2 in enumerate(target, start=len(source)):
                weight = await self._compare_two_blocks(block1, block2)
                graph.add_edge(index1, index2, weight=weight)

        return {
            min(index1, index2): max(index1, index2) - len(source)
            for (index1, index2) in max_weight_matching(graph)
        }

    @classmethod
    def _split_into_blocks(cls, source: list[ast.AST]) -> list[ast.AST | list[ast.AST]]:
        """Split the list of nodes into blocks."""
        blocks: list[ast.AST | list[ast.AST]] = []
        block: list[ast.AST] = []

        for node in source:
            if not isinstance(node, (ast.AsyncFunctionDef, ast.ClassDef, ast.FunctionDef)):
                block.append(node)
                continue
            if block:
                blocks.append(block)
                block = []
            blocks.append(node)

        if block:
            blocks.append(block)

        return blocks

    @classmethod
    def _merge_blocks(cls, blocks: list[ast.AST | list[ast.AST]]) -> list[ast.AST]:
        """Merge the blocks into a single list."""
        nodes: list[ast.AST] = []

        for block in blocks:
            if isinstance(block, list):
                nodes.extend(block)
            else:
                nodes.append(block)

        return nodes
