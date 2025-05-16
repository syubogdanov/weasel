import asyncio

from dataclasses import dataclass
from typing import TYPE_CHECKING

from networkx.algorithms.matching import max_weight_matching
from networkx.classes import Graph
from sqlglot import parse

from weasel.domain.services.interfaces.mutation import MutationInterface


if TYPE_CHECKING:
    from weasel.domain.services.interfaces.estimator import EstimatorInterface


@dataclass
class SQLMutation(MutationInterface):
    """The *SQL* mutation (`SQL014`).

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
        """Mutate `source` using `target` as the reference.

        Notes
        -----
        * `sqlglot` is written in *Rust*.
        """
        source_expressions, target_expressions = await asyncio.gather(
            asyncio.to_thread(parse, source), asyncio.to_thread(parse, target)
        )

        source_blocks = [expression.sql() for expression in source_expressions if expression]
        target_blocks = [expression.sql() for expression in target_expressions if expression]

        if not source_blocks or not target_blocks:
            return source

        matchings = await self._match_blocks(source_blocks, target_blocks)

        blocks: list[str] = [""] * len(source_blocks)

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
            blocks[new_index] = source_blocks[old_index]
            if new_index != old_index:
                self._triggered = True

        return ";\n".join(blocks) + ";"

    async def _match_blocks(self, source: list[str], target: list[str]) -> dict[int, int]:
        """Match `source` and `target` blocks."""
        graph = Graph()

        for index1, block1 in enumerate(source):
            for index2, block2 in enumerate(target, start=len(source)):
                weight = await self._estimator.estimate(block1, block2)
                graph.add_edge(index1, index2, weight=weight)

        return {
            min(index1, index2): max(index1, index2) - len(source)
            for (index1, index2) in max_weight_matching(graph)
        }

    @classmethod
    def as_label(cls) -> str:
        """Return the mutation label."""
        return "SQL014"
