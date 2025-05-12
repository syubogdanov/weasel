from abc import abstractmethod
from typing import Protocol


class CacheInterface(Protocol):
    """The estimator interface."""

    @abstractmethod
    async def get(self, bucket: str, key: str) -> str | None:
        """Get the value for `key`."""

    @abstractmethod
    async def put(self, bucket: str, key: str, value: str) -> None:
        """Put the value for `key`."""
