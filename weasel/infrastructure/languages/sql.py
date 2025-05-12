from dataclasses import dataclass

from sqlglot import parse
from sqlglot.errors import ParseError

from weasel.domain.services.interfaces.language import LanguageInterface


@dataclass
class SQLLanguage(LanguageInterface):
    """The *SQL* language."""

    @classmethod
    def recognizes(cls, code: str) -> bool:
        """Check if code matches the language."""
        try:
            parse(code)
        except ParseError:
            return False
        return True

    @classmethod
    def get_extensions(cls) -> set[str]:
        """List the language extensions."""
        return {".ddl", ".dml", ".sql"}
