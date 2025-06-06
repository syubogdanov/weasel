from abc import abstractmethod
from typing import Protocol


class MutationInterface(Protocol):
    """The mutation interface."""

    @abstractmethod
    async def mutate(self, source: str, target: str) -> str:
        """Mutate `source` using `target` as the reference."""

    @abstractmethod
    def as_label(self) -> str:
        """Return the mutation label."""
