from dataclasses import dataclass

from javalang.parse import parse
from javalang.unparser import unparse

from weasel.domain.services.interfaces.mutation import MutationInterface


@dataclass
class JavaMutation(MutationInterface):
    """The *Java* mutation (`JAVA001`).

    Features
    --------
    * Formats to *Java Code Conventions* indents;
    * Removes comments (`//` & `/* ... */`).
    """

    @classmethod
    async def mutate(cls, source: str, _target: str) -> str:
        """Mutate `source` using `target` as the reference."""
        return unparse(parse(source)).lstrip()

    @classmethod
    def as_label(cls) -> str:
        """Return the mutation label."""
        return "JAVA001"
