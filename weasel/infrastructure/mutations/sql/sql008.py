from dataclasses import dataclass

from sqlglot import parse
from sqlglot.optimizer import optimize
from sqlglot.optimizer.eliminate_subqueries import eliminate_subqueries

from weasel.domain.services.interfaces.mutation import MutationInterface


@dataclass
class SQLMutation(MutationInterface):
    """The *SQL* mutation (`SQL008`).

    Features
    --------
    * Each expression starts from a new line;
    * Rewrites derived tables as CTES, deduplicating if possible.
    """

    @classmethod
    async def mutate(cls, source: str, _target: str) -> str:
        """Mutate `source` using `target` as the reference."""
        expressions = [expression for expression in parse(source) if expression]
        as_strings = [
            optimize(expression, rules=[eliminate_subqueries]).sql() for expression in expressions
        ]
        return ";\n".join(as_strings) + ";"

    @classmethod
    def as_label(cls) -> str:
        """Return the mutation label."""
        return "SQL008"
