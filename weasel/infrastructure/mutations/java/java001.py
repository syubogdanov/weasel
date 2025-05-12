from dataclasses import dataclass

from javalang.parse import parse
from javalang.unparser import unparse

from weasel.domain.services.interfaces.mutation import MutationInterface


@dataclass
class JavaMutation(MutationInterface):
    """The *Java* mutation (`P001`).

    Features
    --------
    * Formats to *Java Code Conventions* indents;
    * Removes comments (`//` & `/* ... */`).
    """

    @classmethod
    def mutate(cls, source: str, target: str) -> str:  # noqa: ARG003
        """Mutate `source` using `target` as the reference."""
        return unparse(parse(source)).lstrip()
