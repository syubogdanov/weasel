from dataclasses import dataclass

from weasel.infrastructure.mutations.python.py006 import PythonMutation


@dataclass
class StarlarkMutation(PythonMutation):
    """The *Starlark* mutation (`BZL005`).

    Features
    --------
    * Eliminates syntatic permutations.

    See Also
    --------
    * `PY006`.
    """
