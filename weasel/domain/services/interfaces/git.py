from abc import abstractmethod
from pathlib import Path
from typing import Protocol


class GitInterface(Protocol):
    """The *Git* interface."""

    @abstractmethod
    async def clone(
        self,
        user: str,
        repo: str,
        *,
        branch: str | None,
        commit: str | None = None,
        tag: str | None = None,
    ) -> Path:
        """Clone the repository."""
