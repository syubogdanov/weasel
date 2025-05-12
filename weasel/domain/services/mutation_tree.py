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

        scores: dict[MutationInterface, float] = {}

        for mutation in self._mutations:
            if mutation not in options.mutations:
                mutated = mutation.mutate(source, target)
                score = self._estimator.estimate(mutated, target)
                if score > options.score:
                    scores[mutation] = score

        if not (top := nlargest(self._degree_of_freedom, scores.items(), key=lambda m: m[1])):
            return options

        optimums: list[DFSOptions] = []

        for mutation, score in top:
            mutated = mutation.mutate(source, target)

            next_mutations = options.mutations | {mutation}
            next_options = DFSOptions(next_mutations, score)

            optimum = self._dfs(mutated, target, next_options)
            optimums.append(optimum)

        return max(optimums, key=lambda o: o.score)


@dataclass
class DFSOptions:
    """The DFS options."""

    mutations: set["MutationInterface"]
    score: float

    @property
    def depth(self) -> int:
        """Get the depth."""
        return len(self.mutations)

    @classmethod
    def initial(cls) -> "DFSOptions":
        """Return the initial options."""
        return cls(mutations=set(), score=0.0)
