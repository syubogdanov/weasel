import ast

from dataclasses import dataclass

from weasel.domain.services.interfaces.mutation import MutationInterface


@dataclass
class PythonMutation(MutationInterface):
    """The *Python* mutation (`P001`).

    Features
    --------
    * Formats to *PEP-8* indents;
    * Concatenates space-delimited strings;
    * Removes comments (`#`).
    """

    @classmethod
    def mutate(cls, source: str, target: str) -> str:  # noqa: ARG003
        """Mutate `source` using `target` as the reference."""
        mutated = ast.unparse(ast.parse(source))
        return mutated if mutated != source else source
