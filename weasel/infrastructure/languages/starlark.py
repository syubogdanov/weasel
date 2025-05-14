import ast

from dataclasses import dataclass

from weasel.domain.services.interfaces.language import LanguageInterface
from weasel.domain.types.language import LanguageType


@dataclass
class StarlarkLanguage(LanguageInterface):
    """The *Starlark* language."""

    @classmethod
    async def recognizes(cls, code: str) -> bool:
        """Check if code matches the language."""
        try:
            tree = ast.parse(code)

        except SyntaxError:
            return False

        visitor = StarlarkVisitor()
        visitor.visit(tree)

        if visitor.is_triggered():
            return False

        return bool(tree.body)

    @classmethod
    def get_extensions(cls) -> set[str]:
        """List the language extensions."""
        return {".BUILD", ".bazel", ".bzl", ".star"}

    @classmethod
    def as_type(cls) -> LanguageType:
        """Get the language type."""
        return LanguageType.STARLARK


@dataclass
class StarlarkVisitor(ast.NodeVisitor):
    """The *Starlark* visitor.

    Notes
    -----
    * Consider this class as a private one.
    """

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._triggered: bool = False

    def is_triggered(self) -> bool:
        """Check if the visitor was triggered."""
        return self._triggered

    def visit_ClassDef(self, _node: ast.ClassDef) -> None:
        """Visit a class definition."""
        self._triggered = True

    def visit_GeneratorExp(self, _node: ast.GeneratorExp) -> None:
        """Visit a generator expression."""
        self._triggered = True

    def visit_Import(self, _node: ast.Import) -> None:
        """Visit an `import` statement."""
        self._triggered = True

    def visit_ImportFrom(self, _node: ast.ImportFrom) -> None:
        """Visit an `import from` statement."""
        self._triggered = True

    def visit_While(self, _node: ast.While) -> None:
        """Visit a `while` statement."""
        self._triggered = True

    def visit_Yield(self, _node: ast.Yield) -> None:
        """Visit a `yield` statement."""
        self._triggered = True

    def visit_YieldFrom(self, _node: ast.YieldFrom) -> None:
        """Visit a `yield from` statement."""
        self._triggered = True
