from dataclasses import dataclass

from sqlglot import parse
from sqlglot.optimizer import optimize
from sqlglot.optimizer.optimize_joins import optimize_joins

from weasel.domain.services.interfaces.mutation import MutationInterface


@dataclass
class SQLMutation(MutationInterface):
    """The *SQL* mutation (`SQL007`).

    Features
    --------
    * Each expression starts from a new line;
    * Removes cross joins if possible and reorder joins based on predicate dependencies.
    """

    @classmethod
    async def mutate(cls, source: str, _target: str) -> str:
        """Mutate `source` using `target` as the reference."""
        expressions = [expression for expression in parse(source) if expression]
        as_strings = [
            optimize(expression, rules=[optimize_joins]).sql() for expression in expressions
        ]
        return ";\n".join(as_strings) + ";"

    @classmethod
    def as_label(cls) -> str:
        """Return the mutation label."""
        return "SQL007"
