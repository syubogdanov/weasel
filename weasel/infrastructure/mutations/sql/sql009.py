import asyncio

from dataclasses import dataclass

from sqlglot import parse
from sqlglot.optimizer import optimize
from sqlglot.optimizer.merge_subqueries import merge_subqueries

from weasel.domain.services.interfaces.mutation import MutationInterface


@dataclass
class SQLMutation(MutationInterface):
    """The *SQL* mutation (`SQL009`).

    Features
    --------
    * Each expression starts from a new line;
    * Merge derived tables into the outer query.
    """

    @classmethod
    async def mutate(cls, source: str, _target: str) -> str:
        """Mutate `source` using `target` as the reference.

        Notes
        -----
        * `sqlglot` is written in *Rust*.
        """
        return await asyncio.to_thread(cls._mutate, source)

    @classmethod
    def _mutate(cls, source: str) -> str:
        """Mutate `source`."""
        expressions = [
            optimize(expression, rules=[merge_subqueries])
            for expression in parse(source)
            if expression
        ]
        return ";\n".join(expression.sql() for expression in expressions) + ";"

    @classmethod
    def as_label(cls) -> str:
        """Return the mutation label."""
        return "SQL009"
