from dataclasses import dataclass

from javalang.parse import parse
from javalang.parser import JavaSyntaxError

from weasel.domain.services.interfaces.language import LanguageInterface
from weasel.domain.types.language import LanguageType


@dataclass
class JavaLanguage(LanguageInterface):
    """The *Java* language."""

    @classmethod
    async def recognizes(cls, code: str) -> bool:
        """Check if code matches the language."""
        try:
            parse(code)
        except JavaSyntaxError:
            return False
        return True

    @classmethod
    def get_extensions(cls) -> set[str]:
        """List the language extensions."""
        return {".jav", ".java"}

    @classmethod
    def as_type(cls) -> LanguageType:
        """Get the language type."""
        return LanguageType.JAVA
