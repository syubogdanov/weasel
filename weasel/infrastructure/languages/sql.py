from dataclasses import dataclass

from sqlglot import parse
from sqlglot.errors import ParseError

from weasel.domain.services.interfaces.language import LanguageInterface
from weasel.domain.types.language import LanguageType


@dataclass
class SQLLanguage(LanguageInterface):
    """The *SQL* language."""

    @classmethod
    async def recognizes(cls, code: str) -> bool:
        """Check if code matches the language."""
        try:
            trees = parse(code)

        except ParseError:
            return False

        return trees != [None]

    @classmethod
    def get_extensions(cls) -> set[str]:
        """List the language extensions."""
        return {".ddl", ".dml", ".sql"}

    @classmethod
    def as_type(cls) -> LanguageType:
        """Get the language type."""
        return LanguageType.SQL
