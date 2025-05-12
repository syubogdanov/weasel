from dataclasses import dataclass
from heapq import nlargest
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from weasel.domain.services.interfaces.estimator import EstimatorInterface
    from weasel.domain.services.interfaces.mutation import MutationInterface


@dataclass
class MutationTree:
    """The mutation tree."""

    _degree_of_freedom: int
    _depth: int
    _estimator: "EstimatorInterface"
    _mutations: list["MutationInterface"]

    def get_mutations(self, source: str, target: str) -> set["MutationInterface"]:
        """Get the set of mutations required to convert `source` to `target`."""
        optimum = self._dfs(source, target, DFSOptions.initial())
        return optimum.mutations

    def _dfs(self, source: str, target: str, options: "DFSOptions") -> "DFSOptions":
        """Perform a depth-first search."""
        if options.depth == self._depth:
            return options

        scores: list[tuple[MutationInterface, float]] = []

        for mutation in self._mutations:
            if mutation not in options.mutations:
                mutated = mutation.mutate(source, target)
                score = self._estimator.estimate(mutated, target)
                if score > options.score:
                    pair = (mutation, score)
                    scores.append(pair)

        optimums: list[DFSOptions] = []

        for mutation, score in nlargest(self._degree_of_freedom, scores, key=lambda x: x[1]):
            mutated = mutation.mutate(source, target)

            next_mutations = [*options.mutations, mutation]
            next_options = DFSOptions(next_mutations, score)

            optimum = self._dfs(mutated, target, next_options)
            optimums.append(optimum)

        return max(optimums, key=lambda o: o.score, default=options)


@dataclass
class DFSOptions:
    """The DFS options."""

    mutations: list["MutationInterface"]
    score: float

    @property
    def depth(self) -> int:
        """Get the depth."""
        return len(self.mutations)

    @classmethod
    def initial(cls) -> "DFSOptions":
        """Return the initial options."""
        return cls(mutations=[], score=0.0)
