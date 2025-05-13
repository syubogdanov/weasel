from dataclasses import dataclass

from weasel.infrastructure.mutations.python.py004 import PythonMutation


@dataclass
class StarlarkMutation(PythonMutation):
    """The *Starlark* mutation (`BZL003`).

    Features
    --------
    * Removes an unreachable code.

    See Also
    --------
    * `PY004`.
    """

    @classmethod
    def as_label(cls) -> str:
        """Return the mutation label."""
        return "BZL003"
