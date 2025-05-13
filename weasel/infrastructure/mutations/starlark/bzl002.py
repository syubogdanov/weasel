from dataclasses import dataclass

from weasel.infrastructure.mutations.python.py003 import PythonMutation


@dataclass
class StarlarkMutation(PythonMutation):
    """The *Starlark* mutation (`BZL002`).

    Features
    --------
    * Removes unused constants.

    See Also
    --------
    * `PY003`.
    """

    @classmethod
    def as_label(cls) -> str:
        """Return the mutation label."""
        return "BZL002"
