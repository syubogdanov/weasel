import asyncio

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
            optimize(expression, rules=[optimize_joins])
            for expression in parse(source)
            if expression
        ]
        return ";\n".join(expression.sql() for expression in expressions) + ";"

    @classmethod
    def as_label(cls) -> str:
        """Return the mutation label."""
        return "SQL007"
