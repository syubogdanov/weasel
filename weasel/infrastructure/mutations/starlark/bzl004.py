from dataclasses import dataclass

from weasel.infrastructure.mutations.python.py005 import PythonMutation


@dataclass
class StarlarkMutation(PythonMutation):
    """The *Starlark* mutation (`BZL004`).

    Features
    --------
    * Simplifies arithmetic operations (`2 + 2` -> `4`).

    See Also
    --------
    * `PY005`.
    """

    @classmethod
    def as_label(cls) -> str:
        """Return the mutation label."""
        return "BZL004"
