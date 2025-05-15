from dataclasses import dataclass

from sqlglot import parse
from sqlglot.optimizer import optimize
from sqlglot.optimizer.qualify_columns import quote_identifiers

from weasel.domain.services.interfaces.mutation import MutationInterface


@dataclass
class SQLMutation(MutationInterface):
    """The *SQL* mutation (`SQL013`).

    Features
    --------
    * Each expression starts from a new line;
    * Ensures all identifiers that need to be quoted are quoted..
    """

    @classmethod
    async def mutate(cls, source: str, _target: str) -> str:
        """Mutate `source` using `target` as the reference."""
        expressions = [expression for expression in parse(source) if expression]
        as_strings = [
            optimize(expression, rules=[quote_identifiers]).sql() for expression in expressions
        ]
        return ";\n".join(as_strings) + ";"

    @classmethod
    def as_label(cls) -> str:
        """Return the mutation label."""
        return "SQL013"
