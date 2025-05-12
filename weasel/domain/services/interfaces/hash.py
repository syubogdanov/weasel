from abc import abstractmethod
from typing import Protocol


class HashInterface(Protocol):
    """The hash interface."""

    @abstractmethod
    async def hash(self, text: str) -> str:
        """Hash the given text."""
