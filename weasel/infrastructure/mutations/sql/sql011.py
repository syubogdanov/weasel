import asyncio

from dataclasses import dataclass

from sqlglot import parse
from sqlglot.optimizer import optimize
from sqlglot.optimizer.eliminate_ctes import eliminate_ctes

from weasel.domain.services.interfaces.mutation import MutationInterface


@dataclass
class SQLMutation(MutationInterface):
    """The *SQL* mutation (`SQL011`).

    Features
    --------
    * Each expression starts from a new line;
    * Removes unused CTEs from an expression.
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
            optimize(expression, rules=[eliminate_ctes])
            for expression in parse(source)
            if expression
        ]
        return ";\n".join(expression.sql() for expression in expressions) + ";"

    @classmethod
    def as_label(cls) -> str:
        """Return the mutation label."""
        return "SQL011"
