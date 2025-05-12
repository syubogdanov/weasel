from abc import abstractmethod
from pathlib import Path
from typing import Protocol


class SealerInterface(Protocol):
    """The sealer interface."""

    @abstractmethod
    async def seal(self, path: Path) -> Path:
        """Seal the file or directory."""

    @abstractmethod
    async def clean(self) -> None:
        """Clean the sealing layer."""
