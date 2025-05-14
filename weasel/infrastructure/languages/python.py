import ast

from dataclasses import dataclass

from weasel.domain.services.interfaces.language import LanguageInterface
from weasel.domain.types.language import LanguageType


@dataclass
class PythonLanguage(LanguageInterface):
    """The *Python* language."""

    @classmethod
    async def recognizes(cls, code: str) -> bool:
        """Check if code matches the language."""
        try:
            ast.parse(code)
        except SyntaxError:
            return False
        return True

    @classmethod
    def get_extensions(cls) -> set[str]:
        """List the language extensions."""
        return {".py", ".py3", ".pyi"}

    @classmethod
    def as_type(cls) -> LanguageType:
        """Get the language type."""
        return LanguageType.PYTHON
