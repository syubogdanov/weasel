from dataclasses import dataclass

from weasel.infrastructure.mutations.python.py001 import PythonMutation


@dataclass
class StarlarkMutation(PythonMutation):
    """The *Starlark* mutation (`BZL001`).

    Features
    --------
    * Formats to *PEP-8* indents;
    * Concatenates space-delimited strings;
    * Removes comments (`#`).

    See Also
    --------
    * `PY001`.
    """

    @classmethod
    def as_label(cls) -> str:
        """Return the mutation label."""
        return "BZL001"
