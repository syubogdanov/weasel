import ast

from dataclasses import dataclass

from weasel.domain.services.interfaces.mutation import MutationInterface


@dataclass
class PythonMutation(MutationInterface):
    """The *Python* mutation (`PY001`).

    Features
    --------
    * Formats to *PEP-8* indents;
    * Concatenates space-delimited strings;
    * Removes comments (`#`).
    """

    @classmethod
    async def mutate(cls, source: str, target: str) -> str:  # noqa: ARG003
        """Mutate `source` using `target` as the reference."""
        return ast.unparse(ast.parse(source))

    @classmethod
    def as_label(cls) -> str:
        """Return the mutation label."""
        return "PY001"
