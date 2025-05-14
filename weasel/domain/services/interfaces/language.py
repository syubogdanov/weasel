from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol


if TYPE_CHECKING:
    from weasel.domain.types.language import LanguageType


class LanguageInterface(Protocol):
    """The language interface."""

    @abstractmethod
    async def recognizes(self, code: str) -> bool:
        """Check if the code matches the language."""

    @abstractmethod
    def get_extensions(self) -> set[str]:
        """List the extensions of the language."""

    @abstractmethod
    def as_type(self) -> "LanguageType":
        """Get the language type."""
