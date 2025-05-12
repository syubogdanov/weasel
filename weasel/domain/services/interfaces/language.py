from abc import abstractmethod
from typing import Protocol


class LanguageInterface(Protocol):
    """The language interface."""

    @abstractmethod
    def recognizes(self, code: str) -> bool:
        """Check if the code matches the language."""

    @abstractmethod
    def get_extensions(self) -> set[str]:
        """List the extensions of the language."""
