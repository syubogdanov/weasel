import asyncio

from dataclasses import dataclass
from heapq import nlargest
from typing import TYPE_CHECKING

from weasel.domain.services.interfaces.mutation_tree import MutationTreeInterface


if TYPE_CHECKING:
    from weasel.domain.services.interfaces.estimator import EstimatorInterface
    from weasel.domain.services.interfaces.mutation import MutationInterface


@dataclass
class MutationTreeAdapter(MutationTreeInterface):
    """The greedy mutation tree."""

    _degree_of_freedom: int
    _depth: int
    _estimator: "EstimatorInterface"
    _mutations: list["MutationInterface"]
    _tolerance: float

    async def get_mutations(self, source: str, target: str) -> list["MutationInterface"]:
        """Get the set of mutations required to convert `source` to `target`."""
        score = await self._estimator.estimate(source, target)
        optimum = await self._dfs(source, target, DFSOptions(mutations=[], score=score))
        return optimum.mutations

    async def _dfs(self, source: str, target: str, options: "DFSOptions") -> "DFSOptions":
        """Perform a depth-first search."""
        if options.depth == self._depth:
            return options

        if not self._degree_of_freedom:
            return options

        coroutines = [self._compare(source, target, mutation) for mutation in self._mutations]
        scores = await asyncio.gather(*coroutines)

        candidates = [
            (mutation, score)
            for mutation, score in zip(self._mutations, scores, strict=True)
            if score > options.score + self._tolerance
        ]

        optimums: list[DFSOptions] = []

        for mutation, score in nlargest(self._degree_of_freedom, candidates, key=lambda p: p[1]):
            mutated = await mutation.mutate(source, target)

            next_mutations = [*options.mutations, mutation]
            next_options = DFSOptions(next_mutations, score)

            optimum = await self._dfs(mutated, target, next_options)
            optimums.append(optimum)

        return max(optimums, key=lambda o: o.score, default=options)

    async def _compare(self, source: str, target: str, mutation: "MutationInterface") -> float:
        """Compare `source` and `target` using `mutation`."""
        mutated = await mutation.mutate(source, target)
        return await self._estimator.estimate(mutated, target)


@dataclass
class DFSOptions:
    """The DFS options.

    Notes
    -----
    * Consider this class as a private one.
    """

    mutations: list["MutationInterface"]
    score: float

    @property
    def depth(self) -> int:
        """Get the depth."""
        return len(self.mutations)
